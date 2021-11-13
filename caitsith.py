from dotenv import dotenv_values
from dotenv import load_dotenv
import json

import spotify_info

def get_next_song():
  si = spotify_info.SpotifyInfo()
  return si.get_next_liked_song()

if __name__ == "__main__":
  # .envファイルの内容を環境変数としてos.environ辞書に追加。
  # ファイルが見つからないなら親へ親へと辿っていく
  load_dotenv()

  next_song = get_next_song()
  print(next_song)
