from flask import Flask, request, jsonify
from pyspark.sql import SparkSession
import pandas as pd

"""
Initiate spark session
"""
spark = SparkSession.builder.enableHiveSupport().getOrCreate()


columns = ["source", "relation", "target"]

data = [("james","where","Home")]

triple_DF = spark.sparkContext.parallelize(data).toDF(columns)

spark.sql("CREATE DATABASE IF NOT EXISTS graph_database")

#Create internal tabel

triple_DF.write.mode('overwrite').saveAsTable("graph_database.triple_relation")

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
	columns = ["source", "relation", "target"]
	data = [(source,relation,target)]

	df_temp = spark.sparkContext.parallelize(data).toDF(columns)

	df_temp.write.mode('append').saveAsTable("graph_database.triple_relation")

	#df.write.insertInto("graph_database.temporal_table",overwrite = False)

	new_triple = {
	'source' : source,
	'relation' : relation,
	'target' : target
	}
	return jsonify(new_triple) # for the browser to understand that a new store was created.

# route for getting target
#@app.route('/show_all_triples')
#def show_triples():
#    return G.query_all_relation()


app.run(host='0.0.0.0',port=8080)

