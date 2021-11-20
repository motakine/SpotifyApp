"""Twitter APIを使ってTwitter Botをやるクラス。"""

import tweepy
import os


class TwitterBot:
  """tweepyを使ったTwitter Botのクラス
  """
  def __init__(self, is_debug):
    """コンストラクタ。

    Args:
        is_debug (bool): デバッグとして行うならTrue, 実際に使用するならFalse。
    """
    self._consumer_key = os.environ['TWITTER_API_KEY']
    """API Key"""
    self._consumer_secret = os.environ['TWITTER_API_KEY_SECRET']
    """API Key Secret"""
    self._access_token = os.environ['TWITTER_ACCESS_TOKEN']
    """Access Token"""
    self._access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    """Access Token Secret"""
    self._bearer_token = os.environ['TWITTER_BEARER_TOKEN']
    """Bearer Token"""
    self.api = self._twitter_api_oauth_v1()
    """ツイート投稿などに使用するTwitter API。"""
    self.is_debug = is_debug
    """デバッグとして行うならTrue。投稿する文言を少し変える。"""

  def _twitter_api_oauth_v1(self):
    """OAuth 1a認証を用いたTwitter APIを返す。
    """
    auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
    auth.set_access_token(self._access_token, self._access_token_secret)
    return tweepy.API(auth)

  def tweet(self, text):
    """ツイートを行う。

    Args:
        text (str): ツイート内容
    """
    self.api.update_status(text)
  

  def tweet_a_song(self, song):
    """曲のツイートを行う。
    
    Args:
        song (dict): { 'artist': 'XXX', 'title': 'XXX', 'spotify_url': 'XXX' } の形式。
    """
    artist = song['artist']
    title = song['title']
    spotify_url = song['spotify_url']
    text_spotify = f'{artist} - {title}' + '\n' + spotify_url

    text = "@motakine キミが今日紹介するべき曲はこれにゃのだよ" + '\n\n' + text_spotify
    if self.is_debug:
      text = "これはテスト投稿にゃのさ\n" + text
    self.api.update_status(text)
    print()
    print('Tweet completed.')


from dotenv import load_dotenv
if __name__ == '__main__':
  load_dotenv()

  tb = TwitterBot()
  tb.tweet('@motakine ababababa')

