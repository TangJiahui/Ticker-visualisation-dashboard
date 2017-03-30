import json

with open("relevant_ticker.json") as datafile:
    data = json.load(datafile)
    result = {}
    for row in data:
        result[row[0]] = row[2:]


def relevant(ticker):
    return result[ticker][1:]
