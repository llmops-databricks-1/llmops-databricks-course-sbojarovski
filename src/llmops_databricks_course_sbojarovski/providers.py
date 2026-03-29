"""
This module contains common "providers"  -- recipes for creating services
"""

from databricks.connect import DatabricksSession
from pyspark.sql import SparkSession


def provide_spark_session() -> SparkSession:
    return DatabricksSession.builder.getOrCreate()
