# Databricks notebook source
import logging

from llmops_databricks_course_sbojarovski.config import settings
from llmops_databricks_course_sbojarovski.providers import provide_spark_session

# COMMAND ----------
# Setup logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("py4j").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# COMMAND ----------
spark = provide_spark_session()

# COMMAND ----------
# Set catalog
logger.info(f"Set catalog {settings.CATALOG_NAME}")
spark.catalog.setCurrentCatalog(settings.CATALOG_NAME)

# COMMAND ----------

logger.info(f"Creating schema '{settings.DATA_INGESTION_SCHEMA_NAME}'...")
try:
    spark.sql(f"""
            CREATE SCHEMA IF NOT EXISTS {settings.DATA_INGESTION_SCHEMA_NAME}
            WITH DBPROPERTIES (
            Name='{settings.USER_SHORT_NAME}',
            Environment='{settings.ENV}'
            )
            """)
    logger.info(f"Successfully created schema '{settings.DATA_INGESTION_SCHEMA_NAME}'")
except Exception as e:
    logger.error(f"Failed to create schema: {e}", exc_info=True)
    raise

# COMMAND ----------
logger.info(f"Updating schema '{settings.DATA_INGESTION_SCHEMA_NAME}'...")
try:
    spark.sql(f"""
            COMMENT ON SCHEMA {settings.DATA_INGESTION_SCHEMA_NAME} IS
            'This schema contains objects where ingested data is stored for the llm agent RAG'
            """)
    logger.info(f"Successfully added comment to schema '{settings.DATA_INGESTION_SCHEMA_NAME}'")
except Exception as e:
    logger.warning(f"Could not add comment to schema: {e}")

try:
    spark.sql(f"""
            ALTER SCHEMA {settings.DATA_INGESTION_SCHEMA_NAME}
                    SET TAGS (
                    'environment' = '{settings.ENV}',
                    'owner_name' = '{settings.USER_SHORT_NAME}'
                    )
            """)
    logger.info(f"Successfully set tags on schema '{settings.DATA_INGESTION_SCHEMA_NAME}'")
except Exception as e:
    logger.warning(f"Could not set tags on schema (may require additional permissions): {e}")

spark.catalog.setCurrentDatabase(settings.DATA_INGESTION_SCHEMA_NAME)

# COMMAND ----------
logger.info(f"Creating {settings.PDF_STORED_METADATA_TABLE_NAME} table...")
spark.sql(f"""
    CREATE TABLE IF NOT EXISTS {settings.PDF_STORED_METADATA_TABLE_NAME} (
        paper_id STRING COMMENT 'The id of the paper in arxiv',
        title STRING COMMENT 'The title of the paper',
        authors ARRAY<STRING> COMMENT 'The authors of the paper',
        summary STRING COMMENT 'The summary of the paper',
        published_datetime LONG COMMENT 'The published timestamp of the paper',
        processed_datetime LONG COMMENT 'The timestamp when the paper was processed by the ingestion pipeline',
        volume_path STRING COMMENT 'The path in the volume where the paper is stored'
    )
    USING DELTA
""")
spark.sql(f"""
    COMMENT ON TABLE {settings.PDF_STORED_METADATA_TABLE_NAME} IS
    'This table contains metadata of the papers whose PDFs have been ingested and stored in the volume. It serves as a checkpoint for incremental ingestion.'
""")
logger.info(f"Successfully created {settings.PDF_STORED_METADATA_TABLE_NAME} table")
