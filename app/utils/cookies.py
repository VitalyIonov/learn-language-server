from fastapi import Request


def build_interface_lang_cookie(lang: str, *, request: Request) -> dict:
    cookie = {
        "key": "interface_lang",
        "value": lang,
        "max_age": 60 * 60 * 24 * 365,
        "path": "/",
        "httponly": True,
        "samesite": "lax",
        "secure": request.url.scheme == "https",
    }
    host = request.url.hostname or ""
    if host.endswith("learn-language.es"):
        cookie["domain"] = ".learn-language.es"
    return cookie
