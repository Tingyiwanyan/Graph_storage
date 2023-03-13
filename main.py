from utility.construct_graph import graph_data_base
from utility.end_point import graph_data_base_endpoint
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd


if __name__ == '__main__':
	app = Flask(__name__)
	api = Api(app)

	api.add_resource(graph_data_base_endpoint, '/graph_data_base')
	#app.run()
	graph_data_base = graph_data_base()

