import config
from textPreprocessor import cleanup

def writeToFile():
    # 1. Writing the index_map to file
    data = []
    '''index_map is a dict of lists. <word> -> [ d1:b1i1, d2:b2c1]...'''
    print("PRINTING IN FILE HANDLER")
    i=1
    for wrd in sorted(config.index_map.keys()):
        postings = ' '.join(config.index_map[wrd])
        # wrd1 = cleanup(wrd)
        data.append(wrd + ' ' + postings)
        if i<15:
            print("word: ", wrd, " postings: ", postings, " total: ", wrd + ' ' + postings)
            # print("DATA: ", data)
            i+=1

    filename = "data/index_file.txt"
    with open(filename, 'w') as f:
        f.write('\n'.join(data))

    # 2. Writing the id_title_map to file
    data = []
    for idn in config.id_title_map:  # sorted(config.id_title_map)
        data.append(str(idn) + ' ' + config.id_title_map[idn])

    filename = "data/id_title_file.txt"
    with open(filename, 'w') as f:
        f.write('\n'.join(data))