import tweepy
import os


class TwitterBot:
  """tweepyを使ったTwitter Botのクラス
  """
  def __init__(self):
    self.consumer_key = os.environ['TWITTER_API_KEY']
    self.consumer_secret = os.environ['TWITTER_API_KEY_SECRET']
    self.access_token = os.environ['TWITTER_ACCESS_TOKEN']
    self.access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    self.bearer_token = os.environ['TWITTER_BEARER_TOKEN']
    self.api = self.twitter_api_oauth_v1()

  def twitter_api_oauth_v1(self):
    """OAuth 1a認証を用いたTwitter APIを返す。
    """
    auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
    auth.set_access_token(self.access_token, self.access_token_secret)
    return tweepy.API(auth)

  def tweet(self, text):
    self.api.update_status(text)


from dotenv import load_dotenv
if __name__ == '__main__':
  load_dotenv()

  tb = TwitterBot()
  tb.tweet('テストにゃのだよ')

