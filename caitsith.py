"""メインとなるモジュール。このモジュールを実行してアプリを実行する。
まずGoogle Driveにアクセスし、最終実行日時が今日の実行予定時刻より前であることを確認。

"""

from dotenv import dotenv_values
from dotenv import load_dotenv
import os, json

import spotify_info
import slack_bot
import twitter_bot


class CaitSith:
  """アプリ全体の実行を行うクラス。"""
  def __init__(self, is_debug, is_local):
    """アプリを実行する。

    Args:
        is_debug (bool): デバッグとして実行するならTrue。Slackで投稿するチャンネル、Twitterで投稿する文言なども変更する。
        is_local (bool): ローカルのjsonファイルを使用するならTrue, Google Drive上のものを使用するならFalse。
    """
    # .envファイルの内容を環境変数としてos.environ辞書に追加。
    # ファイルが見つからないなら親へ親へと辿っていく
    load_dotenv()

    self.next_song = self._get_next_song(is_local)
    """今日紹介する曲。形式は辞書 { 'artist': 'XXX', 'title': 'XXX', 'spotify_url': 'XXX' } 。
    """
    self.is_allowed_to_run = not (self.next_song == None)
    """今アプリを実行して良いかどうか。今日の実行分が既に終わっているなどでFalseとなる。
    """
    if not self.is_allowed_to_run:
      print()
      print('Already ran the app today...')
      return
    
    print()
    print('Got a new song!')
    
    self.slack_bot = slack_bot.SlackSdk(is_debug)
    self.slack_bot.post_a_song(self.next_song)
    self.twitter_bot = twitter_bot.TwitterBot(is_debug)
    self.twitter_bot.tweet_a_song(self.next_song)


  def _get_next_song(self, is_local):
    """自分のSpotifyアカウントのLiked Songsから1曲ランダムに取得して情報を返す。重複なし。
    Returns:
        song: { 'artist': 'XXX', 'title': 'XXX', 'spotify_url': 'XXX' } の形式。
    """
    si = spotify_info.SpotifyInfo(is_local)
    return si.get_next_liked_song()


if __name__ == "__main__":
  caitsith = CaitSith(is_debug=False, is_local=False)
  # caitsith.slack_bot.post_a_song(caitsith.next_song)
  # caitsith.twitter_bot.something()
