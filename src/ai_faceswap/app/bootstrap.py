"""Bootstrap: resolve config, probe device, wire services, hand to handler."""

from __future__ import annotations

import logging
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from ai_faceswap.app.cli import run_pipeline
from ai_faceswap.utils.device_probe import pick_device


class AppConfig(BaseModel):
    device_prefer: str = Field(default="cuda")
    fp16: bool = True
    log_level: str = "INFO"
    config_path: Path = Path("config/default.yaml")


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def boot(config_path: str = "config/default.yaml") -> int:
    cfg = load_config(Path(config_path))
    configure_logging(cfg.get("app", {}).get("log_level", "INFO"))
    device = pick_device(cfg.get("device", {}).get("prefer", "cuda"))
    logging.getLogger(__name__).info("device selected: %s", device)
    return run_pipeline(cfg)