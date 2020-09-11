from collections import defaultdict

# filename = "enwiki.xml-p1p30303"
# filename = "tmp_with_infbx.xml"
# filename = "tmp1.xml-p1p30303"
# filename = "tmp17068.xml"
INPUT_FILE_NAME = "tmp17068.xml"  # "dump_data/enwiki-20200801-pages-articles-multistream13.xml-p5040437p6197594"
OUTPUT_FOLDER_PATH = 'data/'
STATS_FILE_NAME = 'data/stats.txt'
STOPWORD_FILE_PATH = 'code/stopwords.txt'

# INPUT_FILE_NAME = '/home/wiki/multistream1.xml-p1p30303'  #'tmp1.xml-p1p30303'
# OUTPUT_FOLDER_PATH = '2019201015/inverted_index/'  # 'data/'
# STATS_FILE_NAME = '2019201015/invertedindex_stat.txt'  # 'data/invertedindex_stat.txt'
# STOPWORD_FILE_PATH = '2019201015/stopwords.txt'


PAGE_LIM_PER_FILE = 20000
WORD_LIM = 150000

token_count_inverted_index = 0
token_count_dump = 0

index_map = defaultdict(list)

id_title_map = dict()

page_count = 0
file_count = 0
title_offset = 0  # this tells where we left off in the id_title file

'''infobox will be a dict (ultimately) that stores all the words that appear in the infobox of a page and their freq 
(initially it'll have the resp words in form of a list). Similarly for the other 5 '''
title, body, infobox, category, links, references = [], [], [], [], [], []



