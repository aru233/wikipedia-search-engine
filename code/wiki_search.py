import config
import re
from text_preprocessor import casefold, remove_stopwords, stemming, cleanup, tokenize, word_stemming
import sys
import timeit


def search_plain_query(query, index_file_name):
    # print("ISSA PLAIN QUERY!")
    # query = cleanup(query)
    query = tokenize(query)
    query = remove_stopwords(query)
    # query = stemming(query)
    with open(index_file_name, 'r') as f:
        for line in f:
            key = line.split(' ', maxsplit=1)[0]
            posting_list = line.split(' ', maxsplit=1)[1].strip()  # strip() to remove newline
            for wrd in query:
                # wrd = re.sub(r'[.,!;_()"/\'=]', '', wrd, flags=re.MULTILINE)
                stem_wrd = word_stemming(wrd)
                if stem_wrd == key:
                    print(wrd, posting_list)


def search_field_query(query, index_file_name):
    # Query of type: i:affix b:affixion"
    # print("ISSA FIELD QUERY!")
    st, i = 0, 1
    positions = [i.start() for i in re.finditer(":", query)]
    # print(positions)
    query_list = []
    # Find words by taking 2 consecutive ':' positions as boundary for that word
    while i < (len(positions)):
        query_list.append(query[st:positions[i] - 1].strip())
        st = positions[i] - 1
        i += 1
    query_list.append(query[st:len(query)].strip())  # for the last word
    # print(query_list)

    with open(index_file_name, 'r') as f:
        for line in f:
            # print("Line in file: ", line)
            key = line.split(' ', maxsplit=1)[0]
            posting_list = line.split(' ', maxsplit=1)[1].strip()  # strip() to remove newline
            for qu in query_list:
                field, wrd = qu.split(':')
                wrd = wrd.split()
                # print(field, wrd)
                # wrd = re.sub(r'[.,!;_()"/\'=]', '', wrd, flags=re.MULTILINE)
                for w in wrd:
                    w = w.strip()
                    if w is None or w == '' or w == ' ':
                        continue
                    stem_wrd = word_stemming(w)
                    if stem_wrd == key and field in posting_list:
                        print(w, posting_list)


def search(query, index_file_name):
    query = casefold(query)
    if re.search(r'[t|i|b|c|l|r]:', query[:2]):
        search_field_query(query, index_file_name)
    else:
        search_plain_query(query, index_file_name)


def main():
    # if len(sys.argv) != 3:  # check arguments
    #     print("Usage :: python search.py <location_of_index_files> <query_string>")
    #     sys.exit(0)
    # # TODO: Remember to change this filename accordingly
    # index_file_name = sys.argv[1] + 'index_file.txt'

    # query = sys.argv[2]
    # i = 3
    # while i < len(sys.argv):  # for query of type: "t:Anarchism is b:humans lived" (separated by space i.e)
    #     query += ' ' + sys.argv[i]
    #     i += 1

    index_file_name = config.OUTPUT_FOLDER_PATH + 'index_file.txt'
    query = "t:Anarchism is b:humans lived"

    search(query, index_file_name)


if __name__ == '__main__':
    # txt='t:world'
    # print(txt.split(':')[1])
    # print(txt.split(':')[1].split())
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print("Time taken to search: ", stop - start)
