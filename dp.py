from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructType
from pyspark.sql.functions import from_json, col

def read_kafka_data():
    spark = SparkSession.builder.appName("crypto_data") \
        .config("spark.jars.packages", 
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5,"
                "org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.5.5") \
        .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
        .getOrCreate()
    
    # Read data from kafka
    kafka = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:29092") \
        .option("subscribe", "crypto-data") \
        .option("startingOffsets", "latest") \
        .load()
    
    # Extract the data and cast it as a string
    cast_data = kafka.selectExpr("CAST(value AS STRING)")

    query = cast_data.writeStream \
        .format("console") \
        .outputMode("update") \
        .option("truncate", False) \
        .start()
    query.awaitTermination()

    # schema = StructType().add("field1", StringType()).add("field2", StringType())
    # josn_df = cast_data.select(from_json(col("value"), schema).alias("data")).select("data.*")
    # return josn_df
read_kafka_data()