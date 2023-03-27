from flask import Flask, request, jsonify
from pyspark.sql import SparkSesseion
import pandas as pd

spark = SparkSesseion.builder.maskter("local")
			.appName("graph_server")
			.enableHiveSupport()
			.getOrCreate()


columns = ["id", "source", "relation", "target"]

data = [(1,"james",30,"M")]

triple_DF = spark.sparkContext.parallelize(data).toDF(columns)

#Create internal tabel

triple_DF.write.mode('overwrite').saveAsTable("graph_server")

df = spark.read.table("graph_server")
df.show()
