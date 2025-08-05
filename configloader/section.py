from abc import ABC
from typing import ClassVar
from pydantic import BaseModel


class ConfigSection(BaseModel, ABC):
    """
    Base class for config sections.
    - If `config_section_name` is not defined, the class name is used by default.
    - `config_section_name` is treated as immutable and cannot be changed at runtime.
    """

    config_section_name: ClassVar[str]

    class Config:
        arbitrary_types_allowed = True

    def __init_subclass__(cls):
        if not hasattr(cls, "config_section_name"):
            cls.config_section_name = cls.__name__

    def __setattr__(self, key, value):
        if key == "config_section_name":
            raise AttributeError(
                "'config_section_name' is a class-level constant and cannot be modified on instances."
            )
        super().__setattr__(key, value)
