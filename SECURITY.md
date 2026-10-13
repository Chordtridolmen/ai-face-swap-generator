# Security Policy — ai-face-swap-generator

## Scope

This project processes user-supplied images and video locally. It does
not phone home, does not upload frames, and does not ship telemetry.
Anything that changes that contract is a security issue.

## Reporting

Email: security@ai-face-swap-generator.dev (PGP key in `keys/`).
Please do not open public issues for memory-safety or RCE-class bugs.
We aim to acknowledge within 72 hours.

## Threat model

- Malicious image / video input (parser bugs in `utils/image_io.py`).
- Untrusted ONNX models dropped into `models/weights/` (we validate
  graph ops against an allowlist in `models/onnx_guard.py`).
- Native adapter boundary (cpp/csharp/java) — treat as hostile, fuzz
  the JNI/CLR/P-Invoke entry points.
- Local file write races under `cache/`.

## Out of scope

- Misuse of the tool to impersonate people. That is a user policy
  problem, not a code vulnerability. We ship a watermarking hook in
  `services/watermark_service.py` and leave enforcement to you.
- Anything requiring physical access to the machine.

## Supported versions

Only the latest minor release on `main` receives fixes.