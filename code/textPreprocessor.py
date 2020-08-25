from collections import defaultdict
import nltk
# nltk.download('punkt')  # for the tokenizer
# from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
# from nltk import word_tokenize
import re

stopWordsDict = defaultdict(int)

with open('code/stopwords.txt', 'r') as f:
    for line in f:
        stopWordsDict[line.strip()] = 1


def tokenize(dta):
    # data = data.encode("ascii", errors="ignore").decode()
    return dta.split()
    # return word_tokenize(data)
    # TODO : use split() or word_tokenize() for tokenisation?


def casefold(dta):
    return dta.lower()


def remove_stopwords(dta):
    return [wrd for wrd in dta if stopWordsDict[wrd] != 1]


def stemming(dta):
    stemmer = SnowballStemmer('english')
    stemmed_words = [stemmer.stem(wrd) for wrd in dta]
    return stemmed_words


def cleanup(dta):

    # text = re.sub(r'<(.*?)>', '', data)  # Remove tags if any
    # text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text,
    #               flags=re.MULTILINE)  # Remove Url
    # text = re.sub(r'{\|(.*?)\|}', '', text, flags=re.MULTILINE)  # Remove CSS
    # text = re.sub(r'\[\[file:(.*?)\]\]', '', text, flags=re.MULTILINE)  # Remove File
    # text = re.sub(r'[.,;_()"/\'=]', ' ', text, flags=re.MULTILINE)  # Remove Punctuation
    # text = re.sub(r'[~`!@#$%&-^*+{\[}\]()":\|\\<>/?]', ' ', text, flags=re.MULTILINE)
    # return " ".join(text.split())


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

    dta = reg_url.sub('', dta)
    dta = reg_file.sub('', dta)
    dta = reg_css.sub('', dta)
    dta = reg_cite.sub(' ', dta)
    dta = reg_punct.sub('', dta)
    dta = reg_tg.sub('', dta)

    # removing html entities
    dta = re.sub(r'&nbsp;|&lt;|&gt;|&amp;|&quot;|&apos;', r' ', dta)  # removing html entities

    dta = re.sub(r'[~`!@#$%&-^*+{\[}\]()":\|\\<>/?]', ' ', dta, flags=re.MULTILINE)

    # removing special characters
    dta = re.sub(
        r'\—|\%|\$|\'|\||\.|\*|\[|\]|\:|\;|\,|\{|\}|\(|\)|\=|\+|\-|\_|\#|\!|\`|\"|\?|\/|\>|\<|\&|\\|\u2013|\n', r' ',
        dta)

    return dta

# if __name__=='__main__':
#     data = '"hello,'
#     reg_punct = re.compile(r'[.,;_()"/\']', re.DOTALL)
#     data = reg_punct.sub('', data)
#     print(data)