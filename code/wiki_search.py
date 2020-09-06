from collections import defaultdict
import re
import timeit

import config
from text_preprocessor import tokenize, stemming, remove_stopwords, cleanup
from ranker import rank
from search_helper import find_docs, find_file_no, fetch_doc_titles

vocab_offset = []
title_offset = []


def search_field_query(words, fields, fptr_vocab):
    doc_list = defaultdict(dict)
    doc_freq = {}
    for i in range(len(words)):
        word = words[i]
        field = fields[i]
        # print("WORD: "+word + " field: "+field)
        docs, _ = find_file_no(0, len(vocab_offset), vocab_offset, word, fptr_vocab)
        '''
        docs will contain 2 things:
        1. the file no. to look into for the word 'word' (say its 2. Then look into t2.txt, b2.txt, i2.txt, r2.txt, 
        l2.txt, c2.txt)
        2. The count of documents/wiki pages in which the word 'word' occurs
        
        And say we look into b2.txt (later), then it is there that we'll find the exact 9 doc numbers in which the word 
        occurs, along with the freq of the word in each of the 9 docs
        '''
        print('DOCS', docs)
        if len(docs) > 0:
            file_no = docs[0]
            filename = config.OUTPUT_FOLDER_PATH + field + str(file_no) + '.txt'
            fptr_field_file = open(filename, 'r')
            returned_docs_list, df = find_docs(fptr_field_file, file_no, field, word)
            '''
            df: it'll be a single no; it'll be the no. of documents in which the word 'word' appears
            
            returned_docs_list: it will have 'df*2' elements or rather 'df' pairs of elements. 
            Each pair will have the doc no. and the count of occ of the word in that doc
            Mind that this count and the doc num will be field specific. i.e if field if 't' then only those doc nums
            are given where the 'word' occurs in title, and accordingly. the count is the no of occ of the word in the 
            title of that doc
            '''
            doc_list[word][field] = returned_docs_list
            doc_freq[word] = df
    return doc_list, doc_freq


def search_simple_query(words, fptr_vocab):
    doc_list = defaultdict(dict)
    doc_freq = {}
    fields = ['t', 'b', 'i', 'c', 'r', 'l']
    for word in words:
        docs, _ = find_file_no(0, len(vocab_offset), vocab_offset, word, fptr_vocab)
        print('DOCS', docs)
        if len(docs) > 0:
            file_no = docs[0]
            doc_freq[word] = docs[1]
            for field in fields:
                print("WORD: ", word, " FIELD: ", field)
                filename = config.OUTPUT_FOLDER_PATH + field + str(file_no) + '.txt'
                fptr_field_file = open(filename, 'r')
                returned_docs_list, _ = find_docs(fptr_field_file, file_no, field, word)
                print("returned_docs_list: ", returned_docs_list)
                doc_list[word][field] = returned_docs_list
    return doc_list, doc_freq


def search():
    print('Search Engine started!\n')

    filename = config.OUTPUT_FOLDER_PATH + 'title_offset.txt'
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line != '':
                title_offset.append(int(line.strip()))

    filename = config.OUTPUT_FOLDER_PATH + 'vocab_offset.txt'
    with open(filename, 'r') as f:
        for line in f:
            vocab_offset.append(int(line.strip()))

    fptr_vocab = open(config.OUTPUT_FOLDER_PATH + 'vocab.txt', 'r')
    fptr_id_title = open(config.OUTPUT_FOLDER_PATH + 'id_title.txt', 'r')
    with open(config.OUTPUT_FOLDER_PATH + 'numberOfFiles.txt', 'r') as f:
        num_of_files = int(f.read().strip())

    while True:
        query = input('\nType in the query:\n')  # TODO change this to take input from a file instead of cmdline
        start = timeit.default_timer()
        query = query.lower()

        if re.match(r'[tbicrl]:', query):  # is a field query
            query_words = re.findall(r'[tbicrl]:([^:]*)(?!\S)', query)
            query_fields = re.findall(r'([tbicrl]):', query)

            # print("WORDS: ", query_words)
            # print("QFIELDS: ", query_fields)

            tokens = []
            fields = []
            for i in range(len(query_words)):
                for word in query_words[i].split():
                    fields.append(query_fields[i])
                    tokens.append(word)
            """ If input query is: 
            t:the great b:pandas are fluffy i:iceland , then:
            Fields:  ['t', 't', 'b', 'b', 'b', 'i']
            Tokens:  ['the', 'great', 'pandas', 'are', 'fluffy', 'iceland']
            """
            # print("Fields: ", fields)
            # print("Tokens: ", tokens)
            # tokens = cleanup(tokens)
            tokens = remove_stopwords(tokens)
            tokens = stemming(tokens)
            results, doc_freq = search_field_query(tokens, fields, fptr_vocab)
            print("B4 Ranking; Results:", results, "doc_freq:", doc_freq)
            results = rank('field', results, doc_freq, num_of_files)
        else:
            tokens = tokenize(query)
            # tokens = cleanup(tokens)
            tokens = remove_stopwords(tokens)
            tokens = stemming(tokens)
            results, doc_freq = search_simple_query(tokens, fptr_vocab)
            print("B4 Ranking; Results:", results, "doc_freq:", doc_freq)
            results = rank('simple', results, doc_freq, num_of_files)

        print('Results:')
        if len(results) > 0:
            results = sorted(results, key=results.get, reverse=True)
            results = results[:10]
            for key in results:
                title, _ = fetch_doc_titles(0, len(title_offset), title_offset, key, fptr_id_title)
                print(' '.join(title))

        end = timeit.default_timer()
        print('Time taken =', end - start)


if __name__ == '__main__':
    search()

# if len(sys.argv) != 3:  # check arguments
#     print("Usage :: python search.py <location_of_index_files> <query_string>")
#     sys.exit(0)
#
# index_file_name = sys.argv[1] + 'index_file.txt'

# query = sys.argv[2]
# i = 3
# while i < len(sys.argv):  # for query of type: "t:Anarchism is b:humans lived" (separated by space i.e)
#     query += ' ' + sys.argv[i]
#     i += 1
