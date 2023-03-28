from flask import Flask, request, jsonify
#from flask_restful import Resource, Api, reqparse
from utility.construct_graph import graph_data_base
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
#import ast


G = graph_data_base()

app = Flask(__name__)

dataa = 1
#route for adding new triple
@app.route('/add_triple',methods=['POST'])  
def add_triple():
    datas = request.get_json() # get the json from the post request object
    dataa = datas
    for data in datas:
        source = data['source']
        relation = data['relation']
        target = data['target']

        G.add_triple(source, relation, target)

        new_triple = {
            'source' : source,
            'relation' : relation,
            'target' : target
        }
    #return jsonify(new_triple) # for the browser to understand that a new store was created.

@app.route('/add_node',methods=['POST'])
def add_node():
    data = request.get_jason()
    source = data['source']
    attribute_name = data['attribute_name']
    attribute = data['attribute']

    G.add_node(source, attribute_name, attribute)

    
# route for getting target

@app.route('/show_all_triples')
def show_triples():
    return G.query_all_relation()

@app.route('/get_target/<string:source>/<string:relation>')
def get_target(source, relation):
    target = G.query_target(source, relation)
    query_triple = {
    'source' : source,
    'relation' : relation,
    'target' : target
    }
    return jsonify({'query_triple':query_triple})

app.run(host='0.0.0.0',port=8080)