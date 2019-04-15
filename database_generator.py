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

'''

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint

''' Obtains and returns connection to Spotify's API '''
def connect_to_spotify():
    # Project-specific connection information
    client_id = '4394f6c6ce164881abb7cf4b46aa7c2b'
    client_secret = '838d2b7c59804892a71d4d26859f7ec3'  # TODO: Hide this

    # Connect to spotify's API
    credentials = SpotifyClientCredentials(client_id, client_secret)
    connection = spotipy.Spotify(client_credentials_manager=credentials)
    return connection

''' Given an artist's ID, returns all of their albums (id and name) 
This function also deals with duplicates.  There's no reason to parse through the same album more than once'''
def obtain_albums(spotify, artist_id):
    album_names = []
    albums_info = []
    albums_json = spotify.artist_albums(artist_id=artist_id)
    albums = albums_json['items']

    for album in albums:
        album_name = album['name']
        album_id = album['id']
        # print(f'FOUND AN ALBUM: {album_name} with an ID of {album_id}')
        album_info = [album_name, album_id]
        if album_name not in album_names:
            albums_info.append(album_info)
            album_names.append(album_name)

    return albums_info


def main():
    spotify = connect_to_spotify()

    # Will use Drake as a starting point
    drake_id = '3TVXtAsR1Inumwj472S9r4'

    drake_albums = obtain_albums(spotify, drake_id)

    for album in drake_albums:
        print(album)




if __name__ == '__main__':
    main()