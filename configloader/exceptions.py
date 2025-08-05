class ConfigLoaderError(Exception):
    """Base exception for configloader."""


class MissingSectionError(ConfigLoaderError):
    """Raised when expected config sections are not found."""


class ConfigValidationError(ConfigLoaderError):
    """Raised when a section fails validation against its Pydantic model."""