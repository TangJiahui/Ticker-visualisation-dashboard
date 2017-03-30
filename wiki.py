

import requests
import csv

def get_social_mention(ticker):
    r = requests.get("http://socialmention.com/search", params={"q": ticker, "f":'json', "t": 'all', "src[]":'twitter'})
    d = r.json()
    #soup = BeautifulSoup(d["content"])
    #text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return d["items"]


def get_wiki_url(ticker):
    company = convert_ticker_to_company([ticker])[0]
    r = requests.get("https://kgsearch.googleapis.com/v1/entities:search",params={"query": company, "key":"AIzaSyBIr5YTCZ5UopRC7DbM_8jkzTB3pNo7yRg", "limit":1})
    d = r.json()
    return d["itemListElement"][0]["result"]["detailedDescription"]["articleBody"], \
           d["itemListElement"][0]["result"]["detailedDescription"]["url"], \
           d["itemListElement"][0]["result"]["image"]["contentUrl"], \
           d["itemListElement"][0]["result"]["name"]
           #d["itemListElement"][0]["result"]["url"]


# give a list of ticker and return a list of company name
converted = {}


def convert_ticker_to_company(tickerlst):
    non_converted = []
    for i in tickerlst:
        if i not in converted:
            non_converted.append(i)
    if len(non_converted) != 0:
        r = requests.get("http://finance.yahoo.com/d/quotes.csv", params={"s": ",".join(non_converted), "f": "sn"})
        content = r.content
        reader = csv.reader(content.strip().split('\n'), delimiter=',')
        for row in reader:
            converted[row[0]] = row[1]
    result = []
    for i in tickerlst:
        result.append(converted[i])
    return result
