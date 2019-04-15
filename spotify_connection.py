import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint

def main():
    # Project-specific connection information
    client_id = '4394f6c6ce164881abb7cf4b46aa7c2b'
    client_secret = '838d2b7c59804892a71d4d26859f7ec3' #TODO: Hide this

    # Connect to spotify's API
    credentials = SpotifyClientCredentials(client_id, client_secret)
    spotify = spotipy.Spotify(client_credentials_manager=credentials)

    # An example search (this essentially returns the same results if you searched 'Look Alive' on their website)
    results = spotify.search('Look Alive', type='track', limit=1)

    # Cleans up the results to show the artists that are in it
    artists = results['tracks']['items'][0]['album']['artists']

    # Pretty print the results because the JSON object is ugly and confusing
    pprint.pprint(artists)

    x = spotify.search('Twenty One Pilots', type='artist')

    pprint.pprint(x)


if __name__ == '__main__':
    main()
