"""SimSwapAdapter — alternative backend, same Backend interface."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import onnxruntime as ort

from ai_faceswap.models.face_model import Backend, Face


class SimSwapAdapter(Backend):
    name = "simswap"

    def __init__(self, model_path: Path = Path("models/weights/simswap_512.onnx")) -> None:
        self.session = ort.InferenceSession(
            str(model_path),
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
        )
        self.input_name = self.session.get_inputs()[0].name

    def swap(self, source: Face, targets: list[Face]) -> list[np.ndarray]:
        src = source.crop.astype(np.float32)[None, ...] / 255.0
        blended: list[np.ndarray] = []
        for tgt in targets:
            t = tgt.crop.astype(np.float32)[None, ...] / 255.0
            res = self.session.run(None, {self.input_name: np.concatenate([src, t], axis=-1)})[0]
            blended.append(np.clip(res[0] * 255.0, 0, 255).astype(np.uint8))
        return blended