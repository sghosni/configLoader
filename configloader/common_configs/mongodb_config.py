from typing import ClassVar, Optional
from configloader import ConfigSection


class MongoDBConfig(ConfigSection):
    config_section_name: ClassVar[str] = "mongodb"

    uri: str = "mongodb://localhost:27017"
    db_name: str
    user: Optional[str] = None
    password: Optional[str] = None
    replica_set: Optional[str] = None
    tls: bool = False
    auth_source: Optional[str] = None
