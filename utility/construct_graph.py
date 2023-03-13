import networkx as nx
import matplotlib.pyplot as plt
from flask import Flask
from flask_restful import Resource, Api, reqparse

class graph_data_base(Resource):
	def __init__(self):
		"""
		define initial directed graph
		"""
		self.G = nx.DiGraph()

	def add_node(self, source, attribute_name=None, attribute=None):
		"""
		add new node, attribute is default to be none
		"""
		self.G.add_node(source)
		if not attribute == None:
			if not attribute_name == None:
				nx.set_node_attributes(self.G,{source: attribute},attribute_name)
			else:
				nx.set_node_attributes(self.G,{source: attribute},'attribute')


	def add_triple(self, source, relation,target):
		"""
		fill in triple relations.
		"""
		self.G.add_edge(source, target, relation=relation)

	def remove_triple(self, source, target):
		"""
		remove relation
		"""
		self.G.remove_edge(source, target)

	def query_target(self, source, relation):
		"""
		query target node based on source and relation type
		"""
		for i in self.G.successors(source):
			r = self.G[source][i]['relation']
			if r == relation:
				return i

		return None

	def query_all_relation(self, source):
		"""
		return all relation type
		"""
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

	pass

