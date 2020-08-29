import timeit

from parser import Parser
from file_handler import writeToFile, writeStatsToFile
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

    # Writing the index_map and id_title_map to file
    writeToFile()

    writeStatsToFile()


if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print("Time taken to index: ", stop - start)
