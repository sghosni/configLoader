import os
import glob
import logging
from configparser import ConfigParser
from typing import Dict, List, Type, Optional
from pydantic import BaseModel, ValidationError

from .exceptions import MissingSectionError, ConfigValidationError

logger = logging.getLogger("configloader")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)
logger.handlers = [console_handler]


class ConfigLoader:
    def __init__(
        self,
        config_dir: str,
        active_models: List[Type[BaseModel]],
        ignore_missing: bool = False,
    ):
        self.config_dir = config_dir
        self.ignore_missing = ignore_missing

        self._models: Dict[str, Type[BaseModel]] = {}
        for model in active_models:
            if not hasattr(model, "config_section_name"):
                raise AttributeError(
                    f"Model {model.__name__} is missing required attribute 'config_section_name'"
                )
            section = getattr(model, "config_section_name")
            self._models[section] = model

        self._configs: Dict[str, BaseModel] = {}

    def load_config(self, config_file: str) -> None:
        """Load and validate a single .cfg file."""
        logger.info(f"Loading config file: {config_file}")
        parser = ConfigParser()
        parser.read(config_file)

        for section, model in self._models.items():
            if parser.has_section(section):
                try:
                    data = dict(parser.items(section))
                    self._configs[section] = model(**data)
                    logger.info(f"✔ Loaded section: [{section}]")
                except KeyError as e:
                    raise KeyError(f"Missing key in section [{section}]: {e}")
                except (ValidationError, TypeError) as e:
                    raise ConfigValidationError(
                        f"Validation error in section [{section}]: {e}"
                    )

    def load_configs(self) -> None:
        """Load and validate all .cfg files in the config directory."""
        logger.info(f"Scanning directory for config files: {self.config_dir}")
        config_files = glob.glob(os.path.join(self.config_dir, "*.cfg"))

        if not config_files:
            logger.warning("No config files found.")

        for file in config_files:
            self.load_config(file)

        loaded_sections = set(self._configs.keys())
        expected_sections = set(self._models.keys())
        missing_sections = expected_sections - loaded_sections

        if missing_sections and not self.ignore_missing:
            raise MissingSectionError(
                f"Missing required config sections: {sorted(missing_sections)}"
            )

    def get_config(self, section: str) -> Optional[BaseModel]:
        """Retrieve a parsed config model for a given section name."""
        return self._configs.get(section)
