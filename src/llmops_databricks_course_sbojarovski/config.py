"""Application configuration using Pydantic Settings.

Settings are loaded from environment variables. Load .env files via:
- PyCharm: Run → Edit Configurations → Environment → Select environments/local.env
- Command line: source environments/{environment}.env before running
- GitHub Actions: Environment variables set automatically from secrets/workflows
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    All configuration is accessed via UPPERCASE_WITH_UNDERSCORE field names.
    Environment variables are read directly from the current environment,
    so load .env files externally before instantiating Settings.

    Example: To load local environment in PyCharm or shell:
        source environments/local.env
        python your_script.py
    """

    # Spark/Databricks configuration
    SPARK_SESSION_PROFILE: str = "bojarovski-llmops"
    DATABRICKS_HOST: str = "https://community.cloud.databricks.com"
    DATABRICKS_SERVERLESS_COMPUTE_ID: str = "auto"

    class Config:
        """Pydantic Settings configuration."""

        # Case-sensitive to match uppercase environment variables
        case_sensitive = True


# Global settings instance - instantiated once at module import
# Reads from environment variables that are already set
# (via .env file loading, PyCharm config, or GitHub Actions)
settings = Settings()
