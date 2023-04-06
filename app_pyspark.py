from flask import Flask, request, jsonify
from pyspark.sql import SparkSession
import pandas as pd

"""
Initiate spark session
"""
spark = SparkSession.builder.enableHiveSupport().getOrCreate()

spark.sql("CREATE DATABASE IF NOT EXISTS graph_database")


app = Flask(__name__)


#route for adding new triple
@app.route('/add_triple',methods=['POST'])  
def add_triple():
	data = request.get_json() # get the json from the post request object
	source = data['source']
	relation = data['relation']
	#relation_user = data['relationuser']
	target = data['target']
	#id_ = data['id']
	time = data['time']
	columns = ["source","relation","time","target"]
	data = [(id_,relation_user, source,relation,time,target)]
	#print(target)
	#target = ''.join(target.splitlines())
	#print(target)
	df_temp = spark.sparkContext.parallelize(data).toDF(columns)
	#df_temp.show()

	#spark.sql("INSERT INTO graph_database.triple_relation \
	#	VALUES(id_, source, relation, time_, target)")

	#df_temp.createOrReplaceTempView("df_temp")
	#df_temp.write.mode('overwrite').saveAsTable("graph_database.temp_table")

	#spark.sql("INSERT INTO TABLE graph_database.triple_relation SELECT * FROM graph_database.temp_table")
	tables = spark.catalog.listTables("graph_database")
	if "triple_relation" in [table.name for table in tables]:
		df_temp.write.mode('append').saveAsTable("graph_database.triple_relation")
	else:
		df_temp.write.mode('overwrite').saveAsTable("graph_database.triple_relation")

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

