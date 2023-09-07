### Quick Start

Sample App Directory Hierarchy
```
my_app/
├── configs/
│   └── app_config.cfg
├── config_models/
│   └── app_config_models.py
└── main.py
```

app_config.cfg
```
[GENERAL]
app_name = sample_app
version = 1.0
development = False

[DB_CONFIG]
db_server = 127.0.0.1
db_port = 3306
db_username = root
db_password = toor
```

app_config_models.py
```python
from typing import ClassVar
from pydantic import BaseModel, Field, field_validator, validator
from ipaddress import IPv4Address


class general_config(BaseModel):
    config_section_name: ClassVar[str] = "GENERAL"
    app_name: str
    version: float
    development: bool

    # NOTE: if you want to use field_validator you should upgrade to pydantic 2.x
    @field_validator("version")
    @classmethod
    def name_must_contain_space(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("ensure this value is greater than 0")
        return v


class database_config(BaseModel):
    config_section_name: ClassVar[str] = "DB_CONFIG"
    db_server: IPv4Address
    db_port: int = Field(None, gt=0, le=65535)
    db_username: str
    db_password: str
```
main.py
```python
from configloader.loaders import ConfigLoader

if __name__ == "__main__":
    config_loader = ConfigLoader(
        config_dir="configs", active_models=[general_config, database_config]
    )
    config_loader.load_configs()
    db_config = config_loader.get_config("DB_CONFIG")
    if db_config:
        print(db_config.db_server)
        print(db_config.db_port)
        print(db_config.db_username)
        print(db_config.db_password)
```
