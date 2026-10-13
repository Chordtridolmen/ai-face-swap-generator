"""InSwapperAdapter — inswapper_128.onnx face swap backend."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import onnxruntime as ort

from ai_faceswap.models.face_model import Backend, Face


class InSwapperAdapter(Backend):
    name = "inswapper"

    def __init__(self, model_path: Path = Path("models/weights/inswapper_128.onnx")) -> None:
        self.session = ort.InferenceSession(
            str(model_path),
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
        )
        self.inputs = [i.name for i in self.session.get_inputs()]

    def swap(self, source: Face, targets: list[Face]) -> list[np.ndarray]:
        src = source.crop.astype(np.float32)[None, ...] / 255.0
        out: list[np.ndarray] = []
        for tgt in targets:
            t = tgt.crop.astype(np.float32)[None, ...] / 255.0
            res = self.session.run(None, {self.inputs[0]: src, self.inputs[1]: t})[0]
            out.append(np.clip(res[0] * 255.0, 0, 255).astype(np.uint8))
        return out