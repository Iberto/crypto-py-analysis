import twitter_credential
from tweepy import OAuthHandler, API
import numpy as np
import pandas as pd
from textblob import TextBlob
import re


def clean_data(phrase):
    return ' '.join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", phrase).split())


class TwitterScraper:
    def __init__(self):
        self._auth = OAuthHandler(consumer_key=twitter_credential.CONSUMER_KEY, consumer_secret=twitter_credential.CONSUMER_SECRET)
        self._auth.set_access_token(key=twitter_credential.TOKEN_KEY, secret=twitter_credential.TOKEN_SECRET)
        self._client = API(self._auth)

    def search(self, query, count):
        _tweets = self._client.search(q=query, count=count)
        _tweets_df = pd.DataFrame(data=[clean_data(_tweet.text) for _tweet in _tweets], columns=['tweet'])
        _tweets_df['id'] = np.array([_tweet.id for _tweet in _tweets])
        _tweets_df['datetime'] = np.array([_tweet.created_at for _tweet in _tweets])
        _tweets_df['sentiment'] = _tweets_df.apply(lambda row: TextBlob(row.tweet).sentiment.polarity, axis=1)
        return _tweets_df
