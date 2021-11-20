from dotenv import dotenv_values
from dotenv import load_dotenv
import json

import spotify_info
import slack_bot
import twitter_bot

class CaitSith:
  def __init__(self, is_debug=True):
    # .envファイルの内容を環境変数としてos.environ辞書に追加。
    # ファイルが見つからないなら親へ親へと辿っていく
    load_dotenv()

    self.next_song = self.get_next_song()
    self.slack_bot = slack_bot.SlackSdk(is_debug)
    # self.twitter_bot = twitter_bot.TwitterBot()

  def get_next_song(self):
    """自分のSpotifyアカウントのLiked Songsから1曲ランダムに取得して情報を返す。重複なし。
    Returns:
        song: { 'artist': 'XXX', 'title': 'XXX', 'spotify_url': 'XXX' } の形式。
    """
    si = spotify_info.SpotifyInfo()
    return si.get_next_liked_song()


if __name__ == "__main__":
  caitsith = CaitSith(is_debug=False)
  caitsith.slack_bot.post_a_song(caitsith.next_song)
  # caitsith.twitter_bot.something()
