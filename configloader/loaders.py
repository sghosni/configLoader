import os
import glob
from configparser import ConfigParser
from typing import Dict, List
from pydantic import BaseModel, ValidationError


class ConfigLoader:
    def __init__(self, config_dir: str, active_models: List[BaseModel]):
        self.config_dir = config_dir
        self.configs: Dict = {}
        self.active_models = active_models
        self.active_sections = {}
        for active_model in self.active_models:
            self.active_sections[active_model.config_section_name] = active_model

    def load_config(self, config_file: str):
        config = ConfigParser()
        config.read(config_file)
        for active_section in self.active_sections:
            if active_section in config:
                try:
                    app_config = self.active_sections[active_section](
                        **config[active_section]
                    )
                    self.configs[app_config.config_section_name] = app_config
                except KeyError as e:
                    raise Exception(f"Missing key: {e}")
                except (ValidationError, TypeError) as e:
                    raise Exception(f"Validation or type error: {e}")

    def load_configs(self):
        config_files = glob.glob(os.path.join(self.config_dir, "*.cfg"))
        for config_file in config_files:
            self.load_config(config_file)
        parsed_configs = set(self.configs.keys())
        desired_configs = set(self.active_sections)
        missing_configs = list(desired_configs.difference(parsed_configs))
        if len(missing_configs) > 0:
            raise Exception(
                "These config sections are missing in config files: "
                + str(missing_configs)
            )

    def get_config(self, section: str):
        return self.configs.get(section)
