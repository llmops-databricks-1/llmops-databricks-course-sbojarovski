"""Application configuration using Pydantic Settings.

Settings are loaded from environment variables. Load .env files via:
- PyCharm: Run → Edit Configurations → Environment → Select environments/local.env
- Command line: source environments/{environment}.env before running
- GitHub Actions: Environment variables set automatically from secrets/workflows
"""

import logging
from typing import Any

from databricks.sdk import WorkspaceClient
from pydantic import computed_field
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

from llmops_databricks_course_sbojarovski.providers import provide_workspace_client

logger = logging.getLogger(__name__)


def get_dbutils_var(key: str, workspace_client: WorkspaceClient) -> str:
    """Fetch a variable value from Databricks dbutils widgets.

    Raises an exception if the widget does not exist, allowing Pydantic
    to fall back to the next settings source.
    """
    value = workspace_client.dbutils.widgets.get(key)
    logger.debug(f"Retrieved dbutils widget value for '{key}'")
    return value


class DbUtilsSettingsSource(PydanticBaseSettingsSource):
    """Custom settings source that loads from Databricks dbutils widgets."""

    def __init__(
        self,
        settings_cls: type[BaseSettings],
        workspace_client: WorkspaceClient,
    ):
        super().__init__(settings_cls)
        self.workspace_client = workspace_client

    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        """Get value for a single field from dbutils widgets."""
        try:
            value = get_dbutils_var(field_name, self.workspace_client)
            return value, field_name, False
        except Exception as e:
            # Not found in dbutils, let other sources handle it
            raise ValueError(f"Field '{field_name}' not found in dbutils") from e

    def __call__(self) -> dict[str, Any]:
        """Load settings from dbutils widgets."""
        data = {}
        for field_name in self.settings_cls.model_fields:
            try:
                value = get_dbutils_var(field_name, self.workspace_client)
                if value:
                    data[field_name] = value
            except Exception as e:
                logger.debug(f"Could not load '{field_name}' from dbutils widgets: {e}")
                # Widget not found or unavailable, skip to allow next source
                pass
        return data


def print_config() -> None:
    logger.info(f"""Current settings:\n{settings.model_dump_json(indent=4)}""")


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    All configuration is accessed via UPPERCASE_WITH_UNDERSCORE field names.
    Settings are loaded with the following priority:
    1. Init settings (passed explicitly)
    2. Environment variables
    3. Databricks widgets via dbutils
    4. Default values

    Example: To load local environment in PyCharm or shell:
        source environments/local.env
        python your_script.py
    """

    # Databricks configuration
    DATABRICKS_CONFIG_PROFILE: str = "bojarovski-llmops"
    DATABRICKS_HOST: str = "https://community.cloud.databricks.com"
    DATABRICKS_SERVERLESS_COMPUTE_ID: str = "auto"

    ENV: str = "local"
    USER_SHORT_NAME: str | None = None

    @property
    @computed_field
    def CATALOG_NAME(self) -> str:
        """Determine catalog name based on ENV setting."""
        catalog_name_mapping = {
            "local": "mlops_dev",
            "dev": "mlops_acc",
            "prod": "mlops_prd",
        }
        return catalog_name_mapping.get(self.ENV, catalog_name_mapping["local"])

    DATA_INGESTION_SCHEMA_NAME: str = "ingested_data"

    PDF_STORED_METADATA_TABLE_NAME: str = "arxiv_papers"

    class Config:
        """Pydantic Settings configuration."""

        # Case-sensitive to match uppercase environment variables
        case_sensitive = True

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Define settings sources with custom priority.

        Priority (highest to lowest):
        1. Init settings (explicit values passed to constructor)
        2. Environment variables
        3. Databricks widgets/dbutils
        4. Dotenv files
        5. Secret files
        """

        return (
            init_settings,
            env_settings,
            DbUtilsSettingsSource(settings_cls, provide_workspace_client()),
            dotenv_settings,
            file_secret_settings,
        )


# Global settings instance - instantiated once at module import
# Reads from environment variables that are already set
# (via .env file loading, PyCharm config, or GitHub Actions)
settings = Settings()
