import textblob


def calculate_sentiment(text):
    blob = textblob.TextBlob(text)
    try:
        lan = blob.detect_language()
    except:
        lan = ''
    if lan == 'en':
        return blob.sentiment.polarity