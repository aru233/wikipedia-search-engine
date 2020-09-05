import timeit

from collections import defaultdict
from parser import Parser
from file_handler import write_into_file, merge_files
import sys

import config


def main():
    # if len(sys.argv) != 4:  # check arguments
    #     print("Usage :: python indexer.py <sample_wiki_dump.xml> </outputFolderLocation> </statFileLocation>")
    #     sys.exit(0)
    # config.INPUT_FILE_NAME = sys.argv[1]
    # config.OUTPUT_FOLDER_PATH = sys.argv[2]
    # config.STATS_FILE_NAME = sys.argv[3]

    Parser(config.INPUT_FILE_NAME)  # Parse XML using SAX Parser

    # TODO is this needed?
    filename = config.OUTPUT_FOLDER_PATH + 'numberOfFiles.txt'
    with open(filename, 'w') as f:
        f.write(config.page_count)

    config.title_offset = write_into_file()
    config.index_map = defaultdict(list)
    config.id_title_map = dict()
    config.file_count += 1

    merge_files()

    # # Writing the index_map and id_title_map to file
    # writeToFile()
    #
    # writeStatsToFile()


if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print("Time taken to index: ", stop - start)
