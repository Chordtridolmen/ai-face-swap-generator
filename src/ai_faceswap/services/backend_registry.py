"""Backend registry — resolves a backend name to a loaded Backend adapter."""

from __future__ import annotations

from ai_faceswap.models.face_model import Backend
from ai_faceswap.adapters.inswapper_adapter import InSwapperAdapter
from ai_faceswap.adapters.simswap_adapter import SimSwapAdapter

_REGISTRY: dict[str, type[Backend]] = {
    "inswapper": InSwapperAdapter,
    "simswap": SimSwapAdapter,
}


def get_backend(name: str) -> Backend:
    try:
        cls = _REGISTRY[name.lower()]
    except KeyError as exc:
        raise KeyError(f"unknown backend {name!r}; try one of {sorted(_REGISTRY)}") from exc
    return cls()


def list_backends() -> list[str]:
    return sorted(_REGISTRY)