''' This file deals with the different 'webpages' that the website will have '''

from project import app
from flask import render_template

@app.route('/')
def home():
    return render_template('home.html')