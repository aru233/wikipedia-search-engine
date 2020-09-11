import config
import re
from collections import defaultdict
from file_handler import write_into_file


def create_index():

    # vocab_list has all the words present in a page(it's per page, from across the six categories)
    vocab_list = []

    vocab_list.extend(config.title.keys())
    vocab_list.extend(config.body.keys())
    vocab_list.extend(config.infobox.keys())
    vocab_list.extend(config.category.keys())
    vocab_list.extend(config.links.keys())
    vocab_list.extend(config.references.keys())
    vocab_list = set(vocab_list)

    for wrd in vocab_list:
        posting_list = 'd'+str(config.page_count)
        if config.title[wrd]:
            posting_list += 't' + str(config.title[wrd])
        if config.infobox[wrd]:
            posting_list += 'i' + str(config.infobox[wrd])
        if config.body[wrd]:
            posting_list += 'b' + str(config.body[wrd])
        if config.category[wrd]:
            posting_list += 'c' + str(config.category[wrd])
        if config.links[wrd]:
            posting_list += 'l' + str(config.links[wrd])
        if config.references[wrd]:
            posting_list += 'r' + str(config.references[wrd])

        config.index_map[wrd].append(posting_list)

    config.page_count += 1

    tempdict = defaultdict(list)
    for wrd in sorted(config.index_map.keys()):
        if (len(wrd) < 2) or (not (re.match('^[a-zA-Z0-9]+$', wrd))) or re.match('^[0]+$', wrd):
            continue
        tempdict[wrd] = config.index_map[wrd]
    config.index_map = tempdict

    if config.page_count % config.PAGE_LIM_PER_FILE == 0:
        config.title_offset = write_into_file()
        config.index_map = defaultdict(list)
        config.id_title_map = dict()
        print("Files till now: ", config.file_count)
        config.file_count += 1


