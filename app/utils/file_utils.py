import re


def safe_filename(filename: str) -> str:
    cleaned = filename.replace("\\", "_").replace("/", "_").strip()
    cleaned = re.sub(r"[^A-Za-z0-9._ -]", "_", cleaned)
    cleaned = re.sub(r"\s+", "_", cleaned)
    cleaned = cleaned.lstrip(".")
    return cleaned or "document"
