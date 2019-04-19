''' This file deals with the different 'webpages' that the website will have '''

from project import app, g
from flask import render_template
from project.data_generator import get_connected_artists
from project.forms import QueryForm
from project.inserting_data import *


@app.route('/', methods=['GET', 'POST'])
def home():
    connected_artists = []
    form = QueryForm()
    if form.validate_on_submit():
        artist_wanted = form.artist.data

        # Initially searches database for the artist
        if search_nodes_for_artist(artist_wanted, g):
            print(f'FOUND {artist_wanted}!')
            for related_artist in get_relationships(artist_wanted, g):
                print(related_artist) #TODO: send this to HTML Form

        else:
            print(f'Did not find {artist_wanted}... Adding artist to database now')
            add_artist_to_db(artist_wanted, g)

        '''
        
    # This is a dynamic approach to adding nodes to the database.  Rather than 'pre-loading' it with x amount of artists,
    I think it will be best to add nodes dynamically when a user searches for an artist.  This will not only save memory,
    but will also allow the program to run significantly faster (especially when the artist has already been searched for).
        
    if artist_wanted in database:
        return all artist related through the 'worked-with' relationship
    else:
        create a new node with the wanted artist
        run get_connected_artists(artist_wanted) and add a relationship for each connected artist
        return all artists related through the 'worked-with' relationship 
    
        
        # Note that the 'if statment' should only result to True if that artist has been explicitly searched for 
        For example: if someone searches Eminem, a new node will be created for him and any artists that he has worked 
        with. That means that Lil Wayne would have a node created for him in the database, but he would currently only 
        be connected with Eminem.  We can solve this issue by adding a 'searched-for' attribute defaulting to false for
        each new node and only setting it to True when that artist has been explicitly searched for
        
        
        '''


        connected_artists= get_connected_artists(artist_wanted)
    return render_template('group5.html', form=form, connected_artists=connected_artists)
