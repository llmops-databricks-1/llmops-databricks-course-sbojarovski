import logging

from llmops_databricks_course_sbojarovski.config import print_config
from llmops_databricks_course_sbojarovski.example_module import example_spark_function
from llmops_databricks_course_sbojarovski.providers import provide_spark_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    print_config()
    spark = provide_spark_session()
    example_spark_function(spark)
