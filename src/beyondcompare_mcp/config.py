"""Configuration settings for the Beyond Compare MCP server."""

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """Application settings with environment variable overrides."""
    
    # Server configuration
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Beyond Compare configuration
    BEYOND_COMPARE_PATH: str = Field(
        default="BCompare.exe" if os.name == "nt" else "bcompare",
        env="BEYOND_COMPARE_PATH"
    )
    
    BC_SCRIPTS_DIR: str = Field(
        default=str(Path.cwd() / "bc_scripts"),
        env="BC_SCRIPTS_DIR"
    )
    
    # Timeouts in seconds
    COMMAND_TIMEOUT: int = Field(default=300, env="COMMAND_TIMEOUT")  # 5 minutes
    API_TIMEOUT: int = Field(default=30, env="API_TIMEOUT")  # 30 seconds
    
    # DXT packaging
    DXT_PACKAGE_NAME: str = "beyondcompare-mcp"
    DXT_PACKAGE_VERSION: str = "0.1.0"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    @validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}")
        return v.upper()
    
    @validator("BEYOND_COMPARE_PATH", pre=True)
    def validate_bc_path(cls, v):
        if not v:
            return v
            
        path = Path(v).expanduser().resolve()
        if not path.exists():
            # Let the application handle the missing executable with a better error message
            return v
        return str(path)
    
    @validator("BC_SCRIPTS_DIR")
    def validate_scripts_dir(cls, v):
        path = Path(v).expanduser().resolve()
        path.mkdir(parents=True, exist_ok=True)
        return str(path)


# Global settings instance
settings = Settings()
