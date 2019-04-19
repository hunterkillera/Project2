''' This file initializes the application. It will also establish connection to the database'''

from flask import Flask
from py2neo import Graph, Node, Relationship

# Creates Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret' # TODO: Change this

# Establish connection to neo4j graph
#TODO: Hide these
uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"

g = Graph(uri=uri, user=user, password=password)

# this has to stay at the bottom to avoid 'circle importing'
from project import routes
