from collections import defaultdict
import xml.sax
import re

from text_preprocessor import casefold, remove_stopwords, stemming, cleanup, tokenize
from indexer import create_index
import config


def process_title(data):
    config.title = []
    data = casefold(data)
    config.token_count_dump += len(data.split())
    data = cleanup(data)
    data = tokenize(data)
    data = remove_stopwords(data)
    data = stemming(data)

    tempdict = defaultdict(int)
    for wrd in data:
        if len(wrd) >= 2:
            tempdict[wrd] += 1

    config.title = tempdict


def process_text(data):
    config.body, config.infobox, config.category, config.links, config.references = [], [], [], [], []
    data = casefold(data)
    config.token_count_dump += len(data.split())
    data_lines = data.split('\n')
    num_of_lines = len(data_lines)
    # print("num_of_lines in text: ", num_of_lines)
    i = -1
    while 1:
        i += 1
        if i >= num_of_lines:
            break
        if "{{infobox" in data_lines[i]:
            i = extract_infobox_data(data_lines, i, num_of_lines)
        elif "[[category:" in data_lines[i]:
            extract_category_data(data_lines, i)
        elif "== external links ==" in data_lines[i] or "==external links==" in data_lines[i] or \
                "== external links==" in data_lines[i] or "==external links ==" in data_lines[i]:
            i = extract_ext_links(data_lines, i, num_of_lines)
        elif "== references ==" in data_lines[i] or "==references==" in data_lines[i] or "== references==" in \
                data_lines[i] or "==references ==" in data_lines[i]:
            i = extract_references(data_lines, i, num_of_lines)
        else:
            config.body.append(data_lines[i])

    config.body = process_util(config.body)
    config.infobox = process_util(config.infobox)
    config.category = process_util(config.category)
    config.links = process_util(config.links)
    config.references = process_util(config.references)


def process_util(dta):
    data = ' '.join(dta)
    data = cleanup(data)
    data = tokenize(data)
    data = remove_stopwords(data)
    data = stemming(data)

    tempdict = defaultdict(int)
    for x in data:
        tempdict[x] += 1
    return tempdict  # returns a dictionary


def extract_references(data_lines, i, num_of_lines):
    i += 1
    curly_total_opened = 0
    while 1:
        if i >= num_of_lines:
            break
        if "{{" in data_lines[i]:
            curly_new_opened = data_lines[i].count("{{")
            curly_total_opened += curly_new_opened
        if "}}" in data_lines[i]:
            curly_new_closed = data_lines[i].count("}}")
            curly_total_opened -= curly_new_closed
        if curly_total_opened <= 0:
            break
        if "{{reflist" not in data_lines[i] and 'title' in data_lines[i]:
            config.references.append(re.sub(r'.*title[\ ]*=[\ ]*([^\|]*).*', r'\1', data_lines[i]))
        i += 1

    return i


def extract_ext_links(data_lines, i, num_of_lines):
    i += 1
    while i < num_of_lines:
        if "* [" in data_lines[i] or "*[" in data_lines[i]:
            config.links.extend(data_lines[i].split(' '))
            i += 1
        else:
            break
    return i


def extract_category_data(data_lines, i):
    split_line = data_lines[i].split("[[category")
    if len(split_line) <= 1:
        return
    tmp = split_line[1].split("]]")[0] + ' '
    config.category.append(tmp)


def extract_infobox_data(data_lines, i, num_of_lines):
    curly_total_opened = 0
    while 1:
        if "{{" in data_lines[i]:
            curly_new_opened = data_lines[i].count("{{")
            curly_total_opened += curly_new_opened
        if "}}" in data_lines[i]:
            curly_new_closed = data_lines[i].count("}}")
            curly_total_opened -= curly_new_closed
        if curly_total_opened <= 0:
            break
        split_line = data_lines[i].split("{{infobox")
        if "{{infobox" in data_lines[i] and len(split_line) >= 2 and len(split_line[1]) > 0:
            config.infobox.append(split_line[1])
        else:
            config.infobox.append(data_lines[i])
        i += 1
        if i >= num_of_lines:
            break
    return i


class XmlContentHandler(xml.sax.handler.ContentHandler):

    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self.current_tag = ""
        self.bufferTitle = ""
        self.bufferText = ""
        self.bufferId = ""
        self.idFlag = 0

    def startElement(self, tag, attrs):
        self.current_tag = tag
        if tag == "id" and self.idFlag == 0:
            self.bufferId = ""
            self.idFlag = 1
        elif tag == "title":
            self.bufferTitle = ""
        elif tag == "text":
            self.bufferText = ""
        # TODO handle when tag=="page" ?

    def endElement(self, tag):
        if tag == "id" and self.idFlag == 1:
            self.idFlag = 0
        elif tag == "title":
            config.id_title_map[config.page_count] = self.bufferTitle
            process_title(self.bufferTitle)
        elif tag == "text":
            process_text(self.bufferText)
            create_index()

    def characters(self, content):
        if self.current_tag == "id" and self.idFlag == 1:
            self.bufferId += content
        elif self.current_tag == "title":
            self.bufferTitle += content
        elif self.current_tag == "text":
            self.bufferText += content


class Parser:
    def __init__(self, filename):
        self.parser = xml.sax.make_parser()
        self.parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        self.handler = XmlContentHandler()
        self.parser.setContentHandler(self.handler)
        self.parser.parse(filename)
