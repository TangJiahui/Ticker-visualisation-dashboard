from flask import Flask
from flask import render_template
from flask import request
from summarizer import *
from wiki import *
from relevant_company import *
from wordcloud import *
from social_media import *
import xml.etree.ElementTree as ET
import time

app = Flask(__name__)


# add variable parts to URL
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


# Http methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()


def do_the_login():
    return None


def show_the_login_form():
    return None


# static files
# url_for('static', filename='style.css')


# rendering templates
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wordcloud/')
def wordcloud():
    return render_template('wordcloud.html')


def parse_company(ticker):
    url = "http://finance.yahoo.com/rss/headline?s=" + str(ticker)
    feed_xml = urllib2.urlopen(url).read()
    root = ET.fromstring(feed_xml)
    to_summarize = []
    for i in root[0].iter('item'):
        to_summarize.append(i[1].text)
    return to_summarize


def parse_bbc():
    feed_xml = urllib2.urlopen('http://feeds.bbci.co.uk/news/rss.xml').read()
    feed = BeautifulSoup(feed_xml.decode('utf8'))
    to_summarize = map(lambda p: p.text, feed.find_all('guid'))
    return to_summarize


@app.route('/summarize/')
def summarize():
    ticker = request.args['ticker']
    company_name = convert_ticker_to_company(ticker)[0]
    social_tweets = tweets(ticker)
    result = get_history_summary(ticker)
    wiki = wiki_page(ticker)
    relevant_ticker = relevant(ticker)
    relevant_comp = convert_ticker_to_company(relevant_ticker)
    relevant_t_c = zip(relevant_ticker, relevant_comp)
    wordcloud = generate_wordcloud(result)
    return render_template('dashboard.html', ticker=ticker, company_name=company_name, result=result,
                           wiki=wiki, relevant_t_c=relevant_t_c, wordcloud=wordcloud, social_tweets=social_tweets)


def generate_wordcloud(result):
    text = ""
    for article in result:
        text = text + article["text"]
    return compute_frequencies(text)


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
        # social = social_mention(ticker)
    return result


def summary(to_summarize):
    fs = FrequencySummarizer()
    result = []
    while len(result) < 5:
        try:
            article_url = to_summarize.pop(0)
            title, text, image, date, domain = get_only_text(article_url)
            result.append(
                {'title': title, 'text': text, 'image': image, 'points': fs.summarize(text, 3), 'url': article_url,
                 'date': date, 'domain': domain})
        except:
            pass
    return result


# def social_mention(ticker):
#     items = get_social_mention(ticker)
#     result = []
#     for i in items:
#         result.append({'title': i['title'], 'description': i['description'], 'link': i['link'], 'timestamp': i['timestamp'], 'user': i['user'], 'source': i['source']})
#     return result


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
