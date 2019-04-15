from flask import Flask

# Creates Flask app
app = Flask(__name__)

from project import routes
