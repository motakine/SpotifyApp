import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values
from dotenv import load_dotenv
import sys

def get_10_tracks_for_selected_artist(spotify, artist_id):
  results = spotify.artist_top_tracks(artist_id)

  for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()

def client_credentials_something():
  # これはClient Credentials FlowのManagerらしい。
  client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials()
  # Spotify API client
  spotify = spotipy.Spotify(auth_manager=client_credentials_manager)
  artist_id = "https://open.spotify.com/artist/6B9SjvZNSQZkeJDH17oBSO?si=ki7eUh6qTAmwEN239KGYsw"
  get_10_tracks_for_selected_artist(spotify, artist_id)

def get_current_user_liked_songs():
  scope = [
    'user-library-read'
  ]
  sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, show_dialog=True))

  limit = 50
  offset = 0
  results = sp.current_user_saved_tracks(limit=limit, offset=offset)
  for idx, item in enumerate(results['items']):
    track = item['track']
    print(1+offset + idx, track['artists'][0]['name'], " - ", track['name'])
  
  total = results['total']
  while True:
    offset += limit
    if offset >= total:
      break
    results = sp.current_user_saved_tracks(limit=limit, offset=offset)
    for idx, item in enumerate(results['items']):
      track = item['track']
      print(1+offset + idx, track['artists'][0]['name'], " - ", track['name'])
  return

if __name__ == "__main__":
  # .envファイルの内容を環境変数としてos.environ辞書に追加。
  # ファイルが見つからないなら親へ親へと辿っていく
  load_dotenv()

  # client_credentials_something()

  get_current_user_liked_songs()

  
