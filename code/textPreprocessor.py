import re

from collections import defaultdict
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


stopWords = set(stopwords.words('english'))
stopWordsDict = defaultdict(int)
for word in stopWords:
    stopWordsDict[word] = 1


def tokenize(data):
    # data = data.encode("ascii", errors="ignore").decode()
    return data.split()


def casefold(data):
    return data.lower()


def remove_stopwords(data):
    return [wrd for wrd in data if stopWordsDict[wrd] != 1]


def stemming(data):
    stemmer = SnowballStemmer('english')
    stemmed_words = [stemmer.stem(wrd) for wrd in data]
    return stemmed_words


def cleanup(data):
    # Regular Expression to remove URLs
    reg_url = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.DOTALL)

    # Regular Expression to remove [[file:]]
    reg_file = re.compile(r'\[\[file:(.*?)\]\]', re.DOTALL)

    # Regular Expression to remove CSS
    reg_css = re.compile(r'{\|(.*?)\|}', re.DOTALL)

    # Regular Expression to remove {{cite **}} or {{vcite **}}
    reg_cite = re.compile(r'{{v?cite(.*?)}}', re.DOTALL)

    # Regular Expression to remove Punctuation
    reg_punct = re.compile(r'[.,;_()"/\']', re.DOTALL)

    # Regular Expression to remove <..> tags from text
    reg_tg = re.compile(r'<(.*?)>', re.DOTALL)

    data = reg_url.sub('', data)
    data = reg_file.sub('', data)
    data = reg_css.sub('', data)
    data = reg_cite.sub(' ', data)
    data = reg_punct.sub('', data)
    data = reg_tg.sub('', data)

    # removing html entities
    data = re.sub(r'&nbsp;|&lt;|&gt;|&amp;|&quot;|&apos;', r' ', data)  # removing html entities

    data = re.sub(r'[~`!@#$%&-^*+{\[}\]()":\|\\<>/?]', ' ', data, flags=re.MULTILINE)

    # removing special characters
    data = re.sub(
        r'\—|\%|\$|\'|\||\.|\*|\[|\]|\:|\;|\,|\{|\}|\(|\)|\=|\+|\-|\_|\#|\!|\`|\"|\?|\/|\>|\<|\&|\\|\u2013|\n', r' ',
        data)

    return data