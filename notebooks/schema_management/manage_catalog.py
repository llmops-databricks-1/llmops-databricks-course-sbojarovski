# Databricks notebook source
import logging

from llmops_databricks_course_sbojarovski.config import settings
from llmops_databricks_course_sbojarovski.providers import (
    provide_databricks_dbutils,
    provide_spark_session,
)

# COMMAND ----------
# Setup logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("py4j").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# COMMAND ----------
dbutils = provide_databricks_dbutils()

# COMMAND ----------
# Skip catalog management for cauchy environment
if settings.ENV == "cauchy":
    logger.info(f"Skipping catalog management for environment '{settings.ENV}'")
    dbutils.notebook.exit("OK")

# COMMAND ----------
spark = provide_spark_session()

# COMMAND ----------
logger.info(f"Creating catalog '{settings.CATALOG_NAME}'...")
spark.sql(f"""
    CREATE CATALOG IF NOT EXISTS {settings.CATALOG_NAME}
""")
logger.info(f"Successfully created catalog '{settings.CATALOG_NAME}'")


# COMMAND ----------
logger.info(f"Updating catalog '{settings.CATALOG_NAME}'...")
spark.sql(f"""
    COMMENT ON CATALOG {settings.CATALOG_NAME} IS
    'Unity Catalog for the llmops-databricks-course project'
""")
logger.info(f"Successfully added comment to catalog '{settings.CATALOG_NAME}'")

spark.sql(f"""
    ALTER CATALOG {settings.CATALOG_NAME}
    SET TAGS (
        'environment' = '{settings.ENV}'
    )
""")
logger.info(f"Successfully set tags on catalog '{settings.CATALOG_NAME}'")
