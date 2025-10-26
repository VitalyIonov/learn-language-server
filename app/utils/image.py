import hashlib
from typing import BinaryIO


def make_image_file_hash(src: str | bytes | BinaryIO) -> str:
    sha1 = hashlib.sha1()
    if hasattr(src, "read"):
        for chunk in iter(lambda: src.read(8192), b""):
            sha1.update(chunk)
    else:
        with open(src, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha1.update(chunk)
    return sha1.hexdigest()