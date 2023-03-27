from flask import Flask, request, jsonify
from pyspark.sql import SparkSession
import pandas as pd

spark = SparkSession.builder.master("local")\
.appName("graph_server")\
.config("spark.sql.warehouse.dir","/home/ubuntu")\
.enableHiveSupport()\
.getOrCreate()


columns = ["id", "source", "relation", "target"]

data = [(1,"james","where","Home")]

triple_DF = spark.sparkContext.parallelize(data).toDF(columns)

#Create internal tabel

triple_DF.write.mode('overwrite').saveAsTable("graph_server")

df = spark.read.table("graph_server")
df.show()
