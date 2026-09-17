"""Filesystem primitives shared by the local, approval-gated pipeline."""
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

REPO = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = REPO / "pipeline"


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def read_json(path):
    return json.loads(Path(path).read_text())


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".tmp-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def validate_slug(slug):
    if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or len(slug) > 100:
        raise ValueError("Invalid slug")
    return slug


@contextmanager
def lock(root, name):
    validate_slug(name)
    directory = Path(root) / ".locks"
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / (name + ".lock")).open("a+") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def draft_digest(directory):
    digest = hashlib.sha256()
    for name in ("index.html", "meta.json", "evidence.md"):
        path = Path(directory) / name
        if path.is_symlink():
            raise ValueError("Symlink draft artifact forbidden")
        digest.update(name.encode() + b"\0" + path.read_bytes() + b"\0")
    return digest.hexdigest()


def fresh(timestamp, days=7):
    try:
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(timestamp.replace("Z", "+00:00"))).total_seconds()
        return 0 <= age <= days * 86400
    except (ValueError, TypeError, AttributeError):
        return False
