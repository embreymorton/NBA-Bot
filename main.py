import random
from concurrent.futures import ThreadPoolExecutor
from other import keys
import tweepy
from tweetList import tweet_args

# Authenticate with Twitter API using keys from other module
auth = tweepy.OAuthHandler(keys.api_key, keys.api_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


class Tweet:
    """
    A class representing a tweet object, containing text and optional media (image or video)
    """
    def __init__(self, text, image_path=None, video_path=None):
        """
        Initialize a Tweet object with given text and optional media files
        :param text: str, the text content of the tweet
        :param image_path: str, path to an image file (default=None)
        :param video_path: str, path to a video file (default=None)
        """
        self.text = text
        self.image_path = [api.media_upload(image_path).media_id] if image_path else []
        self.video_path = [
            api.media_upload(video_path, chunked=True, media_category="tweet_video").media_id] if video_path else []

    def tweet(self):
        """
        Post the tweet to Twitter with optional media files
        """
        media_ids = self.image_path + self.video_path if self.image_path or self.video_path else None
        api.update_status(self.text, media_ids=media_ids)
        print("Tweeted Successfully")


def create_tweet(args):
    return Tweet(*args)


# Create Tweet objects for each tweet argument using ThreadPoolExecutor
with ThreadPoolExecutor() as executor:
    tweet_objects = executor.map(create_tweet, tweet_args)

# Convert the generator object to a list for random selection
tweets_to_post = list(tweet_objects)

# Choose a random tweet to post and post it
if __name__ == '__main__':
    random_tweet = random.choice(tweets_to_post)
    random_tweet.tweet()
