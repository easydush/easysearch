import re

import justext
import nltk
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer

pattern = re.compile("^[a-zA-Z]+$")
STOPWORDS = stopwords.words('english')


def get_paragraphs_dict():
    result = dict()

    for i in range(1, 200):
        try:
            with open(f'../pages/{i}.txt', 'rb') as file:
                paragraphs = justext.justext(file.read(), justext.get_stoplist('English'))
                p = []
                for paragraph in paragraphs:
                    if not paragraph.is_boilerplate:
                        p.append(paragraph.text)
                result[i] = p
        except FileNotFoundError:
            continue
    return result


def get_lemmas_and_tokens(paragraphs_dict):
    nltk.download('stopwords')
    nltk.download('punkt')
    pymorphy2_analyzer = MorphAnalyzer()

    lemmas = dict()
    tokens = dict()
    for page_number, paragraphs in paragraphs_dict.items():
        l = dict()
        t = list()
        for paragraph in paragraphs:
            tokens = nltk.word_tokenize(paragraph)
            lowered_tokens = [token.lower() for token in tokens]
            t += [item for item in lowered_tokens if item not in STOPWORDS and pattern.match(item)]

        for token in t:
            token_normal_form = pymorphy2_analyzer.parse(token)[0].normal_form
            if token_normal_form in l:
                if token not in l[token_normal_form]:
                    l[token_normal_form].append(token)
            else:
                l[token_normal_form] = [token, ]
        try:
            lemmas[page_number] = l
            tokens[page_number] = t
        except IndexError:
            continue

    return lemmas, tokens


def create_inverted_index(page_lemmas):
    all_lemmas = list()

    for page_num in range(1, len(page_lemmas.keys()) + 1):
        try:
            for item in page_lemmas[page_num].keys():
                all_lemmas.append(item)
        except KeyError:
            continue

    unique_lemmas = list(set(all_lemmas))
    unique_lemmas_dict_str = dict()
    unique_lemmas_dict_int = dict()

    for lemma in unique_lemmas:
        unique_lemmas_dict_int[lemma] = list()
        unique_lemmas_dict_str[lemma] = list()
        for page_num in range(1, len(page_lemmas.keys()) + 1):
            try:
                if lemma in page_lemmas[page_num].keys():
                    unique_lemmas_dict_int[lemma].append(page_num)
                    unique_lemmas_dict_str[lemma].append(str(page_num))
                    continue
            except KeyError:
                continue

    return unique_lemmas_dict_int, unique_lemmas_dict_str


def save_result_file(inverted_index_dict):
    with open('inverted_index.txt', 'w', encoding='utf-8') as file:
        for lemma, pages in inverted_index_dict.items():
            file.write(f'{lemma}: {", ".join(pages)}\n')


if __name__ == '__main__':
    paragraphs_dict = get_paragraphs_dict()
    print('Page parsed')

    lemmas, tokens = get_lemmas_and_tokens(paragraphs_dict)
    print('Lemmas and tokens were formed')

    inverted_index_dict_int, inverted_index_dict_str = create_inverted_index(lemmas)
    print('Inverted index formed')

    save_result_file(inverted_index_dict_str)
    print('Result file saved')
