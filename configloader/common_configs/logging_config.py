from typing import ClassVar, Optional
from configloader import ConfigSection, ConfigEnum


class LoggingConfig(ConfigSection):
    config_section_name: ClassVar[str] = "logging"

    level: ConfigEnum = ConfigEnum("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    log_to_file: bool = False
    log_file_path: Optional[str] = "logs/app.log"
