import os
import glob
import logging
from configparser import ConfigParser
from typing import Dict, List, Type, TypeVar
from .section import ConfigSection
from .exceptions import ConfigLoaderError, ConfigValidationError, MissingSectionError


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

T = TypeVar("T", bound=ConfigSection)

class ConfigLoader:
    def __init__(self, config_dir: str, active_models: List[Type[ConfigSection]], ignore_missing: bool = False):
        self.config_dir = config_dir
        self.ignore_missing = ignore_missing
        self.configs: Dict[str, ConfigSection] = {}
        self.active_sections: Dict[str, Type[ConfigSection]] = {}

        for model in active_models:
            section_name = model.config_section_name
            self.active_sections[section_name] = model
            logger.debug(f"Registered config section: {section_name} -> {model.__name__}")

    def load_config(self, config_file: str):
        """Load and parse a single config file."""
        logger.info(f"Loading config file: {config_file}")
        config = ConfigParser()
        config.read(config_file)

        for section_name, model_cls in self.active_sections.items():
            if config.has_section(section_name):
                section_data = dict(config.items(section_name))
                try:
                    validated = model_cls(**section_data)
                    self.configs[section_name] = validated
                    logger.info(f"Loaded section [{section_name}] from {os.path.basename(config_file)}")
                except Exception as e:
                    raise ConfigValidationError(section_name, str(e))

    def load_configs(self):
        """Load and parse all *.cfg files in the config directory."""
        logger.info(f"Scanning config directory: {self.config_dir}")
        config_files = glob.glob(os.path.join(self.config_dir, "*.cfg"))

        for file in config_files:
            self.load_config(file)

        parsed_sections = set(self.configs.keys())
        required_sections = set(self.active_sections.keys())
        missing = required_sections - parsed_sections

        if missing and not self.ignore_missing:
            raise MissingSectionError(list(missing))

    def _get_config(self, section_name: str) -> ConfigSection:
        """Private raw getter by section name."""
        if section_name not in self.configs:
            raise ConfigLoaderError(f"Config section '{section_name}' not found.")
        return self.configs[section_name]

    def get_config(self, model: Type[T]) -> T:
        """Public typed getter by model class."""
        section_name = model.config_section_name
        config = self._get_config(section_name)
        if not isinstance(config, model):
            raise ConfigLoaderError(f"Config section '{section_name}' is not of type {model.__name__}")
        return config