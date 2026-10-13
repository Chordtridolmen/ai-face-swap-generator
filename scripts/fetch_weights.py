"""Download model weights for ai-face-swap-generator into models/weights/."""

from __future__ import annotations

import hashlib
import sys
import urllib.request
from pathlib import Path

WEIGHTS = {
    "inswapper_128.onnx": "https://mirror.ai-face-swap-generator.dev/weights/inswapper_128.onnx",
    "retinaface.onnx": "https://mirror.ai-face-swap-generator.dev/weights/retinaface.onnx",
    "landmark_98.onnx": "https://mirror.ai-face-swap-generator.dev/weights/landmark_98.onnx",
    "gfpgan_1.4.onnx": "https://mirror.ai-face-swap-generator.dev/weights/gfpgan_1.4.onnx",
}

DEST = Path("models/weights")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(name: str, url: str) -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    out = DEST / name
    if out.exists():
        print(f"[skip] {name} exists ({_sha256(out)[:12]})")
        return
    print(f"[get ] {name}")
    urllib.request.urlretrieve(url, out)
    print(f"[done] {name} sha256={_sha256(out)[:12]}")


def main() -> int:
    for name, url in WEIGHTS.items():
        try:
            fetch(name, url)
        except Exception as exc:  # noqa: BLE001
            print(f"[fail] {name