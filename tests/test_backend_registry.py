"""Verify backend registry resolves names and rejects unknown ones."""

from __future__ import annotations

import pytest

from ai_faceswap.services.backend_registry import get_backend, list_backends


def test_registry_lists_known_backends() -> None:
    names = list_backends()
    assert "inswapper" in names
    assert "simswap" in names


def test_registry_rejects_unknown() -> None:
    with pytest.raises(KeyError):
        get_backend("does-not-exist")