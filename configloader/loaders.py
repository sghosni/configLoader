import os
import glob
from configparser import ConfigParser
from typing import Dict, List
from pydantic import BaseModel, ValidationError


class ConfigLoader:
    def __init__(self, config_dir: str, active_models: List[BaseModel], ignore_missing: bool = False):
        self.config_dir = config_dir
        self.configs: Dict = {}
        self.active_models = active_models
        self.active_sections = {}
        self.ignore_missing = ignore_missing
        for active_model in self.active_models:
            self.active_sections[active_model.config_section_name] = active_model

    def load_config(self, config_file: str):
        '''Load a single config file and validate it against the active models.'''
        config = ConfigParser()
        config.read(config_file)
        for active_section, model in self.active_sections.items():
            if config.has_section(active_section):
                try:
                    section_data = {k: v for k, v in config.items(active_section)}
                    app_config = model(**section_data)
                    self.configs[active_section] = app_config
                except KeyError as e:
                    raise KeyError(f"Missing key: {e}")
                except (ValidationError, TypeError) as e:
                    raise ValueError(f"Validation or type error: {e}")

    def load_configs(self):
        '''Load all config files and validate them against the active models.'''
        config_files = glob.glob(os.path.join(self.config_dir, "*.cfg"))
        for config_file in config_files:
            self.load_config(config_file)
        parsed_configs = set(self.configs.keys())
        desired_configs = set(self.active_sections)
        missing_configs = list(desired_configs.difference(parsed_configs))
        if len(missing_configs) > 0 and not self.ignore_missing:
            raise Exception(
                "These config sections are missing in config files: "
                + str(missing_configs)
            )

    def get_config(self, section: str):
        '''Get a single config section.'''
        return self.configs.get(section)
