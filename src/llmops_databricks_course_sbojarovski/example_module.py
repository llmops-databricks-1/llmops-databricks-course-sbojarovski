from databricks.connect import DatabricksSession

from llmops_databricks_course_sbojarovski.config import SPARK_SESSION_PROFILE


def example_function() -> None:
    spark = (
        DatabricksSession.builder.profile(SPARK_SESSION_PROFILE)
        .serverless(True)
        .getOrCreate()
    )
    df = spark.read.table("samples.nyctaxi.trips")
    df.show(5)
