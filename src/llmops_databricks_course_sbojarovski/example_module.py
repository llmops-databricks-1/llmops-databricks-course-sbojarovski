from databricks.connect import DatabricksSession

from llmops_databricks_course_sbojarovski.config import settings


def example_function() -> None:
    spark = (
        DatabricksSession.builder.profile(settings.SPARK_SESSION_PROFILE)
        .serverless(True)
        .getOrCreate()
    )
    df = spark.read.table("samples.nyctaxi.trips")
    df.show(5)
