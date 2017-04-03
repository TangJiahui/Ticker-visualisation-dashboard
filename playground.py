from flask import Flask, render_template, request, jsonify
from summarizer import *
from wiki import *
from relevant_company import *
from wordcloud import *
from social_media import *
from sentiment import *
from named_entity import *
import xml.etree.ElementTree as ET
import time

app = Flask(__name__)


# rendering templates
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summarize/')
def summarize():
    ticker = request.args['ticker']
    company_name = convert_ticker_to_company([ticker])[0]
    wiki = wiki_page(ticker)
    return render_template('dashboard.html', ticker=ticker, company_name=company_name, wiki=wiki)


@app.route('/modules/news')
def modules_news():
    ticker = request.args['ticker']
    result = get_history_summary(ticker)
    return render_template('modules/news.html', result=result)


@app.route('/modules/wordcloud')
def modules_wordcloud():
    ticker = request.args['ticker']
    result = get_history_summary(ticker)
    wordcloud = generate_wordcloud(result)
    return jsonify(wordcloud)


@app.route('/modules/sentiment')
def modules_sentiment():
    ticker = request.args['ticker']
    result = get_history_summary(ticker)
    social_tweets = tweets(ticker)
    news_sentiment = generate_sentiment(result)
    social_sentiment = generate_sentiment(social_tweets)
    return render_template("modules/sentiment.html", news_sentiment=news_sentiment, social_sentiment=social_sentiment)


@app.route('/modules/relevant')
def modules_relevant():
    ticker = request.args['ticker']
    relevant_ticker = relevant(ticker)
    relevant_comp = convert_ticker_to_company(relevant_ticker)
    relevant_t_c = zip(relevant_ticker, relevant_comp)
    return render_template("modules/relevant.html", relevant_t_c=relevant_t_c,)


@app.route('/modules/tweets')
def modules_tweets():
    ticker = request.args['ticker']
    social_tweets = tweets(ticker)
    return render_template("modules/tweets.html", social_tweets=social_tweets)


@app.route('/modules/ner')
def modules_ner():
    ticker = request.args['ticker']
    wiki = wiki_page(ticker)
    text = wiki["article"]
    entity = ner(text)
    return render_template("modules/ner.html", entity=entity)


def parse_company(ticker):
    url = "http://finance.yahoo.com/rss/headline?s=" + str(ticker)
    feed_xml = urllib2.urlopen(url).read()
    root = ET.fromstring(feed_xml)
    to_summarize = []
    for i in root.iter('item'):
        to_summarize.append(i.find('link').text)
    return to_summarize


def paste_text(result):
    text = ""
    for article in result:
        text = text + article["text"]
    return text


def generate_sentiment(result):
    return calculate_sentiment(paste_text(result))


def generate_wordcloud(result):
    return compute_frequencies(paste_text(result))


summary_history = {}


def get_history_summary(ticker):
    if ticker in summary_history:
        if time.time() > summary_history[ticker]["expiry"]:
            to_summarize = parse_company(ticker)
            result = summary(to_summarize)
            summary_history[ticker] = {}
            summary_history[ticker]["hist"] = result
            summary_history[ticker]["expiry"] = time.time() + 60 * 10
        else:
            result = summary_history[ticker]["hist"]
    else:
        to_summarize = parse_company(ticker)
        result = summary(to_summarize)
        summary_history[ticker] = {}
        summary_history[ticker]["hist"] = result
        summary_history[ticker]["expiry"] = time.time() + 60 * 10
    return result


def summary(to_summarize):
    fs = FrequencySummarizer()
    result = []
    while len(result) < 5 and len(to_summarize) > 0:
        article_url = to_summarize.pop(0)
        try:
            title, text, image, date, domain = get_only_text(article_url)
            result.append(
                {'title': title, 'text': text, 'image': image, 'points': fs.summarize(text, 3), 'url': article_url,
                 'date': date, 'domain': domain})
        except:
            continue
    return result

wiki_history = {}


def wiki_page(ticker):
    if ticker in wiki_history:
        return wiki_history[ticker]
    else:
        result = {}
        result["article"], result["url"], result["image"], result["name"] = get_wiki_url(ticker)
        wiki_history[ticker] = result
        return result


if __name__ == '__main__':
    app.run(debug=True)
