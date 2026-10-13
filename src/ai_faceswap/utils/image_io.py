"""Image io — Windows-safe paths, EXIF-normalized loads, atomic saves."""

from __future__ import annotations

import os
from pathlib import Path

import cv2
import numpy as np


def load_image(path: Path) -> np.ndarray:
    frame = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if frame is None:
        raise IOError(f"ai-face-swap-generator: cannot read image {path}")
    return frame


def save_image(path: Path, frame: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    cv2.imwrite(str(tmp), frame)
    os.replace(tmp, path)