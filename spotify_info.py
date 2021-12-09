import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

import json_data

class SpotifyInfo:
  """Spotify Web APIを使って情報を取得するクラス。
  """
  def __init__(self, is_local):
    """コンストラクタ。

    Args:
        is_local (bool): ローカルのjsonファイルを使用するならTrue, Google Drive上のものを使用するならFalse。
    """
    self.json_data = json_data.JsonData(is_local)
    """ローカルに保存されたLiked Songsとこれまで選択した曲の情報"""
  
  def get_next_liked_song(self):
    """現在のLiked Songsを必要があれば更新し、その中から選択したことのないものを一つ返す。これを外から呼び出す。
    なお、既に今日の分を実行していた場合にはNoneを返す。
    """
    # 今日の分が既に終わっていればNoneを返す。
    if not self.json_data.is_allowed_to_run:
      return None

    # 曲数の変化があればLiked Songsの更新（とjsonファイルへの保存）を行う。
    saved_number_of_songs = self.json_data.number_of_dict_songs(self.json_data.liked_songs_dict)
    self._update_liked_songs(saved_number_of_songs)
    # 次の曲をピックアップして返す。
    next_song = self.json_data.select_a_song_from_liked_songs()
    return next_song

  def _update_liked_songs(self, saved_number_of_songs):
    """ローカルに保存されたLiked Songsの曲数とSpotify APIで取得したLiked Songsの曲数に違いがあれば、
    ローカルに保存されたLiked Songsを更新して保存する。

    Args:
        saved_number_of_songs (int): ローカルに保存されたLiked Songsの曲数
    
    Returns:
        bool: 更新を行ったかどうか
    """
    scope = ['user-library-read']
    print('Spotify Auth start')
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    print('Spotify Auth end')

    limit, offset = 2, 0
    results = sp.current_user_saved_tracks(limit=limit, offset=offset)

    # Spotify APIで取得したLiked Songsの曲数との食い違いがなければ更新をせずに終了する。
    total = results['total']
    if total == saved_number_of_songs:
      return False
    
    # 更新があったとみなし、ローカルに新たなLiked Songsの情報を保存する
    self.json_data.clear_dict(self.json_data.liked_songs_dict)

    limit, offset = 50, 0
    while offset < total:
      results = sp.current_user_saved_tracks(limit=limit, offset=offset)
      for idx, item in enumerate(results['items']):
        track = item['track']
        # アーティストは複数名いる可能性があるので注意。
        self.json_data.append_dict_song(self.json_data.liked_songs_dict, {
          'artist': ', '.join([i['name'] for i in track['artists']]),
          'title': track['name'],
          'spotify_url': track['external_urls']['spotify']
        })
      offset += limit
    
    # Liked Songsを昇順ソートして保存する。
    self.json_data.sort_liked_songs()
    self.json_data.save_json_file_liked_songs()
    return True

