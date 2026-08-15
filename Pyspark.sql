# spark_phase1_init.py
from pyspark.sql import SparkSession

# PySpark Version अनुसारको Kafka Package Coordinate
KAFKA_PKG = "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0"
DELTA_PKG = "io.delta:delta-spark_2.12:3.0.0"

spark = SparkSession.builder \
    .appName("NRB-LoanPrediction-Phase1") \
    .config("spark.jars.packages", f"{KAFKA_PKG},{DELTA_PKG}") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

print("Phase 1 Spark Environment initialized with Kafka Connector successfully!")

