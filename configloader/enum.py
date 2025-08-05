from typing import Literal
from typing_extensions import Annotated

def ConfigEnum(*values: str):
    """
    Factory function to create a pydantic-compatible constrained enum.

    Example:
        environment: ConfigEnum("development", "staging", "production")
    """
    return Annotated[str, Literal[*values]]