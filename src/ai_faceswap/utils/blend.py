"""Blend utilities — poisson + alpha blending for face compositing."""

from __future__ import annotations

import cv2
import numpy as np


def poisson_blend(
    background: np.ndarray, foreground: np.ndarray, alpha: float = 0.85
) -> np.ndarray:
    if background.shape != foreground.shape:
        foreground = cv2.resize(
            foreground, (background.shape[1], background.shape[0]), interpolation=cv2.INTER_LINEAR
        )
    h, w = background.shape[:2]
    mask = np.full((h, w), 255, dtype=np.uint8)
    center = (w // 2, h // 2)
    try:
        mixed = cv2.seamlessClone(foreground, background, mask, center, cv2.NORMAL_CLONE)
        return cv2.addWeighted(mixed, alpha, background, 1.0 - alpha, 0.0)
    except cv2.error:
        return cv2.addWeighted(foreground, alpha, background, 1.0 - alpha, 0.0)