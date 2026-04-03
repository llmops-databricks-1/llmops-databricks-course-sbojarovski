from pyspark.sql import SparkSession


def example_spark_function(
    spark: SparkSession,
) -> None:
    df = spark.read.table("samples.nyctaxi.trips")
    df.show(5)
