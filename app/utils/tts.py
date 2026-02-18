import hashlib, json

from app.utils.string import normalize_text

def make_tts_hash(text: str) -> str:
    payload = {
        "text": normalize_text(text),
    }
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha1(raw).hexdigest()