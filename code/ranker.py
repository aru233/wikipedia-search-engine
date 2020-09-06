from collections import defaultdict
import math
from search_helper import fetch_doc_titles


def rank(k, results, doc_freq, num_files, title_offset, fptr_id_title):
    # print("IN rank!")
    docs = defaultdict(float)
    inverse_doc_freq = defaultdict(float)

    # Calculating and storing IDF for each term
    for wrd in doc_freq:
        if float(doc_freq[wrd]) > 0:
            inverse_doc_freq[wrd] = math.log(float(num_files) / float(doc_freq[wrd]))

    for word in results:
        posting_list_field_wise = results[word]
        # In above, we'll get a dict of list (list being the doc_num and term_freq pairs thing)
        for field in posting_list_field_wise:
            # print("FIELD: ", field)
            posting_list = posting_list_field_wise[field]
            if len(posting_list) > 0:  # TODO: have chng from field->current in len()
                factor = 0.0
                if field == 't':
                    factor = 0.25
                elif field == 'i':
                    factor = 0.25
                elif field == 'b':
                    factor = 0.20
                elif field == 'c':
                    factor = 0.10
                elif field == 'r':
                    factor = 0.05
                elif field == 'l':
                    factor = 0.05
                for i in range(0, len(posting_list), 2):
                    doc_num = posting_list[i]
                    tf = float(posting_list[i + 1])
                    if tf > 0.0:
                        docs[doc_num] += float(factor * (1.0 + math.log(tf)) * inverse_doc_freq[word])
                    '''
                    posting_list[i]: gives a doc num, and 
                    posting_list[i+1]: will the the term-freq (count of occ of word in that doc)
                    docs[posting_list[i]]: for a query word 'word' and a field 'f', docs[doc_num] will store the tf-idf 
                    weight for that doc and for the relevant terms that occur in that doc
                    '''

    return top_k_docs(k, docs, title_offset, fptr_id_title)


def top_k_docs(k, docs, title_offset, fptr_id_title):
    top_k_ranked_results = []
    if len(docs) > 0:
        doc_ids = sorted(docs, key=docs.get, reverse=True)  # sorts the docs on basis of the value i.e the tf-idf weights' value
        doc_ids = doc_ids[:k]
        for doc_id in doc_ids:
            title, _ = fetch_doc_titles(0, len(title_offset), title_offset, doc_id, fptr_id_title)
            # print("doc_id: ", doc_id, " TITLE: ", title)
            top_k_ranked_results.append(str(str(doc_id) + ', ' + title[0]))
    return top_k_ranked_results
