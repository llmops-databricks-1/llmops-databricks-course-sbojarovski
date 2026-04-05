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
logger.info(f"Set catalog {settings.CATALOG}")
spark.catalog.setCurrentCatalog(settings.CATALOG)

# COMMAND ----------

logger.info(f"Creating schema '{settings.DATA_INGESTION_SCHEMA}'...")
spark.sql(f"""
        CREATE SCHEMA IF NOT EXISTS {settings.DATA_INGESTION_SCHEMA}
        WITH DBPROPERTIES (
            creator_user_name='{settings.USER_SHORT_NAME}',
            environment='{settings.ENV}'
        )
        """)
logger.info(f"Successfully created schema '{settings.DATA_INGESTION_SCHEMA}'")


# COMMAND ----------
logger.info(f"Updating schema comment on '{settings.DATA_INGESTION_SCHEMA}'...")
spark.sql(f"""
        COMMENT ON SCHEMA {settings.DATA_INGESTION_SCHEMA} IS
        'This schema contains objects where ingested data is stored for the llm agent RAG'
        """)
logger.info(f"Successfully added comment to schema '{settings.DATA_INGESTION_SCHEMA}'")

# COMMAND ----------
logger.info(f"Updating schema tags on '{settings.DATA_INGESTION_SCHEMA}'...")
spark.sql(f"""
        ALTER SCHEMA {settings.DATA_INGESTION_SCHEMA}
                SET TAGS (
                'environment' = '{settings.ENV}'
                )
        """)
logger.info(f"Successfully set tags on schema '{settings.DATA_INGESTION_SCHEMA}'")

# COMMAND ----------
logger.info(f"Setting current schema to {settings.DATA_INGESTION_SCHEMA}...")
spark.catalog.setCurrentDatabase(settings.DATA_INGESTION_SCHEMA)

# COMMAND ----------
logger.info(f"Creating {settings.PDF_STORAGE_METADATA_TABLE} table...")
spark.sql(f"""
    CREATE TABLE IF NOT EXISTS {settings.PDF_STORAGE_METADATA_TABLE} (
        paper_id STRING COMMENT 'The id of the paper in arxiv',
        title STRING COMMENT 'The title of the paper',
        authors ARRAY<STRING> COMMENT 'The authors of the paper',
        summary STRING COMMENT 'The summary of the paper',
        published_datetime TIMESTAMP COMMENT 'The published timestamp of the paper',
        processed_datetime TIMESTAMP COMMENT 'The timestamp when the paper was processed by the ingestion pipeline',
        volume_path STRING COMMENT 'The path in the volume where the paper is stored'
    )
    USING DELTA
""")

# COMMAND ----------
logger.info(f"Setting comment on {settings.PDF_STORAGE_METADATA_TABLE} table...")
spark.sql(f"""
    COMMENT ON TABLE {settings.PDF_STORAGE_METADATA_TABLE} IS
    'This table contains metadata of the papers whose PDFs have been ingested and stored in the volume. It serves as a checkpoint for incremental ingestion.'
""")
logger.info(f"Successfully created {settings.PDF_STORAGE_METADATA_TABLE} table")

# COMMAND ----------
logger.info(f"Creating a volume {settings.PDF_STORAGE_VOLUME}")
spark.sql(f"""
    CREATE VOLUME IF NOT EXISTS {settings.PDF_STORAGE_VOLUME}
""")
logger.info(f"Successfully created {settings.PDF_STORAGE_VOLUME} volume")
