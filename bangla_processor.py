from functools import singledispatch
from collections import abc
import re
import codecs

global invalid_start_word, kars
BANGLA_UNICODE = '[\\u0980-\\u09FF]+'
NOT_BANGLA_UNICODE = '[^\\u0980-\\u09FF ]+'
NOT_BANGLA_UNICODE_PUNCTUATION = '[^\\u0980-\\u09FF ,;।?!:(){}\-[\]\n]+'
invalid_start_word = "ািীুূৃৄেৈোৌৗয়ৎঁঃংঢ়য়ঙঞড়ণ়্৥"
kars = invalid_start_word[:11]


@singledispatch
def re_extract_bangla_sentence(obj, punctuation=False):
    """
    Extract Bangla content from a given sentence
    :param punctuation: (bool) whether to include punctuation
    :param obj: data
    :return: Bangla text in input formet
    """
    return None


@re_extract_bangla_sentence.register
def _(text: str, punctuation=False):
    if punctuation:
        bangla_text = re.sub(NOT_BANGLA_UNICODE_PUNCTUATION, '', text)
    else:
        bangla_text = re.sub(NOT_BANGLA_UNICODE, '', text)
    return bangla_text


@re_extract_bangla_sentence.register
def _(sentences: abc.MutableSequence, punctuation=False):
    return [re_extract_bangla_sentence(s, punctuation) for s in sentences]


def word_tokenizer_bangla(sentence):
    """
    List of words from sentence
    :param sentence: string
    :return: list of words
    """
    return re.findall(BANGLA_UNICODE, sentence)


def sentence_tokenizer_bn(paragraph):
    """
    Tokenize paragraph in to sentence
    :param paragraph: (str) input
    :return: list of split sentences
    """
    paragraph = paragraph.strip()
    all_splitted_sentences = []

    for sentence in paragraph.split('\n'):
        sentences = sentence.split('।')
        # add the dari to the sentences
        for i in range(len(sentences) - 1):
            sentences[i] = sentences[i] + '।'

        for s in sentences:
            if '?' in s:
                s_1 = s.split('?')
                for i in range(len(s_1) - 1):
                    s_1[i] = s_1[i] + '?'

                for s_1_s in s_1:
                    if '!' in s_1_s:
                        s_2 = s_1_s.split('!')
                        for i in range(len(s_2) - 1):
                            s_2[i] = s_2[i] + '!'
                        all_splitted_sentences.extend(s_2)

                    else:
                        all_splitted_sentences.append(s_1_s)
            elif '!' in s:
                s_2 = s.split('!')
                for i in range(len(s_2) - 1):
                    s_2[i] = s_2[i] + '!'
                all_splitted_sentences.extend(s_2)
            else:
                all_splitted_sentences.append(s)

    return [s.strip() for s in all_splitted_sentences if len(s.strip()) > 0]


def load_all_dict_words():
    """
    Loads all dictionary words
    :return: list of words
    """

    bangla_pedia_dict = []
    with codecs.open('data/words/dictionary/bangla_pedia.txt', mode='r', encoding='utf-8') as f:
        for line in f:
            bangla_pedia_dict.append(line.split(' ')[0])

    long_dict = []
    with codecs.open('data/words/dictionary/long_dict.txt', mode='r', encoding='utf-8') as f:
        for line in f:
            long_dict.append(line[:-2])

    bangla_academy_dict = []
    with codecs.open('data/words/dictionary/bangla_academy.txt', mode='r', encoding='utf-8') as f:
        for line in f:
            bangla_academy_dict.append(line[:-2])

    libreoffice_dict = []
    with codecs.open('data/words/dictionary/libreoffice.txt', mode='r', encoding='utf-8') as f:
        for line in f:
            if '\u200c' not in line[:-2]:
                libreoffice_dict.append(line[:-2])

    avro_dict = []
    with codecs.open('data/words/dictionary/avrodict.txt', mode='r', encoding='utf-8') as f:
        for line in f:
            avro_dict.append(line[:-1])

    sanshod_dict = []
    with codecs.open('data/words/dictionary/sanshod_dict.txt', mode='r', encoding='utf-8') as f:
        for line in f:
            sanshod_dict.append(line[:-1])

    marged = sanshod_dict+avro_dict+libreoffice_dict+bangla_academy_dict
    return list(set([s for s in marged if '়' not in s and 'ো' not in s]))


if __name__ == '__main__':
    text = 'বামাকো, ১৯ জুলাই, ২০১৯ (বাসস) : \nমালির উত্তরপূবা\u200cর্ঞ্চলে নাইজার সীমান্েতর কাছে এক অতর্কিত হামলায় ১ ' \
           'সৈন্য নিহত ও অপর ২ জন আহত হয়েছে,;।?!:-“”(){}[] '
    print(re_extract_bangla_sentence(text))
    print(re_extract_bangla_sentence(text, punctuation=True))
