import config

from collections import defaultdict

def create_index():
    # global index_map

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
        posting_list = 'd'+str(config.page_count)+":"
        if config.title[wrd]:
            posting_list += 't' + str(config.title[wrd])
        if config.body[wrd]:
            posting_list += 'b' + str(config.body[wrd])
        if config.infobox[wrd]:
            posting_list += 'i' + str(config.infobox[wrd])
        if config.category[wrd]:
            posting_list += 'c' + str(config.category[wrd])
        if config.references[wrd]:
            posting_list += 'r' + str(config.references[wrd])

        config.index_map[wrd].append(posting_list)

    config.page_count += 1
    # if config.page_count % config.PAGE_LIM_PER_FILE == 0:
    #     # config.offset = writeIntoFile(sys.argv[2], index, dict_Id, countFile, config.offset)
    #     config.index_map = defaultdict(list)
    #     config.id_title_map = dict()
    #     config.file_count += 1


def fn():
    print(config.index_map)
    config.index_map['2'].append("rew")
    print(config.index_map)


if __name__ == '__main__':
    fn()
