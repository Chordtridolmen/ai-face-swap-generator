"""RenderService — composite swapped faces back onto the target frame."""

from __future__ import annotations

import numpy as np

from ai_faceswap.utils.blend import poisson_blend


class RenderService:
    def __init__(self, alpha: float = 0.85) -> None:
        self.alpha = alpha

    def compose(
        self,
        target: np.ndarray,
        swapped_faces: list[np.ndarray],
        boxes: list[tuple[int, int, int, int]],
    ) -> np.ndarray:
        canvas = target.copy()
        for face, box in zip(swapped_faces, boxes):
            x1, y1, x2, y2 = box
            region = canvas[y1:y2, x1:x2]
            if region.shape[:2] != face.shape[:2]:
                continue
            canvas[y1:y2, x1:x2] = poisson_blend(region, face, alpha=self.alpha)
        return canvas