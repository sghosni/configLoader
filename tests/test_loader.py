# tests/test_loader.py

from configloader.exceptions import ConfigValidationError, MissingSectionError
import pytest
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, Field

from configloader import ConfigLoader


class DummyConfig(BaseModel):
    config_section_name: ClassVar[str] = "dummy"
    host: str
    port: int = Field(..., ge=0, le=65535)


def write_cfg(path: Path, content: str):
    path.write_text(content.strip())


def test_load_valid_config(tmp_path):
    cfg = """
    [dummy]
    host = 127.0.0.1
    port = 8080
    """
    cfg_file = tmp_path / "dummy.cfg"
    write_cfg(cfg_file, cfg)

    loader = ConfigLoader(str(tmp_path), [DummyConfig])
    loader.load_configs()

    config = loader.get_config("dummy")
    assert config.host == "127.0.0.1"
    assert config.port == 8080


def test_missing_section_raises_exception(tmp_path):
    cfg = """
    [wrongsection]
    host = localhost
    port = 9000
    """
    cfg_file = tmp_path / "dummy.cfg"
    write_cfg(cfg_file, cfg)

    loader = ConfigLoader(str(tmp_path), [DummyConfig])
    with pytest.raises(MissingSectionError, match="Missing required config sections:"):
        loader.load_configs()


def test_validation_error(tmp_path):
    cfg = """
    [dummy]
    host = localhost
    port = not-a-number
    """
    cfg_file = tmp_path / "dummy.cfg"
    write_cfg(cfg_file, cfg)

    loader = ConfigLoader(str(tmp_path), [DummyConfig], ignore_missing=True)
    with pytest.raises(ConfigValidationError, match="Validation error in section"):
        loader.load_configs()


def test_ignore_missing_passes(tmp_path):
    # No config file present
    loader = ConfigLoader(str(tmp_path), [DummyConfig], ignore_missing=True)
    loader.load_configs()
    assert loader.get_config("dummy") is None
