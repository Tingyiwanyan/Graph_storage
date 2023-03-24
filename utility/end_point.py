from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
#import ast

app = Flask(__name__)

movies = [
    {
        'name' : 'Dune',
        'actors': [
            {
                'name' : 'Zendaya',
                'age'  : '23'
            },
            {
                'name' : 'Timothee Chalamet',
                'age'  : '26'
            }
        ],
        'ratings' : '7.2'
    },
    {
        'name' : 'The French Dispatch',
        'actors': [
            {
                'name': 'Bill Murray',
                'age' : '56'
                
            },
            {
                'name': 'Frances Mcdormand',
                'age' : '54'
            }
        ],
        'ratings' : '8.0'
    }
]

#route for creating new movies
@app.route('/movies',methods=['POST'])  
def create_movies():
    data = request.get_json() # get the json from the post request object

    new_movie = {
        'name' : data['name'],
        'actors' : data['actors'],
        'ratings' : data['ratings']
    }
    movies.append(new_movie)
    return jsonify(new_movie) # for the browser to understand that a new store was created.

    
# route for getting all movies
@app.route('/movies')
def get_movies():
    return jsonify({'movies':movies})

# route for getting anyone one movie
@app.route('/movies/<string:name>')
def get_movie(name):
    for movie in movies :
        if movie['name'] == name:
            return jsonify(movie)
    return jsonify({'message': 'Movie not found'})


# route for getting actors in a movie
@app.route('/movies_get/<string:name>/actors')
def get_actor_in_movie(name):
    for movie in movies:
        if movie['name'] == name:
            return jsonify({"actors": movie['actors']})
    return jsonify({'message': 'Movie not found'})

# route for adding actors to a movie
@app.route('/movies_post/<string:name>/actor',methods=['POST'])
def add_actor_to_movie(name):
    data = request.get_json()
    new_actor = {'name': data['name'],'age': data['age']}
    for movie in movies:
        if movie['name'] == name:
            movie['actors'].append(new_actor)
            return jsonify(movie)
    return jsonify({'message' : 'Movie does not exist'})    
    

app.run()
