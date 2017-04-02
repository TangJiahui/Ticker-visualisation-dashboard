from nltk.corpus import stopwords
from string import punctuation
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict


stopwords = set(stopwords.words('english') + list(punctuation))
stopwords.add("'")
stopwords.add("n't")
stopwords.add("''")
stopwords.add("``")
stopwords.add("'s")
stopwords.add("--")
min_cut = 5


def compute_frequencies(text):
    sents = sent_tokenize(text)
    word_sent = [word_tokenize(s.lower()) for s in sents]
    freq = defaultdict(int)
    for s in word_sent:
        for word in s:
            if word not in stopwords:
                freq[word] += 1
    result = []
    max_value = float(max(freq.values()))
    min_value = float(min(freq.values()))
    diff = max_value - min_value
    for i in freq:
        if freq[i] > min_cut:
            curr = {}
            curr["text"] = i
            # restrict size between 5-120
            curr["size"] = (freq[i] - min_value)/diff * (115) + 5
            result.append(curr)
    return result


