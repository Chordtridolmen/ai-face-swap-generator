"""WatermarkService — stamps a configurable text or hash onto output frames."""

from __future__ import annotations

import cv2
import numpy as np


class WatermarkService:
    def __init__(self, text: str = "ai-face-swap-generator", enabled: bool = True) -> None:
        self.text = text
        self.enabled = enabled

    def apply(self, frame: np.ndarray) -> np.ndarray:
        if not self.enabled:
            return frame
        h, _ = frame.shape[:2]
        cv2.putText(
            frame,
            self.text,
            (12, h - 16),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (235, 235, 235),
            1,
            cv2.LINE_AA,
        )
        return frame