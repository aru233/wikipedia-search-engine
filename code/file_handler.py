import config
import re
from text_preprocessor import cleanup


def writeToFile():
    # 1. Writing the index_map to file
    data = []
    '''index_map is a dict of lists. <word> -> [ d1:b1i1, d2:b2c1]...'''
    for wrd in sorted(config.index_map.keys()):
        if (len(wrd) < 2) or (not (re.match('^[a-zA-Z0-9]+$', wrd))) or re.match('^[0]+$', wrd):
            # or re.match('^[0-9][a-zA-Z0-9]+$', wrd)
            continue
        postings = ' '.join(config.index_map[wrd])
        data.append(wrd + ' ' + postings)
        config.token_count_index_map += 1

    # TODO: Remember to handle the file name accordingly
    filename = config.OUTPUT_FOLDER_PATH + "index_file.txt"
    with open(filename, 'w') as f:
        f.write('\n'.join(data))

    # # 2. Writing the id_title_map to file
    # data = []
    # for idn in config.id_title_map:  # sorted(config.id_title_map)
    #     data.append(str(idn) + ' ' + config.id_title_map[idn])
    #
    # filename = "data/id_title_file.txt"
    # with open(filename, 'w') as f:
    #     f.write('\n'.join(data))


def writeStatsToFile():
    with open(config.STATS_FILE_NAME, 'w') as f:
        f.write(str(config.token_count_dump) + '\n')
        f.write(str(config.token_count_index_map))
