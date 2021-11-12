import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import dotenv_values
from dotenv import load_dotenv
import sys

def get_samples_and_cover_art_for_10_tracks_for_selected_artist(spotify, artist_uri):
  results = spotify.artist_top_tracks(artist_uri)

  for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()

def client_credentials_something():
  # これはClient Credentials FlowのManagerらしい。
  client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials()
  # Spotify API client
  spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
  artist_uri = "https://open.spotify.com/artist/6B9SjvZNSQZkeJDH17oBSO?si=ki7eUh6qTAmwEN239KGYsw"
  get_samples_and_cover_art_for_10_tracks_for_selected_artist(spotify, artist_uri)

if __name__ == "__main__":
  # # .envファイルに含まれるやつを辞書として返す。
  # config = dotenv_values(".env")

  # # 環境変数からClient ID, Client Secret, Redirect URIをゲット
  # client_id     = config['SPOTIPY_CLIENT_ID']
  # client_secret = config['SPOTIPY_CLIENT_SECRET']
  # redirect_uri  = config['SPOTIPY_REDIRECT_URI']

  # .envファイルの内容を環境変数としてos.environ辞書に追加。
  # ファイルが見つからないなら親へ親へと辿っていく
  load_dotenv()

  client_credentials_something()

  # scope = [
  #   'user-read-private',
  #   'user-read-recently-played',
  #   'playlist-read-private',
  #   'playlist-read-collaborative'
  # ]
  # sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(scope=scope))

  # results = sp.current_user_saved_tracks()
  # for idx, item in enumerate(results['items']):
  #   track = item['track']
  #   print(idx, track['artists'][0]['name'], " - ", track['name'])

  
