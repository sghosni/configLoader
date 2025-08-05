from typing import ClassVar
from configloader import ConfigSection, ConfigEnum


class AppConfig(ConfigSection):
    config_section_name: ClassVar[str] = "app"

    name: str = "MyApp"
    version: str = "0.1.0"
    environment: ConfigEnum = ConfigEnum("development", "staging", "production")
    debug: bool = False
