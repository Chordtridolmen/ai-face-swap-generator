"""Device probe — pick cuda / dml / cpu based on available runtimes."""

from __future__ import annotations

import logging

import onnxruntime as ort

log = logging.getLogger(__name__)


def pick_device(prefer: str = "cuda") -> str:
    available = set(ort.get_available_providers())
    order = {
        "cuda": ["CUDAExecutionProvider", "DmlExecutionProvider", "CPUExecutionProvider"],
        "dml": ["DmlExecutionProvider", "CPUExecutionProvider"],
        "cpu": ["CPUExecutionProvider"],
    }.get(prefer.lower(), ["CPUExecutionProvider"])

    for provider in order:
        if provider in available:
            log.info("ai-face-swap-generator using %s", provider)
            return provider
    return "CPUExecutionProvider"