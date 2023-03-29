from flask import Flask, request, jsonify
from pyspark.sql import SparkSession
import pandas as pd

"""
Initiate spark session
"""
spark = SparkSession.builder.enableHiveSupport().getOrCreate()


#columns = ["source", "relation", "target"]

#data = [("james","where","Home")]

#triple_DF = spark.sparkContext.parallelize(data).toDF(columns)

spark.sql("CREATE DATABASE IF NOT EXISTS graph_database")

spark.sql("CREATE TABLE IF NOT EXISTS graph_database.triple_relation (ID Varchar(100), SOURCE Varchar(10000), RELATION Varchar(1000), TIME_ String, TARGET Varchar(1000000))")

#Create internal tabel

#triple_DF.write.mode('overwrite').saveAsTable("graph_database.triple_relation")

#df = spark.read.table("graph_database.triple_relation")
#df.show()


app = Flask(__name__)


#route for adding new triple
@app.route('/add_triple',methods=['POST'])  
def add_triple():
	data = request.get_json() # get the json from the post request object
	source = data['source']
	relation = data['relation']
	target = data['target']
	id_ = data['id']
	time = data['time']
	columns = ["id","source","relation","time","target"]
	data = [(id_,source,relation,time,target)]

	df_temp = spark.sparkContext.parallelize(data).toDF(columns)

	df_temp.createOrReplaceTempView("df_temp")

	spark.sql("INSERT INTO TABLE graph_database.triple_relation SELECT * FROM df_temp")

	#df_temp.write.mode('append').saveAsTable("graph_database.triple_relation")

	#df.write.insertInto("graph_database.temporal_table",overwrite = False)

	new_triple = {
	'id': id_,
	'source' : source,
	'relation' : relation,
	'time' : time,
	'target' : target
	}
	return jsonify(new_triple) # for the browser to understand that a new store was created.

# route for getting target
#@app.route('/show_all_triples')
#def show_triples():
#    return G.query_all_relation()


app.run(host='0.0.0.0',port=8080)

