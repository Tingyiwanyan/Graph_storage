from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
#import ast

class graph_data_base_endpoint(Resource):
	def __init__(self):
		"""
		define initial directed graph
		"""
		self.G = nx.DiGraph()

	#def get(self):

	def add_node(self):
		"""
		add new node, attribute is default to be none
		"""
		parser = reqparse.RequestParser()
		parser.add_argument('source_node',required=True)
		parser.add_argument('attribute_name',required=True)
		parser.add_argument('attribute',required=True)
		args = parser.parse_args()

		source = args['source_node']
		attribute_name = args['attribute_name']
		attribute = args['attribute']

		self.G.add_node(source)
		if not args[attribute] == None:
			if not args[attribute_name] == None:
				nx.set_node_attributes(self.G,{source: attribute},attribute_name)
			else:
				nx.set_node_attributes(self.G,{source: attribute},'attribute')


	def add_triple(self):
		"""
		fill in triple relations.
		"""
		parser = reqparse.RequestParser()
		parser.add_argument('source_node',required=True)
		parser.add_argument('relation_type',required=True)
		parser.add_argument('target_node',required=True)
		args = parser.parse_args()

		source = args['source_node']
		relation_type = args['relation_type']
		target = args['target_node']

		self.G.add_edge(source, target, relation=relation_type)

	def remove_triple(self):
		"""
		remove relation
		"""
		parser = reqparse.RequestParser()
		parser.add_argument('source_node',required=True)
		parser.add_argument('target_node',required=True)
		args = parser.parse_args()

		source = args['source_node']
		target = args['target_node']

		self.G.remove_edge(source, target)

	def query_target(self):
		"""
		query target node based on source and relation type
		"""
		parser = reqparse.RequestParser()
		parser.add_argument('source_node',required=True)
		parser.add_argument('relation_type',required=True)
		args = parser.parse_args()

		source = args['source_node']
		relation_type = args['relation_type']

		for i in self.G.successors(source):
			r = self.G[source][i]['relation']
			if r == relation_type:
				return i

		return None

	def query_all_relation(self):
		"""
		return all relation type
		"""
		parser = reqparse.RequestParser()
		parser.add_argument('source_node',required=True)
		args = parser.parse_args()

		source = args['source_node']

		for i in self.G.successors(source):
			r = self.G[source][i]['relation']
			print("%s, %s, %s" % (source, r, i))

	def vis_graph(self):
		"""
		visualize the knowledge graph
		"""
		poses=nx.spring_layout(self.G)
		nx.draw(self.G, pos=poses, with_labels=True)
		edge_labels = nx.get_edge_attributes(self.G,'relation')
		nx.draw_networkx_edge_labels(self.G, pos=poses, edge_labels=edge_labels)
		plt.show()
