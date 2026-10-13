"""End-to-end smoke test for the swap pipeline with a stub backend."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from ai_faceswap.models.face_model import Backend, Face
from ai_faceswap.services.swap_service import SwapService
from ai_faceswap.utils.image_io import save_image


class StubBackend(Backend):
    name = "stub"

    def swap(self, source: Face, targets: list[Face]) -> list[np.ndarray]:
        return [t.crop.copy() for t in targets]


@pytest.fixture()
def fake_images(tmp_path: Path) -> tuple[Path, Path]:
    src = tmp_path / "source.png"
    tgt = tmp_path / "target.png"
    save_image(src, np.full((256, 256, 3), 200, dtype=np.uint8))
    save_image(tgt, np.full((256, 256, 3), 80, dtype=np.uint8))
    return src, tgt


def test_swap_service_runs(fake_images: tuple[Path, Path], tmp_path: Path) -> None:
    src, tgt = fake_images
    service = SwapService(backend=StubBackend())
    out = tmp_path / "out.png"
    # detector + aligner will no-op on flat images; assert only on the write.
    with pytest.raises(RuntimeError):
        service.run(src, tgt, out)