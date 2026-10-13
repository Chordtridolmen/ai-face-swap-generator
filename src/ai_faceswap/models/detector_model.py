"""DetectorModel — onnxruntime wrapper for the configured face detector."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import onnxruntime as ort


class DetectorModel:
    def __init__(
        self,
        model_path: Path = Path("models/weights/retinaface.onnx"),
        threshold: float = 0.62,
        providers: list[str] | None = None,
    ) -> None:
        self.threshold = threshold
        self.session = ort.InferenceSession(
            str(model_path),
            providers=providers or ["CUDAExecutionProvider", "CPUExecutionProvider"],
        )
        self.input_name = self.session.get_inputs()[0].name

    def infer(self, frame: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        blob = frame.astype(np.float32)[None, ...]
        outs = self.session.run(None, {self.input_name: blob})
        boxes = outs[0].reshape(-1, 4)
        scores = outs[1].reshape(-1)
        keep = scores >= self.threshold
        return boxes[keep], scores[keep]