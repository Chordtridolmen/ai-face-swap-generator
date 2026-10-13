"""Swap handler — validates input, calls SwapService, returns a typed result."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from ai_faceswap.services.swap_service import SwapService
from ai_faceswap.services.backend_registry import get_backend


class SwapRequest(BaseModel):
    source: Path
    target: Path
    out: Path
    backend: str = "inswapper"


class SwapResult(BaseModel):
    output_path: Path
    frames: int
    backend: str


def handle_swap(req: SwapRequest) -> SwapResult:
    if not req.source.exists():
        raise FileNotFoundError(f"source face not found: {req.source}")
    if not req.target.exists():
        raise FileNotFoundError(f"target not found: {req.target}")

    backend = get_backend(req.backend)
    service = SwapService(backend=backend)
    frames = service.run(req.source, req.target, req.out)
    return SwapResult(output_path=req.out, frames=frames, backend=req.backend)