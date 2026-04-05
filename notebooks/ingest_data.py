# Databricks notebook source
import logging

from llmops_databricks_course_sbojarovski.providers import (
    provide_data_ingestion_service,
    provide_spark_session,
)

# COMMAND ----------
# Setup logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("py4j").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# COMMAND ----------
spark = provide_spark_session()

logger.info("Ingesting data")

data_ingestion_service = provide_data_ingestion_service()
data_ingestion_service.ingest()

logger.info("Finished ingesting data")
