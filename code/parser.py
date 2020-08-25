import xml.sax
from collections import defaultdict
from .textPreprocessor import casefold, remove_stopwords, stemming, cleanup, tokenize
from .indexer import create_index

idTitleMapping = dict()
countId = 1
title, body, infobox, category, links, references = [], [], [], [], [], []


# infobox will be a dict (ultimately) that stores all the words and their freq that appear in the infobox of a page
# (initially it contained the resp words in form of a list, and then the list's data was transformed to a dict)
# Similarly for the other 5


def process_title(data):
    global title
    title = []
    data = casefold(data)
    # TODO cleanup needed??
    tokenized_data = tokenize(data)
    stopword_removed_data = remove_stopwords(tokenized_data)
    stemmed_data = stemming(stopword_removed_data)

    tempdict = defaultdict(int)
    for wrd in stemmed_data:
        tempdict[wrd] += 1

    title = tempdict


def process_text(data):
    global body, infobox, category, links, references
    body, infobox, category, links, references = [], [], [], [], []
    data = casefold(data)
    data_lines = data.split('\n')
    num_of_lines = len(data_lines)
    i = -1
    while 1:
        i += 1
        if i == num_of_lines:
            break
        if "{{infobox" in data_lines[i]:
            i = extract_infobox_data(data_lines, i, num_of_lines)
        elif "[[category:" in data_lines[i]:
            extract_category_data(data_lines, i)
        elif "== external links ==" in data_lines[i] or "==external links==" in data_lines[i] or \
                "== external links==" in data_lines[i] or "==external links ==" in data_lines[i]:
            i += 1
            i = extract_ext_links(data_lines, i, num_of_lines)
        elif "== references ==" in data_lines[i] or "==references==" in data_lines[i] or "== references==" in \
                data_lines[i] or "==references ==" in data_lines[i]:
            i = extract_references(data_lines, i, num_of_lines)
        else:
            body.append(data_lines[i])

    body = process_util(body)
    infobox = process_util(infobox)
    category = process_util(category)
    links = process_util(links)
    references = process_util(references)


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
    global references
    i += 1
    curly_total_opened = 0
    while 1:
        if i == num_of_lines:
            break
        if "{{" in data_lines[i]:
            curly_new_opened = data_lines[i].count("{{")
            curly_total_opened += curly_new_opened
        if "}}" in data_lines[i]:
            curly_new_closed = data_lines[i].count("}}")
            curly_total_opened -= curly_new_closed
        if curly_total_opened <= 0:
            break
        if "{{reflist" not in data_lines[i] and "{{cite" not in data_lines[i] and "{{vcite" not in data_lines[i]:
            references.append(data_lines[i])
        i += 1

    return i


def extract_ext_links(data_lines, i, num_of_lines):
    global links
    i += 1
    while i < num_of_lines:
        if "* [" in data_lines[i]:
            split_line = data_lines[i].split("* [")  # CHNG
            links.extend(split_line.split(' '))
        elif "*[" in data_lines[i]:
            split_line = data_lines[i].split("*[")  # CHNG
            links.extend(split_line.split(' '))
        else:
            break
        i += 1
    return i


def extract_category_data(data_lines, i):
    global category
    split_line = data_lines[i].split("[[category")
    if len(split_line) <= 1:
        return
    tmp = split_line[1].split("]]")[0] + ' '
    category.append(tmp)


def extract_infobox_data(data_lines, i, num_of_lines):
    global infobox
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
            infobox.append(split_line[1])
        else:
            infobox.append(data_lines[i])
        i += 1
        if i == num_of_lines:
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

    def endElement(self, tag):
        global idTitleMapping
        if tag == "id" and self.idFlag == 1:
            self.idFlag = 0
        elif tag == "title":
            # TODO need to pre-process/clean bufferTitle?
            idTitleMapping[countId] = self.bufferTitle
            # TODO need to encode? (data.encode('utf-8'))
            process_title(self.bufferTitle)
        elif tag == "text":
            process_text(self.bufferText)
            create_index(title, body, infobox, category, links, references)
            # TODO - continue the stuff to do here

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

    # # noinspection PyMethodMayBeStatic
    # def get_data(self):
    #     global title, body, infobox, category, links, references
    #     return title, body, infobox, category, links, references
