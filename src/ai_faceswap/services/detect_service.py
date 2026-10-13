"""DetectService — wraps the configured face detector backend."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from ai_faceswap.models.detector_model import DetectorModel
from ai_faceswap.utils.image_io import load_image


class DetectService:
    def __init__(self, max_faces: int = 4, threshold: float = 0.62) -> None:
        self.model = DetectorModel(threshold=threshold)
        self.max_faces = max_faces

    def detect(self, image: Path) -> tuple[list[tuple[int, int, int, int]], list[float]]:
        frame = load_image(image)
        return self._detect_array(frame)

    def _detect_array(
        self, frame: np.ndarray
    ) -> tuple[list[tuple[int, int, int, int]], list[float]]:
        boxes, scores = self.model.infer(frame)
        order = np.argsort(scores)[::-1][: self.max_faces]
        return [tuple(int(v) for v in boxes[i]) for i in order], [float(scores[i]) for i in order]