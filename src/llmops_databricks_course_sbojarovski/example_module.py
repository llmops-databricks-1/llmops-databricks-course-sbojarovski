from databricks.connect import DatabricksSession

from llmops_databricks_course_sbojarovski.config import get_settings


def example_function() -> None:
    settings = get_settings(environment="local")
    spark = (
        DatabricksSession.builder.profile(settings.spark_session_profile)
        .serverless(True)
        .getOrCreate()
    )
    df = spark.read.table("samples.nyctaxi.trips")
    df.show(5)
