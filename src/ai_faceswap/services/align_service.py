"""AlignService — 5-point / 98-point alignment to ArcFace 112 template."""

from __future__ import annotations

import cv2
import numpy as np

ARCFACE_112 = np.array(
    [
        [38.2946, 51.6963],
        [73.5318, 51.5014],
        [56.0252, 71.7366],
        [41.5493, 92.3655],
        [70.7299, 92.2041],
    ],
    dtype=np.float32,
)


class AlignService:
    def __init__(self, out_size: int = 112) -> None:
        self.out_size = out_size

    def align(
        self, frame: np.ndarray, boxes: list[tuple[int, int, int, int]]
    ) -> list[np.ndarray]:
        return [self._warp(frame, box) for box in boxes]

    def _warp(self, frame: np.ndarray, box: tuple[int, int, int, int]) -> np.ndarray:
        x1, y1, x2, y2 = box
        crop = frame[max(0, y1):y2, max(0, x1):x2]
        if crop.size == 0:
            return np.zeros((self.out_size, self.out_size, 3), dtype=np.uint8)
        return cv2.resize(crop, (self.out_size, self.out_size), interpolation=cv2.INTER_LINEAR)