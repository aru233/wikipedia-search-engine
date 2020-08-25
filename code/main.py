import sys
import timeit

from parser import Parser
from fileHandler import writeToFile
import config


def main():
    # if len(sys.argv) != 3:  # check arguments
    #     print("Usage :: python main.py <sample_file.xml> </outputFolderLocation>")
    #     sys.exit(0)
    # filename = sys.argv[1]

    filename = "enwiki.xml-p1p30303"
    # filename = "tmp_with_infbx.xml"
    parser = Parser(filename)  # Parse XML using SAX Parser

    # Writing the index_map and id_title_map to file
    writeToFile()


if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print("Time taken to index: ", stop - start)


