from typing import ClassVar, Optional
from pydantic import Field
from configloader import ConfigSection


class RedisConfig(ConfigSection):
    config_section_name: ClassVar[str] = "redis"

    host: str = "localhost"
    port: int = Field(default=6379, ge=0, le=65535)
    db: int = Field(default=0, ge=0)
    password: Optional[str] = None
