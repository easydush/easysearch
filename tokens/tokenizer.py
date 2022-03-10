import os.path

import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
import re

pattern = re.compile("^[a-zA-Z]+$")
NLTK_PACKAGES = ['tokenizers/punkt', 'corpora/stopwords', 'corpora/wordnet', 'corpora/omw-1.4']
STOPWORDS = stopwords.words('english')


def tokenize(text):
    tokens = []

    tokens += nltk.word_tokenize(text)
    lowered_tokens = [token.lower() for token in tokens]
    return [item for item in lowered_tokens if item not in STOPWORDS and pattern.match(item)]


def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    lemma_token = dict()

    for token in tokens:
        lemmatized = lemmatizer.lemmatize(token)

        mapped_tokens = lemma_token.get(lemmatized, [])
        mapped_tokens.append(token)

        lemma_token[lemmatized] = mapped_tokens
    return lemma_token


def scan_nltk_packages():
    for package in NLTK_PACKAGES:
        try:
            nltk.find(package)
        except Exception:
            nltk.download(package.split('/')[1])


if __name__ == '__main__':
    scan_nltk_packages()

    tokens = set()
    for page in os.listdir('../pages'):
        with open(os.path.join('../pages', page), encoding='UTF-8') as f:
            tokens.update(set(tokenize(f.read())))

    tokens = set(tokens)

    with open('./tokens.txt', mode='wt', encoding='utf-8') as file:
        file.write('\n'.join(tokens))

    lemma_token = lemmatize(tokens)
    with open('./lemmas.txt', mode='at', encoding='utf-8') as file:
        for key, value in lemma_token.items():
            file.write(f'{key}: {value}\n')
