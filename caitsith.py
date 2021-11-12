import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import dotenv_values
import sys


# .envファイルに含まれるやつを辞書として返す。
config = dotenv_values(".env")

# 環境変数からClient ID, Client Secret, Redirect URIをゲット
client_id     = config['SPOTIFY_CLIENT_ID']
client_secret = config['SPOTIFY_CLIENT_SECRET']
redirect_uri  = config['SPOTIFY_REDIRECT_URI']

# 上のTokenはここで使う。これはClient Credentials FlowのManagerらしい。
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# Spotify API client
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# 謎の
lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
results = spotify.artist_top_tracks(lz_uri)

for track in results['tracks'][:10]:
  print('track    : ' + track['name'])
  print('audio    : ' + track['preview_url'])
  print('cover art: ' + track['album']['images'][0]['url'])
  print()
