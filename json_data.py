import copy, json, os, random
from datetime import datetime, timezone, timedelta
import google_drive

class JsonData:
  """ドライブ上あるいはローカルに保存されたjsonファイルを扱うクラス。今日の実行分が終わっているかどうかの判定もこのクラスで行う。
  """
  JSON_DEFAULT = dict()
  JSON_SONGS_DEFAULT = { 'items': []}

  def __init__(self, is_local):
    """コンストラクタ。

    Args:
        is_local (bool): ローカルのjsonファイルを使用するならTrue, Google Drive上のものを使用するならFalse。
    """
    self.CONFIG_FILE = r'json\config.json' if is_local else os.environ.get('APP_CONFIG_JSON')
    """アプリ全体の設定jsonファイルのパス
    """
    self.LIKED_SONGS_FILE = r'json\liked_songs.json' if is_local else os.environ.get('APP_LIKED_SONGS_JSON')
    """ローカルに保存されたLiked Songsの情報が格納されたjsonファイルのパス
    """
    self.SELECTED_SONGS_FILE = r'json\selected_songs.json' if is_local else os.environ.get('APP_SELECTED_SONGS_JSON')
    """これまで選択した曲の情報が格納されたjsonファイルのパス
    """
    self.config_dict = copy.deepcopy(JsonData.JSON_DEFAULT)
    """アプリ全体の設定jsonファイルの辞書。編集はJsonDataクラスのメソッドから行いたい。
    """
    self.liked_songs_dict = copy.deepcopy(JsonData.JSON_SONGS_DEFAULT)
    """ローカルに保存されたLiked Songsの辞書。編集はJsonDataクラスのメソッドから行いたい。
    """
    self.selected_songs_dict = copy.deepcopy(JsonData.JSON_SONGS_DEFAULT)
    """これまで選択した曲の辞書。編集はJsonDataクラスのメソッドから行いたい。
    """
    self.google_drive = None
    """Google Drive APIを使用するときのGoogleDriveクラス。is_local=Trueなら使用しない。
    """
    self.is_local = is_local
    """ローカルのjsonファイルを使用するならTrue, Google Drive上のものを使用するならFalse。
    """
    self.is_allowed_to_run = True
    """「次回実行予定時刻 <= 現在の時刻」であり、今アプリを実行して良いならTrue。configファイルを読み込んでから判定を行う。
    """
    if not self.is_local:
      self.google_drive = google_drive.GoogleDrive()
    
    self._load_json_file(self.CONFIG_FILE, self.config_dict, self.CONFIG_FILE)
    self.is_allowed_to_run = self._check_if_allowed_to_run()

    # 実行して良くないのならLiked Songsやこれまで選択した曲を読み込まず処理を終える。
    if not self.is_allowed_to_run:
      return

    self._load_json_file(self.LIKED_SONGS_FILE, self.liked_songs_dict, self.LIKED_SONGS_FILE)
    self._load_json_file(self.SELECTED_SONGS_FILE, self.selected_songs_dict, self.SELECTED_SONGS_FILE)

  
  def select_a_song_from_liked_songs(self):
    """Liked Songsの中から選択したことのないものを一つランダムに選んで返す。
       それに伴って選んだ曲をこれまで選択した曲に追加し、ファイルに保存する。
       加えて最終実行日時も更新し、configファイルを保存する。
    """
    # この関数を呼び出しているクラス内ですでに対策は行われているはずだが、
    # ここでも一応今日の実行分が終わっているかどうかの判定を行っておく。
    if not self.is_allowed_to_run:
      return None

    not_selected_songs = [i for i in self.liked_songs_dict['items'] if i not in self.selected_songs_dict['items']]

    # 選択したことのない曲が存在しなければ、これまで選択した曲をリセットしてやり直す。
    if len(not_selected_songs) == 0:
      self.clear_dict(self.selected_songs_dict, is_songs=True)
      not_selected_songs = [i for i in self.liked_songs_dict['items'] if i not in self.selected_songs_dict['items']]

    # ランダムに1曲取り出し、これまで選択した曲を保存する。
    song = random.choice(not_selected_songs)
    self.append_dict_song(self.selected_songs_dict, song)
    self.sort_selected_songs()
    self._save_json_file(self.SELECTED_SONGS_FILE, self.selected_songs_dict)

    # 最終実行日時を更新し、configファイルを保存する。
    date_dt_now = datetime.now(timezone(timedelta(hours=9)))
    DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S %z'
    self.config_dict['last_run'] = datetime.strftime(date_dt_now, DATETIME_FORMAT)
    self._save_json_file(self.CONFIG_FILE, self.config_dict)
    return song


  def number_of_dict_songs(self, json_dict):
    """曲が格納された辞書に格納された曲数を返す。

    Args:
        json_dict (dict): 曲が入っているjson辞書。
    """
    return len(json_dict['items'])


  def sort_liked_songs(self):
    """self.liked_songs_dictの内容をアーティスト名、タイトル、URLの順に昇順ソートする。大文字小文字は区別しない。
    """
    self.liked_songs_dict['items'] = sorted(self.liked_songs_dict['items'], key=lambda x:(x['artist'].lower(), x['title'].lower(), x['spotify_url'].lower()))

  
  def sort_selected_songs(self):
    """self.selected_songs_dictの内容をアーティスト名、タイトル、URLの順に昇順ソートする。大文字小文字は区別しない。
    """
    self.selected_songs_dict['items'] = sorted(self.selected_songs_dict['items'], key=lambda x:(x['artist'].lower(), x['title'].lower(), x['spotify_url'].lower()))


  def append_dict_song(self, json_dict, song):
    """曲が格納された辞書に内容（曲）を追加する。

    Args:
        json_dict (dict): 曲が格納された辞書。
        song (dict): { 'artist': 'XXX', 'title': 'XXX', 'spotify_url': 'XXX' } の形式。
    """
    json_dict['items'].append(song)


  def clear_dict(self, json_dict, is_songs=False):
    """json辞書の内容を初期化し、引数に渡した辞書に反映させる。

    Args:
        json_dict (dict): 初期化する辞書
        is_songs (bool): 辞書が格納する情報が曲であるかどうか
    """
    json_dict.clear()
    if is_songs:
      json_dict.update(copy.deepcopy(JsonData.JSON_SONGS_DEFAULT))


  def _load_json_file(self, filepath, json_dict, file_name_str=''):
    """指定したパスからjson辞書に内容を読み込む。self.is_local == Falseならjsonファイルのダウンロードを前もって行う。

    Args:
        filepath (str): 読み込むjsonファイルのパス。
        json_dict (dict): jsonファイルから内容を読み込み格納する辞書。
        file_name_str (str): ファイルが見つからなかった時にこのjsonファイルを出力したとprintする時に\
            使用するjsonファイルの名前。
    """
    # ドライブ上のjsonファイルを使用する場合はダウンロードを行う。
    if not self.is_local:
      self.google_drive.Download_File_from_Appdir(filepath)

    # 再代入すると参照が外れるので注意。
    self.clear_dict(json_dict)
    # ファイルが存在せず開けなかった場合は辞書はデフォルトのままで、エラーメッセージを出力する。
    try:
      with open(filepath, 'r', encoding='utf-8') as f:
        json_dict.update(json.load(f))
    except FileNotFoundError as e:
      print(e)
      file_name_str = file_name_str if file_name_str == '' else ' ' + file_name_str
      print(f"Not found a local{file_name_str} file.")
      print()
    # Liked Songsに曲が追加されるだけで選択した曲情報が初期化されるとかだと困る、のとはまた別の話。


  def _save_json_file(self, filepath, json_dict):
    """指定したパスにjson辞書の内容を保存する。self.is_local == Falseならjsonファイルのアップロード（更新）を最後に行う。

    Args:
        filepath (str): 保存するjsonファイルのパス。
        json_dict (dict): jsonファイルに保存する内容となる辞書。
    """
    with open(filepath, 'w', encoding='utf-8') as f:
      json.dump(json_dict, f, ensure_ascii=False, indent=4, sort_keys=True)
    
    if not self.is_local:
      self.google_drive.Update_File(filepath)


  def save_json_file_liked_songs(self):
    """Liked Songsのjson辞書の内容を保存する。self.is_local == Falseならjsonファイルのアップロード（更新）を最後に行う。
    """
    self._save_json_file(self.LIKED_SONGS_FILE, self.liked_songs_dict)


  def _check_if_allowed_to_run(self):
    """configファイルを読み込んでいることを前提に、今アプリを実行して良いかどうかを返す。
    具体的には「次回実行予定時刻 <= 現在の時刻」の場合のみ、
    乃ち「最終実行日時の次の実行予定時刻 <= 現在の時刻」の場合のみTrueを返す。

    Returns:
        bool: 今アプリを実行して良いかどうか。
    """
    DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S %z'
    DATE_FORMAT = '%Y/%m/%d'
    date_dt_last = datetime.strptime(self.config_dict.get('last_run'), DATETIME_FORMAT)
    date_dt_now = datetime.now(timezone(timedelta(hours=9)))
    # 取り敢えず最終実行日に実行予定時刻を繋げる
    date_str_run = date_dt_last.strftime(DATE_FORMAT) + ' ' + self.config_dict.get('time_to_run')
    date_dt_run = datetime.strptime(date_str_run, DATETIME_FORMAT)
    # 最終実行日時がその日の実行予定時刻を過ぎていた場合、その翌日が次回実行予定時刻になる
    if date_dt_run < date_dt_last:
      date_dt_run += timedelta(days=1)
    return date_dt_run <= date_dt_now


if __name__ == '__main__':
  # sd = JsonData(is_local=False)
  # tmp = sd.number_of_dict_songs(sd.liked_songs_dict)
  # print(tmp)

  # # datetimeモジュールを使ってみる
  # DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S %z'
  # date_dt_now = datetime.now(timezone(timedelta(hours=9)))
  # time_str_run = '06:00:00 +0900'
  # date_str_run = date_dt_now.strftime('%Y/%m/%d') + " " + time_str_run
  # date_dt_run = datetime.strptime(date_str_run, DATETIME_FORMAT)
  # print(f"run < now = {date_dt_run < date_dt_now}")
  # date_dt_str = datetime.strftime(date_dt_run, DATETIME_FORMAT)
  # print(date_dt_str)
  print(os.path.join('json', 'ajajaj.json'))
    