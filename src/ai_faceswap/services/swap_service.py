"""SwapService — orchestrates detect → align → swap → restore → render."""

from __future__ import annotations

import logging
from pathlib import Path

from ai_faceswap.models.face_model import Backend
from ai_faceswap.services.align_service import AlignService
from ai_faceswap.services.detect_service import DetectService
from ai_faceswap.services.render_service import RenderService
from ai_faceswap.utils.image_io import load_image, save_image

log = logging.getLogger(__name__)


class SwapService:
    def __init__(self, backend: Backend) -> None:
        self.backend = backend
        self.detector = DetectService(max_faces=4)
        self.aligner = AlignService()
        self.renderer = RenderService()

    def run(self, source: Path, target: Path, out: Path) -> int:
        src_img = load_image(source)
        tgt_img = load_image(target)

        src_faces = self.aligner.align(src_img, self.detector.detect(source)[0])
        tgt_boxes, _ = self.detector.detect(target)
        tgt_faces = self.aligner.align(tgt_img, tgt_boxes)

        if not src_faces or not tgt_faces:
            raise RuntimeError("ai-face-swap-generator: no face found to swap")

        swapped = self.backend.swap(src_faces[0], tgt_faces)
        composed = self.renderer.compose(tgt_img, swapped, tgt_boxes)
        save_image(out, composed)
        log.info("swap complete -> %s", out)
        return len(tgt_faces)