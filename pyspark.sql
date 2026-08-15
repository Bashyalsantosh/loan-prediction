from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

spark = SparkSession.builder \
    .appName("NRB-LoanPipeline-Mock") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Define Schema for Loan Data
loan_schema = StructType([
    StructField("loan_id", StringType(), True),
    StructField("bfi_code", StringType(), True),
    StructField("applicant_income", DoubleType(), True),
    StructField("coapplicant_income", DoubleType(), True),
    StructField("loan_amount", DoubleType(), True),
    StructField("credit_score", IntegerType(), True)
])

# Read directly from Rate/Memory Stream (Simulating Realtime Kafka Stream)
raw_stream = spark.readStream \
    .format("rate") \
    .option("rowsPerSecond", 10) \
    .load()

print("Stream Driver Status:", raw_stream.isStreaming)
