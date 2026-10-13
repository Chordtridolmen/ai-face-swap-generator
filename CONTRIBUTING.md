# Contributing to ai-face-swap-generator

Thanks for wanting to push pixels around. This is a hobbyist / research
project for real-time and offline AI face swapping on Windows desktops.
We keep the codebase small, typed, and boring — swap the faces, not the
architecture.

## Ground rules

- Python 3.11+ on Windows 10/11 x64. CUDA 12.x optional but strongly
  recommended.
- Every PR must pass `pytest tests/` and `ruff check .` locally before
  opening. CI runs the same.
- No binary model weights in-tree. Weights are pulled by
  `scripts/fetch_weights.py` from the release mirror and live under
  `models/weights/`. That path is gitignored on purpose.
- Type hints everywhere in `services/` and `models/`. Handlers may stay
  loose but must return typed response objects.

## Repo layout

```
src/ai_faceswap/
  app/            entry + bootstrap
  handlers/       thin request/response glue
  services/       business logic (swap, detect, align, render)
  models/         dataclasses + onnx runtime wrappers
  adapters/       platform + native bindings (cpp / csharp / java)
  utils/          image io, timing, device probes
config/           yaml + json runtime config
tests/            pytest suite
scripts/          dev tooling
native/           optional native accel modules
```

## Adding a new backend

1. Drop a new adapter under `src/ai_faceswap/adapters/`.
2. Register it in `services/backend_registry.py`.
3. Add a smoke test in `tests/test_backends.py`.

## Commit style

`area: short imperative` — e.g. `swap: cache aligned faces by hash`,
`adapter/cpp: fix cuda stream sync on exit`.

## Reporting bugs

Open an issue with: Windows build number, GPU + driver, python version,
the exact command you ran, and the tail of `logs/faceswap.log`.