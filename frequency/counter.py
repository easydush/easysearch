import collections
from math import log10

from index.indexer import get_paragraphs_dict, get_lemmas_and_tokens


def calculate_tokens_tf(page_tokens):
    result = dict()
    for page_number, tokens in page_tokens.items():
        tf = dict()
        counter = collections.Counter(tokens)
        for token, count in counter.items():
            tf[token] = round(count / len(tokens), 3)

        result[page_number] = tf

    return result


def calculate_tokens_idf(page_tokens):
    result = dict()
    docs_num = len(page_tokens.keys())

    for page_num, tokens in page_tokens.items():
        unique_tokens = list(set(tokens))
        idf = dict()
        for unique_token in unique_tokens:
            count = 0
            for k, v in page_tokens.items():
                if unique_token in v:
                    count += 1

            idf[unique_token] = round(log10(docs_num / count), 3)

        result[page_num] = idf

    return result


def calculate_tokens_tfidf(page_tokens_tf, page_tokens_idf):
    result = dict()

    for page_num in range(1, len(page_tokens_tf.keys()) + 1):
        tfidf = dict()
        try:
            for token, tf in page_tokens_tf[page_num].items():
                tfidf[token] = round(tf * page_tokens_idf[page_num][token], 3)
            result[page_num] = tfidf
        except KeyError:
            continue

    return result


def calculate_lemmas_tf(page_tokens_tf, page_lemmas):
    result = dict()

    for page_num, lemmas_to_tokens in page_lemmas.items():
        try:
            tf = dict()
            for lemma, tokens in lemmas_to_tokens.items():
                sum = 0
                for token in tokens:
                    sum += page_tokens_tf[page_num][token]
                tf[lemma] = sum
            result[page_num] = tf
        except KeyError:
            continue

    return result


def calculate_lemmas_idf(page_lemmas):
    result = dict()
    docs_num = len(page_lemmas.keys())

    for page_num, lemmas_to_tokens in page_lemmas.items():
        try:
            unique_lemmas = lemmas_to_tokens.keys()
            idf = dict()
            for unique_lemma in unique_lemmas:
                count = 0
                for k, v in page_lemmas.items():
                    if unique_lemma in v.keys():
                        count += 1

                idf[unique_lemma] = round(log10(docs_num / count), 3)

            result[page_num] = idf
        except KeyError:
            continue

    return result


def calculate_lemmas_tfidf(page_lemmas_tf, page_lemmas_idf):
    result = dict()

    for page_num in range(1, len(page_lemmas_tf.keys()) + 1):
        try:
            tfidf = dict()
            for lemma, tf in page_lemmas_tf[page_num].items():
                tfidf[lemma] = round(tf * page_lemmas_idf[page_num][lemma], 3)
            result[page_num] = tfidf
        except KeyError:
            continue

    return result


def generate_result_files(page_tokens_idf, page_tokens_tfidf, page_lemmas_idf, page_lemmas_tfidf):
    for i in range(1, len(page_tokens_idf) + 1):
        try:
            if page_tokens_idf[i]:
                with open(f'tokens/{i}.txt', 'w', encoding='utf-8') as file:
                    for token, token_idf in page_tokens_idf[i].items():
                        file.write(f'{token} {token_idf} {page_tokens_tfidf[i][token]}\n')
            if page_lemmas_idf[i]:
                with open(f'lemmas/{i}.txt', 'w', encoding='utf-8') as file:
                    for lemma, lemma_idf in page_lemmas_idf[i].items():
                        file.write(f'{lemma} {lemma_idf} {page_lemmas_tfidf[i][lemma]}\n')
        except KeyError:
            continue


if __name__ == '__main__':
    paragraphs_dict = get_paragraphs_dict()

    lemmas, tokens = get_lemmas_and_tokens(paragraphs_dict)

    page_tokens_tf = calculate_tokens_tf(tokens)
    page_tokens_idf = calculate_tokens_idf(tokens)
    page_tokens_tfidf = calculate_tokens_tfidf(page_tokens_tf, page_tokens_idf)

    page_lemmas_tf = calculate_lemmas_tf(page_tokens_tf, lemmas)
    page_lemmas_idf = calculate_lemmas_idf(lemmas)
    page_lemmas_tfidf = calculate_lemmas_tfidf(page_lemmas_tf, page_lemmas_idf)

    generate_result_files(page_tokens_idf, page_tokens_tfidf, page_lemmas_idf, page_lemmas_tfidf)
    print('Done')