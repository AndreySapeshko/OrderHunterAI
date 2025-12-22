import hashlib


def compute_content_hash(title: str, content: str) -> str:
    base = (title + content[:500]).encode("utf-8")
    return hashlib.sha256(base).hexdigest()
