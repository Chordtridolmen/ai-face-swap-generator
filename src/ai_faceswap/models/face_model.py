"""Core face abstractions shared across services and adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np


@dataclass(slots=True)
class Face:
    crop: np.ndarray
    box: tuple[int, int, int, int]
    landmarks: np.ndarray | None = None
    embedding: np.ndarray | None = None


@dataclass(slots=True)
class SwapTrace:
    backend: str
    frames: int = 0
    warnings: list[str] = field(default_factory=list)


class Backend(ABC):
    name: str = "base"

    @abstractmethod
    def swap(self, source: Face, targets: list[Face]) -> list[np.ndarray]:
        """Return swapped crops aligned to each target face box."""