import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

import saved_data

class SpotifyInfo:
  """Spotify Web APIを使って情報を取得するクラス。
  """
  def __init__(self):
    self.saved_data = saved_data.SavedData()
    """ローカルに保存されたLiked Songsとこれまで選択した曲の情報"""
  
  def get_next_liked_song(self):
    """現在のLiked Songsの中から選択したことのないものを一つ返す。
       これを外から呼び出してほしい。
    """
    saved_number_of_songs = self.saved_data.number_of_liked_songs()
    self.update_liked_songs(saved_number_of_songs)
    self.saved_data.save_liked_songs()
    next_song = self.saved_data.select_a_song_from_liked_songs()
    self.saved_data.save_selected_songs()
    return next_song

  def update_liked_songs(self, saved_number_of_songs):
    """必要があればローカルに保存されたLiked Songsを更新する。
       更新の判定は曲数が変化したかどうか。
       get_next_liked_song()から呼ばれる。
    Args:
        saved_number_of_songs(int): ローカルに保存されたLiked Songsの曲数
    """
    scope = ['user-library-read']
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    limit, offset = 2, 0
    results = sp.current_user_saved_tracks(limit=limit, offset=offset)

    total = results['total']
    if total == saved_number_of_songs:
      return
    
    # 更新があったとみなし、ローカルに新たなLiked Songsの情報を保存する
    self.saved_data.reset_liked_songs()

    limit, offset = 50, 0
    while offset < total:
      results = sp.current_user_saved_tracks(limit=limit, offset=offset)
      for idx, item in enumerate(results['items']):
        track = item['track']
        # アーティストは複数名いる可能性があるので注意。
        self.saved_data.append_liked_songs({
          'artist': ', '.join([i['name'] for i in track['artists']]),
          'title': track['name'],
          'spotify_url': track['external_urls']['spotify']
        })
      offset += limit
    
    # Liked Songsを昇順ソートしておく。
    self.saved_data.sort_liked_songs()
    return


# def get_10_tracks_for_selected_artist(spotify, artist_id):
#   results = spotify.artist_top_tracks(artist_id)

#   for track in results['tracks'][:10]:
#     print('track    : ' + track['name'])
#     print('audio    : ' + track['preview_url'])
#     print('cover art: ' + track['album']['images'][0]['url'])
#     print()

# def client_credentials_something():
#   # これはClient Credentials FlowのManagerらしい。
#   client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials()
#   # Spotify API client
#   spotify = spotipy.Spotify(auth_manager=client_credentials_manager)
#   artist_id = "https://open.spotify.com/artist/6B9SjvZNSQZkeJDH17oBSO?si=ki7eUh6qTAmwEN239KGYsw"
#   get_10_tracks_for_selected_artist(spotify, artist_id)

# def get_current_user_liked_songs_if_updated(previous_total):
#   '''まず現在のユーザのLiked Songsの曲数を取得し、ローカルに保存した曲目から変化があるかを調べる。
#      変化があれば改めてLiked Songsの曲目を取得し、なければ
  
#   Args:
#       previous_total(int): 保存されていた曲目の曲数
#   '''
#   scope = ['user-library-read']
#   sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

#   limit, offset = 2, 0
#   results = sp.current_user_saved_tracks(limit=limit, offset=offset)

#   for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(1+offset + idx, track['artists'][0]['name'], " - ", track['name'])
  
#   total = results['total']
#   while True:
#     offset += limit
#     if offset >= total:
#       break
#     results = sp.current_user_saved_tracks(limit=limit, offset=offset)
#     for idx, item in enumerate(results['items']):
#       track = item['track']
#       print(1+offset + idx, track['artists'][0]['name'], " - ", track['name'])
#   return

  
