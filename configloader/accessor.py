from typing import Dict
from .base import ConfigSection


class ConfigAccessor:
    def __init__(self, configs: Dict[str, ConfigSection]):
        self._sections = {
            self._normalize_key(k): v for k, v in configs.items()
        }

    def _normalize_key(self, key: str) -> str:
        return key.lower()

    def __getattr__(self, key: str) -> ConfigSection:
        if key in self._sections:
            return self._sections[key]
        raise AttributeError(f"No such config section: '{key}'")

    def __dir__(self):
        return list(self._sections.keys())

    def to_dict(self) -> Dict[str, dict]:
        """Convert all config sections to plain dicts."""
        return {
            name: section.model_dump() for name, section in self._sections.items()
        }
