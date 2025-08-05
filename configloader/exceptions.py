class ConfigLoaderError(Exception):
    """Base exception for all configloader-related errors."""


class MissingSectionError(ConfigLoaderError):
    """Raised when expected config sections are not found."""

    def __init__(self, missing_sections):
        missing_list = ", ".join(missing_sections)
        super().__init__(f"Missing required config sections: {missing_list}")
        self.missing_sections = missing_sections


class ConfigValidationError(ConfigLoaderError):
    """Raised when a section fails validation against its Pydantic model."""

    def __init__(self, section: str, error: str):
        super().__init__(f"Validation failed for section [{section}]: {error}")
        self.section = section
        self.error = error
