# ConfigLoader

A lightweight Python package to load and validate `.ini`-style configuration files using `pydantic` models.

## Features

- Load `.cfg` configuration files from a directory.
- Strong runtime validation using `pydantic`.
- Nested attribute access (e.g. `CONFIG.configs.general.app_name`)
- Clean, extendable architecture with reusable config section templates.
- Optional enforcement of required config sections.

## Installation

```bash
pip install git+https://github.com/sghosni/configLoader.git
```

## Directory Layout Example
my_app/
├── configs/
│   └── app_config.cfg
├── config_models/
│   └── app_config_models.py
└── main.py
