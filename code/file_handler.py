import config
import re
import heapq
from collections import defaultdict
from tqdm import tqdm
import threading
glob_wrd_cnt = 0


def write_into_file():
    '''
    This fn writes the temporary intermediate inverted index to files, and also the id-title mapping to the id_title
    file (there's only one such file)
    '''
    prev_title_offset = config.title_offset
    data = []
    for key in sorted(config.index_map.keys()):
        string = key + ' '
        postings = config.index_map[key]
        string += ' '.join(postings)
        data.append(string)

    filename = config.OUTPUT_FOLDER_PATH + 'index' + str(config.file_count) + '.txt'
    with open(filename, 'w') as f:
        f.write('\n'.join(data))

    data = []
    data_offset = []
    for key in sorted(config.id_title_map):
        string = str(key) + ' ' + config.id_title_map[key].strip()
        data.append(string)
        data_offset.append(str(prev_title_offset))
        prev_title_offset += len(string) + 1

    filename = config.OUTPUT_FOLDER_PATH + 'id_title.txt'
    with open(filename, 'a') as f:
        f.write('\n'.join(data))
        f.write('\n')

    filename = config.OUTPUT_FOLDER_PATH + 'title_offset.txt'
    with open(filename, 'a') as f:
        f.write('\n'.join(data_offset))
        f.write('\n')

    return prev_title_offset


def merge_files():
    # TODO rm ?
    global glob_wrd_cnt

    heap = []
    file_ptrs = {}
    file_flag = [0] * config.file_count
    line_in_file = {}
    words = {}
    data = defaultdict(list)

    count_final = 0  # maintains count of the final inverted index files
    offset_size = 0
    word_count = 0

    for i in range(config.file_count):
        filename = config.OUTPUT_FOLDER_PATH + 'index' + str(i) + '.txt'
        file_ptrs[i] = open(filename, 'r')
        file_flag[i] = 1
        line_in_file[i] = file_ptrs[i].readline().strip()
        words[i] = line_in_file[i].split()
        if len(words[i]) == 0:
            file_flag[i] = 0
            continue
        if words[i][0] not in heap:
            heapq.heappush(heap, words[i][0])

    while any(file_flag) == 1:
        word_count += 1
        tmp = heapq.heappop(heap)
        if word_count % config.WORD_LIM == 0:
            # TODO rm ?
            glob_wrd_cnt = word_count
            count_old = count_final
            count_final, offset_size = write_into_final_index_file(data, count_final, offset_size)
            if count_old != count_final:
                data = defaultdict(list)
        for i in range(config.file_count):
            if file_flag[i] == 1 and tmp == words[i][0]:
                data[tmp].extend(words[i][1:])
                line_in_file[i] = file_ptrs[i].readline().strip()
                if line_in_file[i] != '':
                    words[i] = line_in_file[i].split()
                    if words[i][0] not in heap:
                        heapq.heappush(heap, words[i][0])
                else:  # all words of i th temp index file have been processed;
                    file_ptrs[i].close()
                    file_flag[i] = 0

    _, _ = write_into_final_index_file(data, count_final, offset_size)

    print("COUNT_FINAL="+str(count_final))


def write_into_final_index_file(data, count_final, offset_size):
    # data has the posting lists for WORD_LIM words

    # dod: dict of dict
    title_dod = defaultdict(dict)
    body_dod = defaultdict(dict)
    infobox_dod = defaultdict(dict)
    category_dod = defaultdict(dict)
    link_dod = defaultdict(dict)
    reference_dod = defaultdict(dict)

    # ALL the words ever in the dump + the actual file no.(i.e after merging) it'll be in (int text, body, category..)
    distinct_words = []

    # This is the offset for the vocab.txt file we'll write with the distinct_words
    offset = []

    for key in tqdm(sorted(data.keys())):
        list_of_postings = data[key]
        # temp = []

        for i in range(len(list_of_postings)):
            posting = list_of_postings[i]
            doc_id = re.sub(r'.*d([0-9]*).*', r'\1', posting)

            temp = re.sub(r'.*t([0-9]*).*', r'\1', posting)
            if temp != posting: # the 'key' is present in title of some doc
                title_dod[key][doc_id] = float(temp)

            temp = re.sub(r'.*b([0-9]*).*', r'\1', posting)
            if temp != posting:
                body_dod[key][doc_id] = float(temp)

            temp = re.sub(r'.*i([0-9]*).*', r'\1', posting)
            if temp != posting:
                infobox_dod[key][doc_id] = float(temp)

            temp = re.sub(r'.*c([0-9]*).*', r'\1', posting)
            if temp != posting:
                category_dod[key][doc_id] = float(temp)

            temp = re.sub(r'.*l([0-9]*).*', r'\1', posting)
            if temp != posting:
                link_dod[key][doc_id] = float(temp)

            temp = re.sub(r'.*r([0-9]*).*', r'\1', posting)
            if temp != posting:
                reference_dod[key][doc_id] = float(temp)

        string = key + ' ' + str(count_final) + ' ' + str(len(list_of_postings))
        distinct_words.append(string)
        offset.append(str(offset_size))
        offset_size += len(string) + 1

    write_to_field_based_files(data, title_dod, body_dod, infobox_dod, category_dod, link_dod, reference_dod, count_final)

    # TODO needed?
    filename = config.OUTPUT_FOLDER_PATH + 'vocab.txt'
    with open(filename, 'a') as f:
        f.write('\n'.join(distinct_words))
        f.write('\n')

    filename = config.OUTPUT_FOLDER_PATH + 'vocab_offset.txt'
    with open(filename, 'a') as f:
        f.write('\n'.join(offset))
        f.write('\n')

    return count_final + 1, offset_size


def write_to_field_based_files(data, title_dod, body_dod, infobox_dod, category_dod, link_dod, reference_dod, count_final):
    title_data = []
    title_offset = []
    prev_offset_title = 0

    body_data = []
    body_offset = []
    prev_offset_body = 0

    infobox_data = []
    infobox_offset = []
    prev_offset_infobox = 0

    link_data = []
    link_offset = []
    prev_offset_link = 0

    category_data = []
    category_offset = []
    prev_offset_category = 0

    reference_data = []
    reference_offset = []
    prev_offset_reference = 0

    for key in tqdm(sorted(data.keys())):
        if key in title_dod:
            string = key + ' '
            tdocs = title_dod[key]
            # tdocs is a dict; keys are the docIDs and values are the count of occ of word 'key' in title

            sorted_doc_ids = sorted(tdocs, key=tdocs.get, reverse=True)
            # returns the keys sorted in descending order of the values

            for doc in sorted_doc_ids:
                string += doc + ' ' + str(title_dod[key][doc]) + ' '
            title_offset.append(str(prev_offset_title) + ' ' + str(len(sorted_doc_ids)))
            prev_offset_title += len(string) + 1
            title_data.append(string)

        if key in body_dod:
            string = key + ' '
            bdocs = body_dod[key]
            sorted_doc_ids = sorted(bdocs, key=bdocs.get, reverse=True)
            for doc in sorted_doc_ids:
                string += doc + ' ' + str(body_dod[key][doc]) + ' '
            body_offset.append(str(prev_offset_body) + ' ' + str(len(sorted_doc_ids)))
            prev_offset_body += len(string) + 1
            body_data.append(string)

        if key in infobox_dod:
            string = key + ' '
            idocs = infobox_dod[key]
            sorted_doc_ids = sorted(idocs, key=idocs.get, reverse=True)
            for doc in sorted_doc_ids:
                string += doc + ' ' + str(infobox_dod[key][doc]) + ' '
            infobox_offset.append(str(prev_offset_infobox) + ' ' + str(len(sorted_doc_ids)))
            prev_offset_infobox += len(string) + 1
            infobox_data.append(string)

        if key in category_dod:
            string = key + ' '
            cdocs = category_dod[key]
            sorted_doc_ids = sorted(cdocs, key=cdocs.get, reverse=True)
            for doc in sorted_doc_ids:
                string += doc + ' ' + str(category_dod[key][doc]) + ' '
            category_offset.append(str(prev_offset_category) + ' ' + str(len(sorted_doc_ids)))
            prev_offset_category += len(string) + 1
            category_data.append(string)

        if key in link_dod:
            string = key + ' '
            ldocs = link_dod[key]
            sorted_doc_ids = sorted(ldocs, key=ldocs.get, reverse=True)
            for doc in sorted_doc_ids:
                string += doc + ' ' + str(link_dod[key][doc]) + ' '
            link_offset.append(str(prev_offset_link) + ' ' + str(len(sorted_doc_ids)))
            prev_offset_link += len(string) + 1
            link_data.append(string)

        if key in reference_dod:
            string = key + ' '
            rdocs = reference_dod[key]
            sorted_doc_ids = sorted(rdocs, key=rdocs.get, reverse=True)
            for doc in sorted_doc_ids:
                string += doc + ' ' + str(reference_dod[key][doc]) + ' '
            reference_offset.append(str(prev_offset_reference) + ' ' + str(len(sorted_doc_ids)))
            prev_offset_reference += len(string) + 1
            reference_data.append(string)

    thread = [WriteThread('t', title_data, title_offset, count_final),
              WriteThread('b', body_data, body_offset, count_final),
              WriteThread('i', infobox_data, infobox_offset, count_final),
              WriteThread('c', category_data, category_offset, count_final),
              WriteThread('l', link_data, link_offset, count_final),
              WriteThread('r', reference_data, reference_offset, count_final)]

    for i in range(6):
        thread[i].start()

    for i in range(6):
        thread[i].join()


class WriteThread(threading.Thread):
    def __init__(self, field, data, offset, count):
        threading.Thread.__init__(self)
        self.field = field
        self.data = data
        self.count = count
        self.offset = offset

    def run(self):
        filename = config.OUTPUT_FOLDER_PATH + self.field + str(self.count) + '.txt'
        with open(filename, 'w') as f:
            f.write('\n'.join(self.data))

        filename = config.OUTPUT_FOLDER_PATH + 'offset_' + self.field + str(self.count) + '.txt'
        with open(filename, 'w') as f:
            f.write('\n'.join(self.offset))

