import tweepy

auth = tweepy.OAuthHandler("lDu9lefDsfn4zhL2SYbfNN4Aw", "X0HG5wTNmyo7zag5CUUCiev6p3o19Ims6nWlgCAwqNBC7LqjAV")
auth.set_access_token("489069042-okCFCkRDlchl9uuuDBEYD81Mb4UIifsNVk784MzY",
                      "8WV77xawZPpYFCq5KZH9MCYkg5ocvZLpiLeNFjWTvKPMj")

api = tweepy.API(auth)


def tweets(query):
    public_tweets = api.search(query + "-filter:retweets")
    tweet_list = []
    for tweet in public_tweets:
        tweet_list.append({"name": tweet.author.name, "image": tweet.author.profile_image_url,
                           "text": tweet.text, "id": tweet.id, "screen_name": tweet.author.screen_name})
    return tweet_list
