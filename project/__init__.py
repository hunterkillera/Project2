''' This file initializes the application. It will also establish connection to the database'''

from flask import Flask

# Creates Flask app
app = Flask(__name__)


# this has to stay at the bottom to avoid 'circle importing'
from project import routes
