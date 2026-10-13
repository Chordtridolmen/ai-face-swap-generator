"""Pydantic schema mirroring config/default.yaml — validated on boot."""

from __future__ import annotations

from pydantic import BaseModel, Field


class DeviceCfg(BaseModel):
    prefer: str = "cuda"
    fp16: bool = True


class DetectorCfg(BaseModel):
    backend: str = "retinaface"
    score_threshold: float = 0.62
    max_faces: int = 4


class SwapperCfg(BaseModel):
    backend: str = "inswapper"
    model: str = "models/weights/inswapper_128.onnx"
    blend_alpha: float = 0.85
    restore_face: bool = True


class RootCfg(BaseModel):
    device: DeviceCfg = Field(default_factory=DeviceCfg)
    detector: DetectorCfg = Field(default_factory=DetectorCfg)
    swapper: SwapperCfg = Field(default_factory=SwapperCfg)