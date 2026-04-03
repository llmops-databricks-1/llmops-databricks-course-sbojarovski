# Databricks notebook source
"""
Hello World notebook — verifies the environment is set up correctly.
"""

from llmops_databricks_course_sbojarovski.example_module import example_spark_function
from llmops_databricks_course_sbojarovski.providers import provide_spark_session

# COMMAND ----------

spark = provide_spark_session()
example_spark_function(spark)

# COMMAND ----------

print("Hello, world!")
print("Environment is ready.")
