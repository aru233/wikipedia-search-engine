import config


def writeToFile():
    # 1. Writing the index_map to file
    data = []
    '''index_map is a dict of lists. 
    <word> -> [ d1:b1i1, d2:b2c1]...
    '''
    for wrd in sorted(config.index_map.keys()):
        data.append(wrd + ' ' + ' '.join(config.index_map[wrd]))

    filename = "../data/index_file.txt"
    with open(filename, 'w') as f:
        f.write('\n'.join(data))

    # 2. Writing the id_title_map to file
    data = []
    for id in sorted(config.id_title_map):
        data.append(str(id) + ' ' + config.index_map[id].strip())

    filename = "../data/id_title_file.txt"
    with open(filename, 'w') as f:
        f.write('\n'.join(data))
