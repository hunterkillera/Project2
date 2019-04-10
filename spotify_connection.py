import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint

def main():
    # Connection information
    client_id = '4394f6c6ce164881abb7cf4b46aa7c2b'
    client_secret = '838d2b7c59804892a71d4d26859f7ec3'

    credentials = SpotifyClientCredentials(client_id, client_secret)
    spotify = spotipy.Spotify(client_credentials_manager=credentials)

    # results = spotify.search('Mona Lisa', type='track', limit=1)
    # artists = results['tracks']['items'][0]['album']['artists']
    # pprint.pprint(artists)


    results = spotify.search('Look Alive', type='track', limit=1)
    artists = results['tracks']['items'][0]['album']['artists']

    #pprint.pprint(results)
    pprint.pprint(artists)


main()