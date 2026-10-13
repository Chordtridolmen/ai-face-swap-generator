"""Detect handler — returns face boxes without touching swap logic."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from ai_faceswap.services.detect_service import DetectService


class DetectRequest(BaseModel):
    image: Path
    max_faces: int = 4


class DetectResult(BaseModel):
    boxes: list[tuple[int, int, int, int]]
    scores: list[float]


def handle_detect(req: DetectRequest) -> DetectResult:
    service = DetectService(max_faces=req.max_faces)
    boxes, scores = service.detect(req.image)
    return DetectResult(boxes=boxes, scores=scores)