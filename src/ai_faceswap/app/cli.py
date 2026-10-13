"""Typer CLI — the faceswap entry point exposed in pyproject scripts."""

from __future__ import annotations

from pathlib import Path

import typer

from ai_faceswap.handlers.swap_handler import SwapRequest, handle_swap
from ai_faceswap.handlers.detect_handler import DetectRequest, handle_detect

app = typer.Typer(help="ai-face-swap-generator CLI")


@app.command("swap")
def swap_cmd(
    source: Path = typer.Option(..., "--source", "-s", help="source face image"),
    target: Path = typer.Option(..., "--target", "-t", help="target image or video"),
    out: Path = typer.Option(Path("out.mp4"), "--out", "-o"),
    backend: str = typer.Option("inswapper", "--backend"),
) -> None:
    req = SwapRequest(source=source, target=target, out=out, backend=backend)
    result = handle_swap(req)
    typer.echo(f"[ai-face-swap-generator] wrote {result.output_path} ({result.frames} frames)")


@app.command("detect")
def detect_cmd(
    image: Path = typer.Option(..., "--image", "-i"),
) -> None:
    req = DetectRequest(image=image)
    res = handle_detect(req)
    typer.echo(f"detected {len(res.boxes)} faces in {image}")


def run_pipeline(cfg: dict) -> int:
    """Headless pipeline invoked by bootstrap when no subcommand is given."""
    return 0


def main() -> None:
    app()


if __name__ == "__main__":
    main()