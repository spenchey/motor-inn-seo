#!/usr/bin/env python3
"""Digest-bound Spencer approvals, recorded by a Slack-authenticated Jeeves bridge."""
from __future__ import annotations

import argparse
from contextlib import nullcontext
from decimal import Decimal
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import stat
import time

try:
    from .common import atomic_json, read_json, utcnow, validate_slug, lock, draft_digest
except ImportError:
    from common import atomic_json, read_json, utcnow, validate_slug, lock, draft_digest

DEFAULT_ROOT = Path(__file__).resolve().parents[1] / "pipeline"
DEFAULT_CONFIG = Path(__file__).with_name("config.json")
COMMAND = re.compile(r"(APPROVE|HOLD|REJECT) ([a-z0-9]+(?:-[a-z0-9]+)*) ([a-f0-9]{64})")


def key_bytes(path: str) -> bytes:
    """Secrets must be external regular files owned by this user, mode 0600."""
    p = Path(path).expanduser()
    if not p.is_absolute() or p.is_symlink():
        raise ValueError("Approval secret must be an absolute non-symlink path")
    info = p.stat()
    if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600 or info.st_uid != os.getuid():
        raise ValueError("Approval secret must be owned by current user and mode 0600")
    repo = Path(__file__).resolve().parents[1]
    if p.resolve().is_relative_to(repo):
        raise ValueError("Approval secret must be outside the repository")
    value = p.read_bytes().strip()
    if len(value) < 16:
        raise ValueError("Approval secret is missing or too short")
    return value


def approval_config(config: dict) -> dict:
    values = config.get("approval", {})
    for name in ("spencer_slack_user_id", "slack_channel_id", "receipt_key_path"):
        if not values.get(name) or str(values[name]).startswith(("REPLACE", "TODO", "<")):
            raise ValueError(f"Missing approval.{name}; approvals fail closed")
    return values


def signature(payload: dict, key: bytes) -> str:
    return hmac.new(key, json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(), hashlib.sha256).hexdigest()


def record_event(root: Path, config: dict, raw_body: bytes, slack_timestamp: str, slack_signature: str,
                 now: float | None = None) -> dict:
    """Verify original Slack signed request, then create a Jeeves signed receipt.

    Called only by a bridge holding the original request bytes and Slack headers.
    An arbitrary JSON object naming Spencer is never accepted as authorization.
    """
    settings = approval_config(config)
    if not settings.get("slack_signing_secret_path"):
        raise ValueError("Missing approval.slack_signing_secret_path; Slack authentication is required")
    slack_key = key_bytes(settings["slack_signing_secret_path"])
    receipt_key = key_bytes(settings["receipt_key_path"])
    now = time.time() if now is None else now
    if not re.fullmatch(r"\d{10,12}", slack_timestamp) or abs(now - int(slack_timestamp)) > 300:
        raise ValueError("Expired or invalid Slack request timestamp")
    expected = "v0=" + hmac.new(slack_key, b"v0:" + slack_timestamp.encode() + b":" + raw_body,
                                hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, slack_signature):
        raise ValueError("Invalid Slack request signature")
    envelope = json.loads(raw_body)
    if not isinstance(envelope, dict) or not isinstance(envelope.get("event"), dict):
        raise ValueError("Slack event envelope must be an object")
    event = envelope.get("event", {})
    event_id = envelope.get("event_id", "")
    if envelope.get("type") != "event_callback" or not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", event_id):
        raise ValueError("A Slack event_callback with a valid event_id is required")
    if event.get("type") != "message" or event.get("subtype") or event.get("bot_id") or event.get("bot_profile") or event.get("edited"):
        raise ValueError("Only original human Slack messages can approve pages")
    if event.get("user") != settings["spencer_slack_user_id"] or event.get("channel") != settings["slack_channel_id"]:
        raise ValueError("Slack message does not match configured Spencer and approval channel")
    match = COMMAND.fullmatch(event.get("text", "").strip())
    if not match:
        raise ValueError("Use exactly APPROVE|HOLD|REJECT slug 64-character-draft-digest")
    message_order(event.get("ts"))
    decision, slug, digest = match.groups()
    validate_slug(slug)
    with lock(root, "queue"):
        seen_file = root / "approvals" / "events" / f"{event_id}.json"
        if seen_file.exists():
            raise ValueError("Slack event replay rejected")
        job_path = queued_draft(root, slug)
        job = read_json(job_path)
        if job.get("draft_digest") != digest:
            raise ValueError("Approval digest does not match draft queue")
        verify_draft(root, job)
        payload = {"version": 1, "recorder": "jeeves", "event_id": event_id,
                   "slack_user_id": event["user"], "slack_channel_id": event["channel"],
                   "slack_message_ts": event.get("ts"), "slack_request_ts": slack_timestamp,
                   "decision": decision, "slug": slug, "draft_digest": digest,
                   "recorded_at": utcnow(), "authentication": "slack-v0-hmac"}
        receipt = {"payload": payload, "signature": signature(payload, receipt_key)}
        # Write replay marker first: interruption can lose a receipt, never duplicate one.
        atomic_json(seen_file, {"event_id": event_id, "recorded_at": payload["recorded_at"]})
        atomic_json(root / "approvals" / "inbox" / f"{event_id}.json", receipt)
        return receipt


def message_order(timestamp: object) -> Decimal:
    if not isinstance(timestamp, str) or not re.fullmatch(r"[0-9]{1,12}\.[0-9]{1,9}", timestamp):
        raise ValueError("Original Slack message timestamp is required")
    return Decimal(timestamp)


def queued_draft(root: Path, slug: str) -> Path:
    """Explicit later decisions may revoke or replace any pre-dispatch decision."""
    choices = [root / "queue" / state / f"{slug}.json" for state in ("drafts", "hold", "approved", "rejected")]
    existing = [path for path in choices if path.exists()]
    if len(existing) > 1:
        raise ValueError("Draft appears in multiple queue states; reconcile before approving")
    path = existing[0] if existing else choices[0]
    if path.is_symlink():
        raise ValueError("Symlink queue job forbidden")
    return path


def verify_receipt(config: dict, receipt: dict) -> dict:
    settings = approval_config(config)
    if not isinstance(receipt, dict) or not isinstance(receipt.get("payload"), dict):
        raise ValueError("Jeeves receipt must contain an object payload")
    payload = receipt.get("payload", {})
    expected = signature(payload, key_bytes(settings["receipt_key_path"]))
    if not isinstance(receipt.get("signature"), str) or not hmac.compare_digest(expected, receipt["signature"]):
        raise ValueError("Invalid Jeeves receipt signature")
    if (payload.get("version") != 1 or payload.get("recorder") != "jeeves" or
        payload.get("authentication") != "slack-v0-hmac" or
        payload.get("slack_user_id") != settings["spencer_slack_user_id"] or
        payload.get("slack_channel_id") != settings["slack_channel_id"] or
        payload.get("decision") not in {"APPROVE", "HOLD", "REJECT"}):
        raise ValueError("Jeeves receipt identity or decision is invalid")
    validate_slug(payload.get("slug", ""))
    if not re.fullmatch(r"[a-f0-9]{64}", payload.get("draft_digest", "")):
        raise ValueError("Receipt has invalid digest")
    message_order(payload.get("slack_message_ts"))
    return payload


def verify_draft(root: Path, job: dict) -> Path:
    if not isinstance(job, dict):
        raise ValueError("Queue job must be an object")
    slug = job.get("slug", "")
    validate_slug(slug)
    directory = root / "drafts" / slug
    if directory.is_symlink() or not directory.resolve().is_relative_to((root / "drafts").resolve()):
        raise ValueError("Draft path must remain within pipeline/drafts")
    for filename in ("index.html", "meta.json", "evidence.md", "qa-report.json"):
        if (directory / filename).is_symlink():
            raise ValueError("Symlink draft artifacts are forbidden")
    if job.get("qa_passed") is not True or read_json(directory / "qa-report.json").get("passed") is not True:
        raise ValueError("Draft has not passed QA")
    if draft_digest(directory) != job.get("draft_digest"):
        raise ValueError("Draft changed since QA or approval; regenerate and request new approval")
    return directory


def verify_approval(root: Path, config: dict, job: dict) -> Path:
    if not isinstance(job, dict):
        raise ValueError("Queue job must be an object")
    payload = verify_receipt(config, job.get("approval_receipt", {}))
    if payload["decision"] != "APPROVE" or payload["slug"] != job.get("slug") or payload["draft_digest"] != job.get("draft_digest"):
        raise ValueError("Approval is not bound to this exact draft")
    return verify_draft(root, job)


def sync(root: Path, config: dict, *, _lock_held: bool = False) -> dict:
    root = Path(root)
    result = {"approved": [], "hold": [], "rejected": [], "errors": []}
    try:
        settings = approval_config(config)
        key_bytes(settings["receipt_key_path"])
        if not settings.get("slack_signing_secret_path"):
            raise ValueError("Missing approval.slack_signing_secret_path; Slack bridge is not ready")
        key_bytes(settings["slack_signing_secret_path"])
    except (ValueError, OSError) as exc:
        result["errors"].append({"configuration": "approval", "error": str(exc)})
    with (nullcontext() if _lock_held else lock(root, "queue")):
        # Verify all receipts before applying any. Filename order is not event order.
        grouped = {}
        for source in sorted((root / "approvals" / "inbox").glob("*.json")):
            try:
                if source.is_symlink():
                    raise ValueError("Symlink receipt forbidden")
                receipt = read_json(source)
                payload = verify_receipt(config, receipt)
                grouped.setdefault(payload["slug"], []).append((source, receipt, payload))
            except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
                result["errors"].append({"receipt": source.name, "error": str(exc)})
        restriction = {"APPROVE": 0, "HOLD": 1, "REJECT": 2}
        for slug, entries in sorted(grouped.items()):
            # Equal timestamps fail closed to the most restrictive signed decision.
            entries.sort(key=lambda entry: (message_order(entry[2]["slack_message_ts"]), restriction[entry[2]["decision"]]))
            source, receipt, payload = entries[-1]
            try:
                job_path = queued_draft(root, slug)
                job = read_json(job_path)
                verify_draft(root, job)
                if job.get("slug") != slug or job.get("draft_digest") != payload["draft_digest"]:
                    raise ValueError("Approval does not match current draft")
                current = verify_receipt(config, job["approval_receipt"]) if job.get("approval_receipt") else None
                incoming_order = (message_order(payload["slack_message_ts"]), restriction[payload["decision"]])
                current_order = (message_order(current["slack_message_ts"]), restriction[current["decision"]]) if current else None
                if current_order is None or incoming_order > current_order:
                    dest_state = {"APPROVE": "approved", "HOLD": "hold", "REJECT": "rejected"}[payload["decision"]]
                    dest = root / "queue" / dest_state / f"{slug}.json"
                    if dest.exists() and read_json(dest).get("draft_digest") != payload["draft_digest"]:
                        raise ValueError("Conflicting destination job; manual reconciliation required")
                    job.update({"approval_receipt": receipt, "status": dest_state, "approval_recorded_at": utcnow()})
                    atomic_json(dest, job)
                    if job_path != dest:
                        job_path.unlink()
                    result[dest_state].append(slug)
                # Archive all older receipts only after the latest decision is durable.
                for source, _, _ in entries:
                    processed = root / "approvals" / "processed" / source.name
                    processed.parent.mkdir(parents=True, exist_ok=True)
                    source.replace(processed)
            except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
                result["errors"].append({"receipt": source.name, "error": str(exc)})
        rows = ["# Page approvals", "", "Reply in the configured Slack approval channel with one exact command per message.",
                "Approval binds to the displayed digest. A changed draft requires a new approval.", ""]
        for path in sorted((root / "queue" / "drafts").glob("*.json")):
            try:
                if path.is_symlink():
                    raise ValueError("Symlink queue job forbidden")
                job = read_json(path)
                verify_draft(root, job)
                slug, digest = job["slug"], job["draft_digest"]
                content_post = job.get("kind") == "content_post"
                volume = "not applicable (content post)" if content_post else job.get("estimated_volume")
                if volume is None:
                    volume = "unavailable"
                query_label = "Content topic" if content_post else "Target query"
                outline = job.get("outline", [])
                if isinstance(outline, list):
                    outline = "; ".join(x if isinstance(x, str) else str(x.get("heading", x)) for x in outline)
                query = str(job.get("title", "") if content_post else job.get("target_query", job.get("target-query", ""))).replace("\n", " ")
                rows.extend([f"## {slug}", f"- {query_label}: {query}", f"- Estimated monthly volume (DataForSEO): {volume}",
                             f"- Outline: {str(outline).replace(chr(10), ' ')}", f"- Draft: drafts/{slug}/index.html", "",
                             f"`APPROVE {slug} {digest}`", f"`HOLD {slug} {digest}`", f"`REJECT {slug} {digest}`", ""])
            except (ValueError, OSError, KeyError, TypeError) as exc:
                result["errors"].append({"draft": path.name, "error": str(exc)})
        if len(rows) == 5:
            rows.append("No drafts awaiting approval.")
        root.mkdir(parents=True, exist_ok=True)
        _atomic_text(root / "APPROVALS-TODAY.md", "\n".join(rows) + "\n")
        atomic_json(root / "handoffs" / "jeeves-approvals.json", {
            "kind": "slack_approval_queue", "created_at": utcnow(), "status": "prepared_not_sent",
            "channel_id": config.get("approval", {}).get("slack_channel_id"),
            "markdown_path": str(root / "APPROVALS-TODAY.md"), "requires": "Jeeves Slack bridge and original signed Slack event forwarding",
            "errors": result["errors"]})
    return result


def _atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(text)
    temp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    sub = parser.add_subparsers(dest="command")
    recorder = sub.add_parser("record", help="Jeeves bridge: verify original Slack request and record receipt")
    recorder.add_argument("--event", type=Path, required=True)
    recorder.add_argument("--slack-timestamp", required=True)
    recorder.add_argument("--slack-signature", required=True)
    args = parser.parse_args()
    try:
        config = read_json(args.config)
        result = (record_event(args.root, config, args.event.read_bytes(), args.slack_timestamp, args.slack_signature)
                  if args.command == "record" else sync(args.root, config))
        print(json.dumps(result, indent=2))
        return 1 if result.get("errors") else 0
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
