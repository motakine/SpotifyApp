import logging, os
from slack_sdk import WebClient


class SlackSdk:
  """slack_sdkを使ったSlack Botのクラス"""
  def __init__(self, is_debug=True):
    if is_debug:
      # デバッグレベルのログを出力
      logging.basicConfig(level=logging.DEBUG)
    
    # Web API クライアントを初期化
    self.client = WebClient(os.environ["SLACK_BOT_TOKEN"])
    # 投稿するチャンネル
    self.channel = '#motakine-lab' if is_debug else '#motakineめっも'


  def post_a_message(self, text):
    response = self.client.chat_postMessage(
      channel=self.channel,
      text=text
    )


  def post_a_song(self, song):
    artist = song['artist']
    title = song['title']
    spotify_url = song['spotify_url']
    text_spotify = f'{artist} - {title}' + '\n' + spotify_url

    self.post_a_message('キミが今日紹介するべき曲はこれにゃのだよ' + '\n\n' + text_spotify)


  def post_input_messages(self):
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


