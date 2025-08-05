# ConfigLoader

A lightweight Python package to load and validate `.ini`-style configuration files using `pydantic` models.

## Features

- Load `.ini`/`.cfg` configuration files from a directory.
- Strong runtime validation using `pydantic`.
- Support for optional or required config sections.
- Extendable with reusable config section templates (e.g., MongoDB, MySQL, etc.).

## Installation

You can install directly from GitHub:

```bash
pip install git+https://github.com/your-username/configloader.git
```

## Quick Start

### Sample App Directory Hierarchy

```
my_app/
├── configs/
│   └── app_config.cfg
├── config_models/
│   └── app_config_models.py
└── main.py
```

### app_config.cfg

```ini
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

### app_config_models.py

```python
from typing import ClassVar
from pydantic import BaseModel, Field, field_validator
from ipaddress import IPv4Address
from configloader.base import ConfigSection


class GeneralConfig(ConfigSection):
    config_section_name: ClassVar[str] = "GENERAL"
    app_name: str
    version: float
    development: bool

    @field_validator("version")
    @classmethod
    def version_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("ensure this value is greater than 0")
        return v


class DatabaseConfig(ConfigSection):
    config_section_name: ClassVar[str] = "DB_CONFIG"
    db_server: IPv4Address
    db_port: int = Field(..., gt=0, le=65535)
    db_username: str
    db_password: str
```

### main.py

```python
from configloader.loaders import ConfigLoader
from config_models.app_config_models import GeneralConfig, DatabaseConfig

if __name__ == "__main__":
    config_loader = ConfigLoader(
        config_dir="configs", active_models=[GeneralConfig, DatabaseConfig]
    )
    config_loader.load_configs()

    db_config = config_loader.get_config("DB_CONFIG")
    print(db_config.db_server)
    print(db_config.db_port)
    print(db_config.db_username)
    print(db_config.db_password)
```

## Exception Handling

ConfigLoader may raise the following exceptions:

- `ConfigLoaderError`: Base exception class.
- `MissingSectionError`: Raised when required sections are not found.
- `ConfigValidationError`: Raised when validation of a section fails.

## License

MIT