''' This file deals with the different 'webpages' that the website will have '''

from project import app, graph
from flask import render_template, url_for
from project.data_generator import get_connected_artists_from_spotify
from project.forms import QueryForm
from project.queries import *


@app.route('/', methods=['GET', 'POST'])
def home():
    connected_artists = []
    form = QueryForm()

    if form.validate_on_submit():
        artist_wanted = form.artist.data

        # Check database first
        if artist_in_db(artist_wanted):
            print(f'Found {artist_wanted} in database!')
            connected_artists = get_connected_artists_from_db(artist_wanted)
            # Adds to database using Spotify's API
        else:
            print(f'Did not find {artist_wanted} in database... adding now')
            connected_artists = get_connected_artists_from_spotify(artist_wanted)
            print(f'Connected artists in home: {connected_artists}')

    return render_template('group5.html', form=form, connected_artists=connected_artists)
