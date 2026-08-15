"""
Medallion Pipeline for NRB Loan Risk Assessment Engine
- Bronze: Parquet Streaming Ingestion
- Silver: Cleansing & Metric Computation (DTI, LTV)
- Gold: ML Risk Score Engine (GBT / XGBoost Classifier)
"""

import builtins
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, round as sp_round, current_timestamp, when
from pyspark.sql.types import StructType, StructField, TimestampType, LongType, DoubleType, IntegerType, StringType
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import GBTClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator

# Python native round reference to prevent conflicts
py_round = builtins.round


def init_spark():
    """Spark Session Initialization"""
    return SparkSession.builder \
        .appName("NRB-Loan-Risk-Engine") \
        .config("spark.sql.shuffle.partitions", "2") \
        .getOrCreate()


def run_bronze_layer(spark):
    """Bronze Layer: Ingest Stream to Lakehouse Storage"""
    print("\n[🥉] Starting Bronze Streaming Ingestion...")
    
    schema = StructType([
        StructField("timestamp", TimestampType(), True),
        StructField("value", LongType(), True),
        StructField("ingested_at", TimestampType(), True)
    ])

    bronze_stream = spark.readStream \
        .schema(schema) \
        .format("parquet") \
        .load("/tmp/parquet/bronze_loans")

    return bronze_stream


def run_silver_layer(bronze_stream):
    """Silver Layer: Feature Engineering (DTI & LTV Ratio)"""
    print("[🥈] Running Silver Transformations & Feature Engineering...")
    
    enriched = bronze_stream \
        .withColumn("loan_id", expr("concat('L-NRB-', value)")) \
        .withColumn("applicant_income", (expr("value % 150000") + 35000).cast(DoubleType())) \
        .withColumn("coapplicant_income", (expr("value % 50000")).cast(DoubleType())) \
        .withColumn("loan_amount", (expr("value % 2000000") + 100000).cast(DoubleType())) \
        .withColumn("credit_score", (expr("value % 350") + 500).cast(IntegerType())) \
        .withColumn("collateral_value", (expr("value % 4000000") + 500000).cast(DoubleType()))

    silver_df = enriched \
        .withColumn("total_income", col("applicant_income") + col("coapplicant_income")) \
        .withColumn("dti_ratio", sp_round(col("loan_amount") / col("total_income"), 4)) \
        .withColumn("ltv_ratio", sp_round(col("loan_amount") / col("collateral_value"), 4)) \
        .filter(
            (col("applicant_income") > 0) & 
            (col("loan_amount") > 0) & 
            (col("credit_score").between(300, 850))
        ) \
        .withColumn("processed_at", current_timestamp())

    return silver_df


def train_gold_ml_model(spark):
    """Gold Layer: Machine Learning Default Risk Assessment Engine"""
    print("[🥇] Training Gold Layer Machine Learning Model (GBT/XGBoost)...")
    
    silver_df = spark.read.format("parquet").load("/tmp/parquet/silver_loans")

    # Label Assignment Rules (NRB Compliance Framework)
    labeled_df = silver_df.withColumn(
        "is_default",
        when(
            (col("dti_ratio") > 0.45) | 
            (col("credit_score") < 600) | 
            (col("ltv_ratio") > 0.80), 
            1
        ).otherwise(0)
    )

    feature_cols = ["applicant_income", "total_income", "dti_ratio", "ltv_ratio", "credit_score"]
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    ml_dataset = assembler.transform(labeled_df).select("features", "is_default", "loan_id")

    train_data, test_data = ml_dataset.randomSplit([0.8, 0.2], seed=42)

    gbt = GBTClassifier(labelCol="is_default", featuresCol="features", maxDepth=5, maxIter=20)
    model = gbt.fit(train_data)

    predictions = model.transform(test_data)
    evaluator = BinaryClassificationEvaluator(labelCol="is_default", rawPredictionCol="rawPrediction")
    auc_score = evaluator.evaluate(predictions)

    print(f"✅ Training Complete! Model AUC Score: {auc_score:.4f}")
    
    # Save Model to disk
    model_path = "/tmp/models/gbt_loan_model"
    model.write().overwrite().save(model_path)
    print(f"💾 Model persisted successfully to '{model_path}'")

    return predictions


if __name__ == "__main__":
    spark = init_spark()
    print("🚀 NRB Medallion Pipeline Engine Initialized.")
    
    # Run Gold Model Training on available Silver Storage
    if os.path.exists("/tmp/parquet/silver_loans"):
        train_gold_ml_model(spark)
    else:
        print("⚠️ Silver Storage not found. Please run streaming driver to collect initial batch.")
