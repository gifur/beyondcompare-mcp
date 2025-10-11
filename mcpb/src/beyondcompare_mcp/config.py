"""Configuration settings for the Beyond Compare MCP server."""

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict


class Settings(BaseModel):
    """Application settings with environment variable overrides."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="forbid"
    )

    # Server configuration
    HOST: str = Field(default="127.0.0.1", description="Host to bind the server to")
    PORT: int = Field(default=8000, description="Port to listen on")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    # Beyond Compare configuration
    BEYOND_COMPARE_PATH: Optional[str] = Field(
        default=None,
        description="Path to Beyond Compare executable (auto-detected if not specified)"
    )

    BC_SCRIPTS_DIR: str = Field(
        default=str(Path.cwd() / "bc_scripts"),
        description="Directory for Beyond Compare script files"
    )

    # Timeouts in seconds
    COMMAND_TIMEOUT: int = Field(
        default=300,
        description="Timeout for Beyond Compare commands in seconds"
    )
    API_TIMEOUT: int = Field(
        default=30,
        description="API request timeout in seconds"
    )

    # Package information
    DXT_PACKAGE_NAME: str = Field(
        default="beyondcompare-mcp",
        description="Package name for DXT builds"
    )
    DXT_PACKAGE_VERSION: str = Field(
        default="0.1.0",
        description="Package version for DXT builds"
    )

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}")
        return v.upper()

    @field_validator("BEYOND_COMPARE_PATH", mode="before")
    @classmethod
    def validate_bc_path(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v

        path = Path(v).expanduser().resolve()
        if not path.exists():
            # Let the application handle the missing executable with a better error message
            return v
        return str(path)

    @field_validator("BC_SCRIPTS_DIR")
    @classmethod
    def validate_scripts_dir(cls, v: str) -> str:
        path = Path(v).expanduser().resolve()
        path.mkdir(parents=True, exist_ok=True)
        return str(path)


def create_settings() -> Settings:
    """Create settings instance with environment variable support."""
    # Read environment variables with fallbacks
    return Settings(
        HOST=os.getenv("HOST", "127.0.0.1"),
        PORT=int(os.getenv("PORT", "8000")),
        LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO"),
        BEYOND_COMPARE_PATH=os.getenv("BEYOND_COMPARE_PATH", None),
        BC_SCRIPTS_DIR=os.getenv("BC_SCRIPTS_DIR", str(Path.cwd() / "bc_scripts")),
        COMMAND_TIMEOUT=int(os.getenv("COMMAND_TIMEOUT", "300")),
        API_TIMEOUT=int(os.getenv("API_TIMEOUT", "30")),
        DXT_PACKAGE_NAME=os.getenv("DXT_PACKAGE_NAME", "beyondcompare-mcp"),
        DXT_PACKAGE_VERSION=os.getenv("DXT_PACKAGE_VERSION", "0.1.0"),
    )


# Global settings instance
settings = create_settings()
