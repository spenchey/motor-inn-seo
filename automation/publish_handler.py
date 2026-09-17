#!/usr/bin/env python3
"""Prepare approved DealerOn/content packets; optionally execute approved AI PRs."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import urlparse

try:
    from .common import atomic_json, read_json, utcnow, lock, fresh
    from .approval_sync import DEFAULT_ROOT, DEFAULT_CONFIG, verify_approval, _atomic_text, sync as sync_approvals
except ImportError:
    from common import atomic_json, read_json, utcnow, lock, fresh
    from approval_sync import DEFAULT_ROOT, DEFAULT_CONFIG, verify_approval, _atomic_text, sync as sync_approvals


def source_check(job: dict, meta: dict) -> None:
    """Publication admission requires fresh source evidence, never stale approval alone."""
    if not isinstance(meta, dict):
        raise ValueError("Draft metadata must be an object")
    for key in ("fixture", "fixture_only"):
        if meta.get(key) or job.get(key):
            raise ValueError("Fixture jobs are forbidden in the publication pipeline")
    evidence = meta.get("source_evidence", [])
    if not evidence:
        raise ValueError("Missing source evidence for publication")
    for item in evidence:
        if not isinstance(item, dict) or item.get("verified") is not True:
            raise ValueError("Source evidence must be structured and verified")
        timestamp = item.get("retrieved_at", item.get("fetched_at", item.get("checked_at")))
        if not fresh(timestamp, 7):
            raise ValueError("Source evidence is stale or lacks a verified retrieval timestamp")
        if item.get("valid_until"):
            try:
                expiry = datetime.fromisoformat(item["valid_until"].replace("Z", "+00:00"))
                if expiry <= datetime.now(timezone.utc):
                    raise ValueError("Source evidence has expired")
            except (TypeError, ValueError) as exc:
                raise ValueError("Source evidence has expired or invalid validity timestamp") from exc
        source_path = item.get("source_path")
        source_hash = item.get("sha256")
        if source_path and source_hash:
            path = Path(source_path)
            if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != source_hash:
                raise ValueError("Source file changed after evidence collection")

    if meta.get("kind") == "content_post":
        manifest_path = meta.get("upstream_manifest_path")
        manifest_hash = meta.get("upstream_manifest_sha256")
        if not manifest_path or not manifest_hash:
            raise ValueError("Content post requires immutable upstream manifest evidence")
        manifest = Path(manifest_path)
        if manifest.is_symlink() or hashlib.sha256(manifest.read_bytes()).hexdigest() != manifest_hash:
            raise ValueError("Content manifest changed after approval")
        for payload in meta.get("content_files", []):
            source = payload.get("source_path")
            if not source:
                raise ValueError("Content post lacks original source path")
            path = Path(source)
            if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != payload.get("sha256"):
                raise ValueError("Content source changed after approval")


def relative_path(value: str) -> Path:
    path = Path(value)
    if not value or path.is_absolute() or ".." in path.parts or ".git" in path.parts or path == Path("."):
        raise ValueError("Unsafe relative content path")
    return path


def final_html(directory: Path) -> bytes:
    """Return exactly the approved candidate bytes; publication never rewrites them."""
    return (directory / "index.html").read_bytes()


def make_packet(root: Path, job: dict, directory: Path, kind: str) -> Path:
    slug = job["slug"]
    bucket = "ready-for-content" if kind == "content_post" else "ready-for-dealeron"
    dest = root / bucket / slug
    if dest.is_symlink():
        raise ValueError("Symlink output directory forbidden")
    if dest.exists():
        marker = read_json(dest / "packet.json")
        if marker.get("draft_digest") != job["draft_digest"]:
            raise ValueError("A different approved packet already exists for this slug")
        # Reconstruct on retries to repair interrupted or altered packet files.
    dest.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{slug}-", dir=dest.parent))
    try:
        for name in ("index.html", "meta.json", "evidence.md", "qa-report.json"):
            shutil.copyfile(directory / name, staging / name)
        if kind != "content_post":
            (staging / "index.html").write_bytes(final_html(directory))
        meta = read_json(directory / "meta.json")
        if kind == "content_post":
            content_files = meta.get("content_files", [])
            if not content_files:
                raise ValueError("Content post has no immutable source payload")
            for payload in content_files:
                target = staging / "content" / relative_path(payload["path"])
                data = payload["text"].encode()
                if hashlib.sha256(data).hexdigest() != payload["sha256"]:
                    raise ValueError("Content post payload hash mismatch")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            text = f"Approved content post: {slug}\nDigest: {job['draft_digest']}\nUse the exact files in content/. Route through the existing approved October content owner. No social publication or customer contact was performed.\n"
            if meta.get("publication_blockers"):
                text += "\nUpstream publication blockers remain (handoff does not clear these):\n" + "\n".join(str(x) for x in meta["publication_blockers"]) + "\n"
            _atomic_text(staging / "handoff.txt", text)
        else:
            text = (f"DealerOn page-creation request: {meta.get('title', job.get('title', slug))}\n"
                    f"Requested slug: /{slug}/\n"
                    f"Target site: {meta.get('site_url', meta.get('target_url', job.get('site_url', 'CONFIRM SITE BEFORE SUBMISSION')))}\n"
                    f"Approved draft digest: {job['draft_digest']}\n\n"
                    "Please create the attached page using index.html. Preserve the metadata, canonical URL, internal links, "
                    "viewport and structured data recorded in meta.json. Return the preview URL for verification before activation. "
                    "Keep previews access-controlled. Activate only after preview verification; preserve the approved HTML bytes.\n"
                    "Attachments: index.html, meta.json, evidence.md, qa-report.json.\n"
                    "This local packet is prepared; no support ticket or email has been submitted.\n")
            _atomic_text(staging / "submission.txt", text)
        atomic_json(staging / "packet.json", {"slug": slug, "kind": kind, "draft_digest": job["draft_digest"],
                    "approval_receipt": job["approval_receipt"], "prepared_at": utcnow(),
                    "final_html_sha256": hashlib.sha256((staging / 'index.html').read_bytes()).hexdigest(),
                    "transform": "none-approved-bytes"})
        if dest.exists():
            # Owned generated folder only; all its payload is regenerated from approved artifacts.
            for entry in staging.iterdir():
                existing = dest / entry.name
                if existing.is_symlink():
                    raise ValueError("Symlink packet entry forbidden")
                if entry.is_dir():
                    if existing.exists():
                        shutil.rmtree(existing)
                    entry.replace(existing)
                else:
                    entry.replace(existing)
            shutil.rmtree(staging)
        else:
            staging.replace(dest)
        return dest
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def run(args: list[str], cwd: Path, allowed: tuple[int, ...] = (0,)) -> subprocess.CompletedProcess:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, timeout=120)
    if result.returncode not in allowed:
        raise ValueError(f"{args[0]} {args[1]} failed (exit {result.returncode}): {result.stderr[-1000:]}")
    return result


def ai_settings(config: dict, meta: dict) -> tuple[dict, str, Path]:
    settings = config.get("ai_proxy", {})
    for key in ("repo_path", "remote", "base_branch", "content_directory", "allowed_hosts"):
        if not settings.get(key):
            raise ValueError(f"Missing ai_proxy.{key}; AI PR is blocked")
    target = meta.get("canonical_url", meta.get("target_url", meta.get("site_url", "")))
    parsed = urlparse(target)
    if parsed.scheme != "https" or parsed.hostname not in settings["allowed_hosts"] or not parsed.hostname.startswith("ai.") or parsed.username or parsed.password:
        raise ValueError("AI destination is not an explicitly allowed HTTPS ai.* host")
    for key in ("remote", "base_branch"):
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", settings[key]) or ".." in settings[key]:
            raise ValueError(f"Invalid ai_proxy.{key}")
    content = relative_path(settings["content_directory"])
    repo = Path(settings["repo_path"]).expanduser()
    if not repo.is_absolute() or not repo.is_dir():
        raise ValueError("AI proxy repository must be an existing absolute directory")
    return settings, parsed.hostname, content


def ai_pr(root: Path, config: dict, job: dict, directory: Path, meta: dict, execute: bool) -> dict:
    settings, host, content = ai_settings(config, meta)
    slug, digest = job["slug"], job["draft_digest"]
    branch = f"seo/{slug}-{digest[:16]}"
    result = {"slug": slug, "draft_digest": digest, "branch": branch, "status": "prepared_not_pushed"}
    state_path = root / "ai-prs" / f"{slug}.json"
    if state_path.exists():
        previous = read_json(state_path)
        if previous.get("draft_digest") != digest:
            raise ValueError("AI PR state conflicts with a different draft")
        if previous.get("status") == "pr_opened":
            return previous
    if not execute:
        atomic_json(state_path, result)
        return result
    # Admission is repeated immediately before any repository mutation.
    verify_approval(root, config, job)
    source_check(job, meta)
    repo = Path(settings["repo_path"]).expanduser()
    remote, base = settings["remote"], settings["base_branch"]
    run(["git", "rev-parse", "--show-toplevel"], repo)
    run(["git", "fetch", "--", remote, base], repo)
    worktree = root.resolve() / "worktrees" / f"{slug}-{digest[:16]}"
    if worktree.is_symlink():
        raise ValueError("Symlink worktree forbidden")
    if not worktree.exists():
        worktree.parent.mkdir(parents=True, exist_ok=True)
        branch_exists = run(["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"], repo, (0, 1))
        if branch_exists.returncode == 0:
            run(["git", "worktree", "add", str(worktree), branch], repo)
        else:
            remote_exists = run(["git", "ls-remote", "--exit-code", "--heads", remote, f"refs/heads/{branch}"], repo, (0, 2))
            if remote_exists.returncode == 0:
                run(["git", "fetch", "--", remote, f"{branch}:refs/heads/{branch}"], repo)
                run(["git", "worktree", "add", str(worktree), branch], repo)
            else:
                run(["git", "worktree", "add", "-b", branch, str(worktree), f"{remote}/{base}"], repo)
    if run(["git", "branch", "--show-current"], worktree).stdout.strip() != branch:
        raise ValueError("AI worktree is not on its isolated approved branch")
    destination = worktree / content / host / slug
    cursor = worktree
    for part in (content / host / slug).parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError("AI content path contains symlinks")
    if not destination.resolve().is_relative_to(worktree.resolve()):
        raise ValueError("AI content path escapes worktree")
    destination.mkdir(parents=True, exist_ok=True)
    owned = {str((destination / name).relative_to(worktree)) for name in ("index.html", "meta.json", "evidence.md")}
    changed = set(run(["git", "diff", "--name-only", f"{remote}/{base}...HEAD"], worktree).stdout.splitlines())
    dirty = run(["git", "status", "--porcelain", "--untracked-files=all"], worktree).stdout.splitlines()
    if not changed.issubset(owned) or any(line[3:] not in owned for line in dirty):
        raise ValueError("AI worktree contains changes outside this approved page")
    for name in ("index.html", "meta.json", "evidence.md"):
        if (destination / name).is_symlink():
            raise ValueError("Symlink AI artifact forbidden")
        shutil.copyfile(directory / name, destination / name)
    (destination / 'index.html').write_bytes(final_html(directory))
    run(["git", "add", "--", *sorted(owned)], worktree)
    if run(["git", "diff", "--cached", "--quiet"], worktree, (0, 1)).returncode:
        run(["git", "commit", "-m", f"Add approved SEO page {slug} ({digest[:12]})"], worktree)
    verify_approval(root, config, job)
    source_check(job, meta)
    run(["git", "push", "--", remote, f"HEAD:refs/heads/{branch}"], worktree)
    prs = json.loads(run(["gh", "pr", "list", "--head", branch, "--state", "all", "--json", "url,state"], worktree).stdout)
    if prs:
        if prs[0]["state"] == "CLOSED":
            raise ValueError("Approved AI PR was closed; no duplicate PR will be created")
        url = prs[0]["url"]
    else:
        body = root / "ai-prs" / f"{slug}-body.md"
        _atomic_text(body, f"Adds the approved page `{slug}`.\n\nSpencer approval is bound to SHA-256 `{digest}`; QA and source evidence were checked before push.\n\nPage activation remains governed by the proxy repository deployment workflow.\n")
        url = run(["gh", "pr", "create", "--head", branch, "--base", base,
                   "--title", f"SEO: {slug}", "--body-file", str(body.resolve())], worktree).stdout.strip()
    result.update({"status": "pr_opened", "url": url, "worktree": str(worktree), "prepared_at": utcnow()})
    atomic_json(state_path, result)
    return result


def weekly_email(root: Path, config: dict) -> Path | None:
    week = datetime.now(timezone.utc).strftime("%G-W%V")
    path = root / "email-drafts" / f"dealeron-{week}.md"
    packets = []
    for marker in sorted((root / "ready-for-dealeron").glob("*/packet.json")):
        packet = read_json(marker)
        prepared = datetime.fromisoformat(packet["prepared_at"].replace("Z", "+00:00"))
        if prepared.strftime("%G-W%V") == week:
            packets.append(marker.parent)
    if not packets:
        return None
    recipient = config.get("dealeron", {}).get("support_email") or "[DealerOn support recipient must be configured]"
    rows = [f"To: {recipient}", f"Subject: Motor Inn approved page creation requests — {week}", "", "Hello DealerOn Support,", "",
            "Please prepare the following approved pages and return preview URLs for verification.", ""]
    rows.extend(f"- {p.name}: {p / 'submission.txt'} (HTML, metadata and evidence attached from the same folder)" for p in packets)
    rows.extend(["", "Please preserve the supplied metadata and structured data.", "", "Local email draft only; Jeeves must handle the existing authorized send workflow.", ""])
    _atomic_text(path, "\n".join(rows))
    atomic_json(root / "handoffs" / f"jeeves-dealeron-{week}.json", {
        "kind": "dealeron_weekly_email", "week": week, "status": "prepared_not_sent",
        "draft_path": str(path), "packet_paths": [str(p) for p in packets],
        "recipient": config.get("dealeron", {}).get("support_email"), "created_at": utcnow()})
    return path


def publish(root: Path, config: dict, execute_ai: bool = False) -> dict:
    root = Path(root)
    result = {"dealeron": [], "content_posts": [], "ai": [], "errors": []}
    with lock(root, "queue"):
        approval_result = sync_approvals(root, config, _lock_held=True)
        if approval_result["errors"]:
            result["errors"].extend({"approval_sync": error} for error in approval_result["errors"])
            atomic_json(root / "publish-last-run.json", {"ran_at": utcnow(), **result})
            return result
        for path in sorted((root / "queue" / "approved").glob("*.json")):
            try:
                if path.is_symlink():
                    raise ValueError("Symlink queue job forbidden")
                job = read_json(path)
                if job.get('slug') != path.stem:
                    raise ValueError('Approved filename must match slug')
                if job.get('fixture_only') and root.resolve() == DEFAULT_ROOT.resolve():
                    raise ValueError('Synthetic fixtures cannot enter production publication')
                directory = verify_approval(root, config, job)
                meta = read_json(directory / "meta.json")
                source_check(job, meta)
                if meta.get("kind") != "content_post":
                    try:
                        from .page_generator import validate_draft
                    except ImportError:
                        from page_generator import validate_draft
                    qa = validate_draft(directory)
                    if qa.get("passed") is not True:
                        raise ValueError("Fresh publication QA failed: " + "; ".join(qa.get("errors", [])))
                # Routing comes from digest-bound metadata, never mutable job assertions.
                kind = meta.get("kind", "seo_page")
                target_url = meta.get("canonical_url", meta.get("target_url", meta.get("site_url", "")))
                host = urlparse(target_url).hostname or ""
                platform = meta.get("target_platform", meta.get("destination", "dealeron"))
                if kind == "content_post" or platform == "content_post":
                    packet = make_packet(root, job, directory, "content_post")
                    result["content_posts"].append(str(packet))
                elif host.startswith("ai.") or platform in ("ai_proxy", "ai-proxy"):
                    outcome = ai_pr(root, config, job, directory, meta, execute_ai)
                    result["ai"].append(outcome)
                    if outcome["status"] != "pr_opened":
                        continue
                elif platform == "dealeron":
                    packet = make_packet(root, job, directory, "seo_page")
                    result["dealeron"].append(str(packet))
                else:
                    raise ValueError("Unknown publication target platform")
                job.update({"status": "ready", "ready_at": utcnow()})
                atomic_json(root / "queue" / "ready" / path.name, job)
                path.unlink()
            except (ValueError, OSError, KeyError, TypeError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
                result["errors"].append({"job": path.name, "error": str(exc)})
        email = weekly_email(root, config)
        result["weekly_email_draft"] = str(email) if email else None
        atomic_json(root / "publish-last-run.json", {"ran_at": utcnow(), **result})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--execute-ai", action="store_true", help="Create approved isolated branches, push and open PRs")
    args = parser.parse_args()
    try:
        result = publish(args.root, read_json(args.config), args.execute_ai)
        print(json.dumps(result, indent=2))
        return 1 if result["errors"] else 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
