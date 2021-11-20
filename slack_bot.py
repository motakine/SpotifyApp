import logging, os
from slack_sdk import WebClient


class SlackSdk:
  """slack_sdkを使ったSlack Botのクラス"""
  def __init__(self, is_debug=True):
    """コンストラクタ。

    Args:
        is_debug (bool): デバッグとして行うならTrue, 実際に使用するならFalse。
    """
    if is_debug:
      # デバッグレベルのログを出力
      logging.basicConfig(level=logging.DEBUG)
    
    # Web API クライアントを初期化
    self.client = WebClient(os.environ["SLACK_BOT_TOKEN"])
    # 投稿するチャンネル
    self.channel = '#motakine-lab' if is_debug else '#motakineめっも'


  def post_a_message(self, text):
    """メッセージを投稿する。

    Args:
        text (str): 投稿するメッセージ。
    """
    response = self.client.chat_postMessage(
      channel=self.channel,
      text=text
    )


  def post_a_song(self, song):
    """曲の紹介を要求するメッセージを投稿する。

    Args:
        song (dict): { 'artist': 'XXX', 'title': 'XXX', 'spotify_url': 'XXX' } の形式。
    """
    artist = song['artist']
    title = song['title']
    spotify_url = song['spotify_url']
    text_spotify = f'{artist} - {title}' + '\n' + spotify_url

    self.post_a_message('キミが今日紹介するべき曲はこれにゃのだよ' + '\n\n' + text_spotify)
    print()
    print('Post to Slack completed.')


  def post_input_messages(self):
    """コンソールで入力した文字列を投稿していく。
    """
    # chat.postMessage API を呼び出す
    response = self.client.chat_postMessage(
      channel=self.channel,
      text=":ultimate_tippy",
    )

    while True:
      text = input('>> ')
      response = self.client.chat_postMessage(
        channel=self.channel,
        text=text,
      )


class SlackBolt:
  """slack-boltを使ったSlack Botのクラス"""
  pass


