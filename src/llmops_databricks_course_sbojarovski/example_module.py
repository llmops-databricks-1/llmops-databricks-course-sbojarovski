from databricks.connect import DatabricksSession


def example_function() -> None:
    spark = DatabricksSession.builder.getOrCreate()
    # from llmops_databricks_course_sbojarovski.config import settings
    # spark = (
    #     DatabricksSession.builder.profile(settings.DATABRICKS_CONFIG_PROFILE)
    #     .serverless(True)
    #     .getOrCreate()
    # )
    df = spark.read.table("samples.nyctaxi.trips")
    df.show(5)
