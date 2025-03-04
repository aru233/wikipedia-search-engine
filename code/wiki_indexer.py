import timeit

from collections import defaultdict
from parser import Parser
from file_handler import write_into_file, merge_files
import sys
from datetime import datetime

import config


def main():
    # if len(sys.argv) != 4:  # check arguments
    #     print("Usage :: python indexer.py <sample_wiki_dump.xml> </outputFolderLocation> </statFileLocation>")
    #     sys.exit(0)
    # config.INPUT_FILE_NAME = sys.argv[1]
    # config.OUTPUT_FOLDER_PATH = sys.argv[2]
    # config.STATS_FILE_NAME = sys.argv[3]

    # Parser(config.INPUT_FILE_NAME)  # Parse XML using SAX Parser
    Parser()

    filename = config.OUTPUT_FOLDER_PATH + 'numberOfFiles.txt'
    with open(filename, 'w') as f:
        f.write(str(config.page_count))

    config.title_offset = write_into_file()
    config.index_map = defaultdict(list)
    config.id_title_map = dict()
    config.file_count += 1

    print("FILE COUNT="+str(config.file_count))
    print("PAGE COUNT=" + str(config.page_count))

    # print("Going to merge files")
    # count_final = merge_files()
    #
    # write_to_stats_file(count_final)


def write_to_stats_file(count_final):
    filename = config.STATS_FILE_NAME
    with open(filename, 'w') as f:
        # f.write()  # index size in GB
        f.write(str(int(count_final+1) * 6) + '\n')
        f.write(str(config.token_count_inverted_index) + '\n')


if __name__ == '__main__':
    print(datetime.now().time())
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print("Time taken to index: ", (stop - start)/60, " min")
