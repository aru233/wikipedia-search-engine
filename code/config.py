from collections import defaultdict

PAGE_LIM_PER_FILE = 20000

index_map = defaultdict(list)
# index_map["1"].append("uff")

id_title_map = dict()
# vocab_list = []

page_count = 1
file_count = 1
offset = 0

'''infobox will be a dict (ultimately) that stores all the words that appear in the infobox of a page and their freq 
(initially it'll have the resp words in form of a list). Similarly for the other 5 '''
title, body, infobox, category, links, references = [], [], [], [], [], []



