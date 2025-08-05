from typing import ClassVar, Optional
from pydantic import Field
from configloader import ConfigSection

class HTTPServerConfig(ConfigSection):
    config_section_name: ClassVar[str] = "http_server"

    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=0, le=65535)
    workers: Optional[int] = 1
    ssl_enabled: bool = False
    ssl_cert_path: Optional[str] = None
    ssl_key_path: Optional[str] = None
