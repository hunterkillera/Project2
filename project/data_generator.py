''' This file will use Spotify's API to fill a neo4j database with data pertaining to what artists are related to each
other

Pseodocode:
Connect to spotify
Start with drake (id = '3TVXtAsR1Inumwj472S9r4' ) # I figured Drake would be a good artist to start with
Obtain a list of all drake's albums using the spotify.artist_albums(artist_id) function (store the album name and album id)
For album in drakes_albums:
    use spotify.album_tracks(album) to obtain a list of all songs for each album

    For track in album_tracks:
        If another artist on track:
            create and store relationship between drake and artist
        else:
            move on to next track




The above pseudocode should store all of the artists that have worked with Drake, which is a good start.
If we can get that code to work, we can easily modify it to iterate through other artists.  This should be able to fill
our database.


Some notes:
    - Spotify's API returns JSON objects which are ugly when printed. Use pprint.pprint(result) rather than print(result)
      to make the output more clear and user-friendly
    - The spotify.artist_albums tends to return duplicates of albums (since there are different versions of the album)
      so we can deal with this when the time comes.  It's not a big deal but could significantly slow down our code
    - Every artist, album and track have a unique ID.  These will be very useful in our code. Rather than searhcing by
      an artist's name, it will make more sense to search using their ID.
    - Later on, we may want to store the name of the songs that artists worked on together, but for now we wont need to
      include this (for simplicity sake)


Currently this script only makes connections when the desired artist is the head of the song. We will have to update
this somehow to make it add connections where they are featured in songs (if possible).  This change will most likely
take place in the 'get_features' function
'''

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint


def connect_to_spotify():
    ''' Obtains and returns connection to Spotify's API '''

    # Project-specific connection information
    client_id = '4394f6c6ce164881abb7cf4b46aa7c2b'
    client_secret = '838d2b7c59804892a71d4d26859f7ec3'  # TODO: Hide this

    # Connect to spotify's API
    credentials = SpotifyClientCredentials(client_id, client_secret)
    connection = spotipy.Spotify(client_credentials_manager=credentials)
    return connection



def search_artist(spotify, name):
    '''Searches for an artist on Spotify and returns their name and unique ID

    parameters:
        - spotify: connection to Spotify's API
        - name: name of the artist/band the user is interested in

    returns:
        - Artist's name and unique ID if found on Spotify
        - Null if not found on Spotify '''

    print(f'Searching for {name}\n')
    query = spotify.search(name, type='artist', limit=1)
    if not query['artists']['items']:
        print(f"ERROR: COULD NOT FIND ARTIST WITH NAME {name}")
        return

    artist_name = query['artists']['items'][0]['name']
    # This ensures that the correct artist was found
    #user_response = input(f"FOUND '{artist_name}'. Is this who you are interested in? If so, hit enter")
    user_response = False # TODO: change this
    if user_response:
        print(f'SORRY. Please try entering a different artist')
        return
    artist_id = query['artists']['items'][0]['id']
    artist_info = (artist_name, artist_id)

    return artist_info


def obtain_albums(spotify, artist_id):
    ''' Given an artist's ID, returns all of their albums (id and name)
    This function also deals with duplicates.  There's no reason to parse through the same album more than once

    parameters:
        - spotify: connection to Spotify's API
        - artist_id: unique artist ID that user is interested in

    returns:
        - a list of all of the artist's albums (ID and name) on Spotify '''

    album_names = []
    albums_info = []
    albums_json = spotify.artist_albums(artist_id=artist_id)
    albums = albums_json['items']

    for album in albums:
        album_name = album['name']
        album_id = album['id']
        album_info = [album_name, album_id]

        if album_name not in album_names:
            albums_info.append(album_info)
            album_names.append(album_name)

    return albums_info



def get_songs(spotify, album_id):
    ''' Given an ID for an album, returns all the tracks on the album
    parameters:
        - spotify: connection to Spotify's API
        - album_id: album's unique ID

    returns:
        - a list of all tracks on the album '''

    tracks = spotify.album_tracks(album_id)
    tracks = tracks['items']

    return tracks



def get_features(main_artist, track, features):
    ''' Given the json object for a track, appends to 'features' when someone else is on the track
    parameters:
        - main_artist: The head artist on the track (the artist the user is interested in)
        - track: The song json object
        - features: list of artists that have collaborated with the main_artist

    returns:
        - nothing
    '''
    track_name = track['name']
    #print(f'Looking for features on {track_name}...')
    artists = track['artists']
    if artists[0]['name'] != main_artist:
        return
    for artist in artists:
        artist_name = artist['name']
        artist_id = artist['id']
        artist_info = [artist_name, artist_id]

        if (artist_name != main_artist) and (artist_info not in features):
            features.append(artist_info)

    return


def get_connected_artists(inputted_artist):
    ''' Given the name of an artist/band, this function creates and returns a list of all artists that have collaborated
      with that artist

      parameters:
        - inputted_artist: Name of the artist that the user is interested in. Default is an empty string

      returns:
        - list of artists that the main artist has collaborated with (name, id)
    '''

    spotify = connect_to_spotify()
    desired_artist = search_artist(spotify, inputted_artist)

    if not desired_artist:
        return

    artist_name = desired_artist[0]
    artist_id = desired_artist[1]
    #print(f"LOOKING FOR {artist_name}'s COLLABORATIONS")

    artist_collaborators = []
    artist_albums = obtain_albums(spotify, artist_id)

    for album in artist_albums:
        name, artist_id = 0, 1
        #print(f'\nChecking for collaborations on {album[name]}')
        #print('---------------------------------------------------')
        songs = get_songs(spotify, album[artist_id])

        for song in songs:
            get_features(artist_name, song, artist_collaborators)

    collaborator_names = list(artist[0] for artist in artist_collaborators)

    #print(f'\n{artist_name} has collaborated with: {collaborator_names}')

    return collaborator_names
