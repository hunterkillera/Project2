import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from project import graph
from py2neo import Node, Relationship


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

        if artist_name != main_artist:
            if artist_name not in list(features.keys()):
                features[artist_name] = [track_name]
            else:
                songs = features[artist_name]
                songs.append(track_name)
                features[artist_name] = songs


    return


def get_connected_artists_from_spotify(inputted_artist):
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
    print(f"LOOKING FOR {artist_name}'s COLLABORATIONS")

    artist_collaborators = {}
    artist_albums = obtain_albums(spotify, artist_id)

    for album in artist_albums:
        name, artist_id = 0, 1
        #print(f'\nChecking for collaborations on {album[name]}')
        #print('---------------------------------------------------')
        songs = get_songs(spotify, album[artist_id])
        for song in songs:
            get_features(artist_name, song, artist_collaborators)

    tx = graph.begin()
    a = Node("Artist", name=str(artist_name), major="yes")
    tx.create(a)
    for key, value in artist_collaborators.items():
        collaborator_name = Node("Artist", name=str(key), collab=str(artist_name), major="no")
        collaborator_rel = Relationship(a, "Collabed with", collaborator_name, song=value)
        tx.create(collaborator_name)
        tx.create(collaborator_rel)
    tx.commit()

    print(f'Collavorators: {artist_collaborators}')

    return artist_collaborators


def main():
    name = input('enter an artist')
    get_connected_artists_from_spotify(name)

if __name__== '__main__':
    main()



'''features for Drake:
{artist1: [song1, song2, songn] , artist2: [song1, song2, songn}'''