from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from pymorphy2 import MorphAnalyzer
import numpy as np
import re
from scipy import spatial

pattern = re.compile("^[a-zA-Z]+$")
STOPWORDS = stopwords.words('english')
indexes = {}

class Searcher:
    def __init__(self):
        self.lemmas, self.matrix = self.load_index()
        with open('../index.txt') as ind:
            items = ind.readlines()
            for item in items:
                key, value, other = item.split(' ')
                indexes[key] = value
        nltk.download('punkt')
        nltk.download('stopwords')
        self.pymorphy2_analyzer = MorphAnalyzer()

    def load_index(self):
        with open('../index/inverted_index.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()

        lemmas_list = list()
        matrix = [[0] * 500 for _ in range(len(lines))]
        for idx, line in enumerate(lines):
            line = re.sub('\n', '', line)
            lemma = line.split(': ')[0]
            lemmas_list.append(lemma)
            pages = line.split(': ')[1].split(', ')
            for page in pages:
                matrix[idx][int(page) - 1] = 1

        return lemmas_list, np.array(matrix).transpose()

    def get_vector(self, search_string):
        search_tokens = word_tokenize(search_string)
        lowered_tokens = [line_token.lower() for line_token in search_tokens]
        cleaned_search_tokens = [item for item in lowered_tokens if item not in STOPWORDS and pattern.match(item)]

        tokens_normal_form = [self.pymorphy2_analyzer.parse(token)[0].normal_form for token in cleaned_search_tokens]
        vector = [0] * len(self.lemmas)
        for token in tokens_normal_form:
            if token in self.lemmas:
                vector[self.lemmas.index(token)] = 1

        return vector

    def search(self, search_string):
        vector = self.get_vector(search_string)

        docs = dict()
        for idx, doc in enumerate(self.matrix):
            if max(doc) == 1:
                docs[idx + 1] = 1 - spatial.distance.cosine(vector, doc)
            else:
                docs[idx + 1] = 0.0

        sorted_docs = sorted(docs.items(), key=lambda x: x[1], reverse=True)
        print(indexes)
        indexed_docs = [(indexes.get(str(doc[0])), doc) for doc in sorted_docs]
        return indexed_docs


if __name__ == '__main__':
    searcher = Searcher()
    print(searcher.search(str(input('Type your query:\n'))))
