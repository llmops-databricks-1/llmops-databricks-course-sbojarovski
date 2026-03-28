"""Configuration management using Pydantic Settings."""

from pathlib import Path
from typing import Any

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DatabricksConfig(BaseModel):
    """Databricks workspace configuration.

    Environment variables prefixed with DATABRICKS_ are automatically loaded.
    Example: DATABRICKS_HOST, DATABRICKS_SERVERLESS_COMPUTE_ID
    """

    # Databricks workspace host URL
    # Defaults to Databricks Free Edition community workspace
    host: str = "https://community.cloud.databricks.com"
    # Serverless compute ID for the target workspace (optional)
    serverless_compute_id: str | None = None


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env files.

    Environment files are loaded from ./environments/{environment}.env
    Development settings can be overridden by setting environment variables.
    """

    # Databricks configuration (loads DATABRICKS_* environment variables)
    databricks: DatabricksConfig = DatabricksConfig()
    # Spark session profile for Databricks Connect
    spark_session_profile: str = "bojarovski-llmops"

    class Config:
        """Pydantic configuration."""

        # Load from environment variables
        env_file = None  # Set dynamically in __init__
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Use double underscore for nested model environment variables
        # e.g., DATABRICKS__HOST for databricks.host
        env_nested_delimiter = "__"

    def __init__(
        self,
        environment: str = "local",
        **data: Any,  # noqa: ANN401
    ) -> None:
        """Initialize settings, loading from the appropriate environment file.

        Args:
            environment: Environment name (local, dev, prod, cauchy).
                        Used to load ./environments/{environment}.env
            **data: Additional data to override loaded settings
        """
        # Build path to environment file
        env_file_path = (
            Path(__file__).parent.parent.parent / "environments" / f"{environment}.env"
        )

        # Update config to use the environment file
        self.model_config["env_file"] = (
            str(env_file_path) if env_file_path.exists() else None
        )

        super().__init__(**data)


def get_settings(environment: str = "local") -> Settings:
    """Get application settings for the given environment.

    Args:
        environment: Environment name (local, dev, prod, cauchy).
                    Defaults to 'local'.

    Returns:
        Settings instance configured for the environment.
    """
    return Settings(environment=environment)
