import copy
import json
import random

class SavedData:
  """ローカルに保存されたLiked Songsの情報とこれまで選択した曲の情報を扱うクラス。
  """
  JSON_DEFAULT = { 'items': []}

  def __init__(self):
    self.LIKED_SONGS_FILE = r'json\liked_songs.json'
    """ローカルに保存されたLiked Songsの情報が格納されたjsonファイルのパス"""
    self.SELECTED_SONGS_FILE = r'json\selected_songs.json'
    """これまで選択した曲の情報が格納されたjsonファイルのパス"""
    self.liked_songs = copy.deepcopy(SavedData.JSON_DEFAULT)
    """ローカルに保存されたLiked Songsの辞書。編集はSavedDataクラスのメソッドから行いたい。"""
    self.selected_songs = copy.deepcopy(SavedData.JSON_DEFAULT)
    """これまで選択した曲の辞書。編集はSavedDataクラスのメソッドから行いたい。"""
    
    try:
      self.load_liked_songs()
    except FileNotFoundError as e:
      print(e)
      print('Create a new liked songs file.')
      print()
    
    try:
      self.load_selected_songs()
    except FileNotFoundError as e:
      print(e)
      print('Create a new selected songs file.')
      print()
    # Liked Songsに曲が追加されるだけで選択した曲情報が初期化されるとかだと困る、のとはまた別の話。


  def select_a_song_from_liked_songs(self):
    """Liked Songsの中から選択したことのないものを一つランダムに選んで返す。
       それに伴って選んだ曲をこれまで選択した曲に追加する。未完成。
    """
    not_selected_songs = [i for i in self.liked_songs['items'] if i not in self.selected_songs['items']]

    # 選択したことのない曲が存在しなければ、これまで選択した曲をリセットする。
    if len(not_selected_songs) == 0:
      self.reset_selected_songs()
      not_selected_songs = [i for i in self.liked_songs['items'] if i not in self.selected_songs['items']]

    # ランダムに1曲取り出して返す。
    song = random.choice(not_selected_songs)
    self.append_selected_songs(song)
    self.sort_selected_songs()
    return song


  def number_of_liked_songs(self):
    """self.liked_songsの曲数を返す。
    """
    # print(len(self.liked_songs['items']))
    return len(self.liked_songs['items'])

  
  def number_of_selected_songs(self):
    """self.selected_songsの曲数を返す。
    """
    # i = len(self.selected_songs['items'])
    # if i % 100 == 0:
    #   print(f'selected songs: {i}')
    return len(self.selected_songs['items'])
  

  def append_liked_songs(self, song):
    """self.liked_songsに内容を追加する。
    Args:
        song: { 'artist': 'XXX', 'title': 'XXX', 'spotify_url': 'XXX' } の形式。
    """
    self.liked_songs['items'].append(song)


  def reset_liked_songs(self):
    """self.liked_songsの内容を初期化する。
    """
    self.liked_songs = copy.deepcopy(SavedData.JSON_DEFAULT)
  

  def sort_liked_songs(self):
    """self.liked_songsの内容をアーティスト名、タイトル、URLの順に昇順ソートする。大文字小文字は区別しない。
    """
    self.liked_songs['items'] = sorted(self.liked_songs['items'], key=lambda x:(x['artist'].lower(), x['title'].lower(), x['spotify_url'].lower()))

  
  def append_selected_songs(self, song):
    """self.selected_songsに内容を追加する。
    Args:
        song: { 'artist': 'XXX', 'title': 'XXX', 'spotify_url': 'XXX' } の形式。
    """
    self.selected_songs['items'].append(song)
  

  def reset_selected_songs(self):
    """self.selected_songsの内容を初期化する。
    """
    self.selected_songs = copy.deepcopy(SavedData.JSON_DEFAULT)


  def sort_selected_songs(self):
    """self.selected_songsの内容をアーティスト名、タイトル、URLの順に昇順ソートする。大文字小文字は区別しない。
    """
    self.selected_songs['items'] = sorted(self.selected_songs['items'], key=lambda x:(x['artist'].lower(), x['title'].lower(), x['spotify_url'].lower()))


  def load_liked_songs(self):
    """self.liked_songsの内容をローカルから読み込む。
    """
    with open(self.LIKED_SONGS_FILE, 'r', encoding='utf-8') as f:
      self.liked_songs = json.load(f)
  

  def load_selected_songs(self):
    """self.selected_songsの内容をローカルから読み込む。
    """
    with open(self.SELECTED_SONGS_FILE, 'r', encoding='utf-8') as f:
      self.selected_songs = json.load(f)


  def save_liked_songs(self):
    """self.liked_songsの内容をローカルに保存する。jsonは少し整形。
    """
    with open(self.LIKED_SONGS_FILE, 'w', encoding='utf-8') as f:
      json.dump(self.liked_songs, f, ensure_ascii=False, indent=4, sort_keys=True)


  def save_selected_songs(self):
    """self.selected_songsの内容をローカルに保存する。jsonは少し整形。
    """
    with open(self.SELECTED_SONGS_FILE, 'w', encoding='utf-8') as f:
      json.dump(self.selected_songs, f, ensure_ascii=False, indent=4, sort_keys=True)



if __name__ == '__main__':
  sd = SavedData()
  sd.number_of_liked_songs()
    