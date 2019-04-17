''' This file deals with the different 'webpages' that the website will have '''

from project import app
from flask import render_template
from project.data_generator import get_connected_artists
from project.forms import QueryForm


@app.route('/', methods=['GET', 'POST'])
def home():
    connected_artists = []
    form = QueryForm()
    if form.validate_on_submit():
        artist_wanted = form.artist.data
        connected_artists= get_connected_artists(artist_wanted)
    return render_template('group5.html', form=form, connected_artists=connected_artists)
