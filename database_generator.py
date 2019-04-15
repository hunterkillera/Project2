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

def main():
    # Project-specific connection information
    client_id = '4394f6c6ce164881abb7cf4b46aa7c2b'
    client_secret = '838d2b7c59804892a71d4d26859f7ec3'  # TODO: Hide this

    # Connect to spotify's API
    credentials = SpotifyClientCredentials(client_id, client_secret)
    spotify = spotipy.Spotify(client_credentials_manager=credentials)


if __name__ == '__main__':
    main()