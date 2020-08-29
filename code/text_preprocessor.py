# import nltk
# nltk.download('punkt')  # for the tokenizer
# from nltk.corpus import stopwords
# from nltk import word_tokenize
# from nltk.stem.porter import *

from collections import defaultdict
from nltk.stem.snowball import SnowballStemmer
import re

import config

stopWordsDict = defaultdict(int)
stemmer = SnowballStemmer('english')

with open(config.STOPWORD_FILE_PATH, 'r') as f:
    for line in f:
        stopWordsDict[line.strip()] = 1


def tokenize(dta):
    return dta.split()
    # return word_tokenize(data)
    # TODO : use split() or word_tokenize() for tokenisation?


def casefold(dta):
    return dta.lower()


def remove_stopwords(dta):
    return [wrd for wrd in dta if stopWordsDict[wrd] != 1]


def word_stemming(wrd):
    return stemmer.stem(wrd)


def stemming(dta):
    return [stemmer.stem(wrd) for wrd in dta]
    # stemmer = PorterStemmer()
    # return [stemmer.stem(wrd) for wrd in dta]
    pass


def cleanup(dta):

    text = re.sub(r'<(.*?)>', '', dta)  # Remove tags if any
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text,
                  flags=re.MULTILINE)  # Remove Url
    text = re.sub(r'{\|(.*?)\|}', '', text, flags=re.MULTILINE)  # Remove CSS
    text = re.sub(r'\[\[file:(.*?)\]\]', '', text, flags=re.MULTILINE)  # Remove File
    text = re.sub(r'[.,;_()"/\'=]', ' ', text, flags=re.MULTILINE)  # Remove Punctuation
    text = re.sub(r'[~`!@#$%&-^*+{\[}\]()":|\\<>/?]', ' ', text, flags=re.MULTILINE)

    return dta
