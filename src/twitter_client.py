import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

def get_twitter_clients():
    # v1.1 client for media upload (OAuth 1.0a)
    auth = tweepy.OAuth1UserHandler(
        os.getenv("TWITTER_API_KEY"),
        os.getenv("TWITTER_API_SECRET"),
        os.getenv("TWITTER_ACCESS_TOKEN"),
        os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    )
    api_v1 = tweepy.API(auth)

    # v2 client for posting the tweet
    client_v2 = tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    )

    return api_v1, client_v2

def post_tweet(api_v1, client_v2, text, image_path=None):
    media_id = None

    if image_path and os.path.exists(image_path):
        media = api_v1.media_upload(filename=image_path)
        media_id = media.media_id

    if media_id:
        tweet = client_v2.create_tweet(text=text, media_ids=[media_id])
    else:
        tweet = client_v2.create_tweet(text=text)

    return tweet