import polyglot
from polyglot.text import Text, Word


def ner(text):
    result = {i: [] for i in ('I-ORG', 'I-LOC', 'I-PER')}
    text = Text(text, hint_language_code='en')
    for entity in text.entities:
        result[entity.tag].append(' '.join(entity))
    return result
