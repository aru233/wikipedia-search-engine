from collections import defaultdict
import re
import timeit

import config
from text_preprocessor import tokenize, stemming, remove_stopwords, cleanup
from ranker import rank
from search_helper import find_docs, find_file_no

vocab_offset = []
title_offset = []
num_of_queries = 0
fptr_vocab = None
fptr_id_title = None


def search_field_query(words, fields):
    doc_list = defaultdict(dict)
    doc_list_for_other_fields = defaultdict(dict)
    doc_freq = defaultdict(int)
    doc_freq_for_other_fields = defaultdict(int)
    for i in range(len(words)):
        word = words[i]
        field = fields[i]
        # print("WORD: "+word + " field: "+field)
        docs, _ = find_file_no(0, len(vocab_offset), vocab_offset, word, fptr_vocab)
        '''
        docs will contain 2 things:
        1. the file no. to look into for the word 'word' (say its 2. Then look into t2.txt, b2.txt, i2.txt, r2.txt, 
        l2.txt, c2.txt);.
        2. The count of documents/wiki pages in which the word 'word' occurs
        
        And say we look into b2.txt (later), then it is there that we'll find the exact doc numbers in which the word 
        occurs in the BODY, along with the freq of the word in each of the docs 
        (for t2.txt we'll find words that occur in the TITLE and so on)
        '''
        print('DOCS', docs)
        if len(docs) > 0:
            file_no = docs[0]
            filename = config.OUTPUT_FOLDER_PATH + field + str(file_no) + '.txt'
            fptr_field_file = open(filename, 'r')
            returned_docs_list, df = find_docs(fptr_field_file, file_no, field, word)
            fptr_field_file.close()
            '''
            df: it'll be a single no; it'll be the no. of documents in which the word 'word' appears (DOCUMENT FREQUENCY)

            returned_docs_list: it will have 'df*2' elements or rather 'df' pairs of elements. 
            Each pair will have the doc no. and the count of occ of the word in that particular doc (TERM FREQUENCY)
            Mind that this count and the doc num will be field specific. i.e if field if 't' then only those doc nums
            are given where the 'word' occurs in title, and accordingly. the count is the no of occ of the word in the 
            title of that doc
            '''
            doc_list[word][field] = returned_docs_list
            doc_freq[word] = df

            # SPECIAL SPECIAL HANDLING; Say query is t:Sachin, and we need top 10 results. But Sachin occurs in the title of only 1 doc.
            # Now to be able to return something for the remaining 9 results, look for Sachin in the other fields as well.
            for other_field in ['t', 'b', 'r', 'l', 'c', 'i']:
                if other_field != field:
                    filename = config.OUTPUT_FOLDER_PATH + other_field + str(file_no) + '.txt'
                    fptr_field_file = open(filename, 'r')
                    returned_doc_list_for_other_field, df_other_field = find_docs(fptr_field_file, file_no, other_field,
                                                                                  word)
                    fptr_field_file.close()
                    doc_list_for_other_fields[word][other_field] = returned_doc_list_for_other_field
                    doc_freq_for_other_fields[word] += df_other_field

    return doc_list, doc_list_for_other_fields, doc_freq, doc_freq_for_other_fields


def search_simple_query(words):
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
                # print("WORD: ", word, " FIELD: ", field)
                filename = config.OUTPUT_FOLDER_PATH + field + str(file_no) + '.txt'
                fptr_field_file = open(filename, 'r')
                returned_docs_list, _ = find_docs(fptr_field_file, file_no, field, word)
                fptr_field_file.close()
                # print("returned_docs_list: ", returned_docs_list)
                doc_list[word][field] = returned_docs_list
    return doc_list, doc_freq


def search():
    global num_of_queries
    filename = 'queries.txt'  # TODO: need to take this file name from the sh file?
    with open(filename, 'r') as f:
        for line in f:
            if line == '':
                continue
            num_of_queries += 1
            k, query = line.split(',')
            print('-------------------------------------------------------------------------------------------')
            start = timeit.default_timer()
            k = int(k)
            query = query.strip().lower()
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
                results, results_for_other_fields, doc_freq, doc_freq_for_other_fields = search_field_query(tokens, fields)
                '''
                'results' will have entry only for relevant fields (corres val can be empty/non-empty
                depending on whether the word appears in the particular field or not)
                'results_for_other_fields' will have entry for the other fields
                '''
                print("B4 RANKING; Results:", results)
                print("Results for other fields:", results_for_other_fields)
                print("doc_freq:", doc_freq, " doc freq for other fields:", doc_freq_for_other_fields)

                top_k_results = rank(k, results, doc_freq, num_of_files, title_offset, fptr_id_title)
                if len(top_k_results) < k:
                    other_results = rank(k-len(top_k_results), results_for_other_fields, doc_freq_for_other_fields, num_of_files, title_offset, fptr_id_title)
                    for res in other_results:
                        top_k_results.append(res)

                top_k_results = list(set(top_k_results))
            else:
                tokens = tokenize(query)
                # tokens = cleanup(tokens)
                tokens = remove_stopwords(tokens)
                tokens = stemming(tokens)
                results, doc_freq = search_simple_query(tokens)
                '''
                'results' for a simple query will have entry for all 6 fields, the corres val might be empty/non-empty 
                depending on the fields in which the word occurs
                '''
                print("B4 Ranking; Results:", results, "doc_freq:", doc_freq)
                top_k_results = rank(k, results, doc_freq, num_of_files, title_offset, fptr_id_title)

            print('\nRanked Results:\n', top_k_results)

            end = timeit.default_timer()
            print(end - start)

            write_query_output_to_file(top_k_results, start, end)


def write_query_output_to_file(top_k_results, start, end):
    total_time = end - start
    if num_of_queries > 0:
        avg_time = total_time / num_of_queries
    else:
        avg_time = 0
    with open('queries_op.txt', 'a') as fp:
        for res in top_k_results:
            fp.write(res + '\n')
        fp.write(str(total_time) + ',' + str(avg_time) + '\n\n')


if __name__ == '__main__':
    print('Search Engine started!\n')

    with open(config.OUTPUT_FOLDER_PATH + 'title_offset.txt', 'r') as fl:
        for lne in fl:
            lne = lne.strip()
            if lne != '':
                title_offset.append(int(lne.strip()))

    with open(config.OUTPUT_FOLDER_PATH + 'vocab_offset.txt', 'r') as fl:
        for lne in fl:
            vocab_offset.append(int(lne.strip()))

    fptr_vocab = open(config.OUTPUT_FOLDER_PATH + 'vocab.txt', 'r')
    fptr_id_title = open(config.OUTPUT_FOLDER_PATH + 'id_title.txt', 'r')
    with open(config.OUTPUT_FOLDER_PATH + 'numberOfFiles.txt', 'r') as fl:
        num_of_files = int(fl.read().strip())

    search()
    fptr_vocab.close()
    fptr_id_title.close()
