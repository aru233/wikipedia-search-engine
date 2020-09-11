# Wikipedia-Search-Engine

This repository consists of a search engine over the 40GB Wikipedia dump. The code consists of wiki_indexer.py and wiki_search.py. 
Both multi-word simple and multi-field queries have been implemented. The search returns a ranked list of top k articles in real time.

### Indexing:
SAX Parser is used to parse the XML corpus.

After parsing, following pre-processing is done:

    Casefolding: Converting Upper Case to Lower Case.
    Tokenisation: It is done using regex.
    Stop Word Removal: Stop words are removed by referring to the stop word list returned by nltk.
    Stemming: A python library PyStemmer is used for this purpose.
    
 * The index, consisting of stemmed words and posting lists is built for the corpus after performing the above operations,
 along with the title and the unique mapping that has been defined for each document. 
 * The document id of the wikipedia page is thus ignored. This helps in reducing the size and easily tracking the repective document.  
 * Since the size of the corpus will not fit into the main memory, several intermediary index files are generated. 
 * Next, these index files are merged using Multi-way External sorting and field based index files are created along with their respective offsets.
 * Maintaining offsets of the respective field based idex files allows to use binary search while searching for a word.
 * The field based files are create using multi-threading. This helps in doing multiple I/O simultaneously.
 
### Searching:

    The query given is parsed, processed and given to the respective query handler(simple or field).
    One by one word is searched in vocabulary and the file number is noted.
    The respective field files are opened and the document ids along with the frequencies are noted.
    The documents are ranked on the basis of TF-IDF scores.
    The title of the documents are extracted using title.txt

### Files Produced

    index*.txt (temporary intermediate files) : It consists of words with their posting list. Eg. cricket d1b2t4c5 d5b3t6l1
    title.txt : It consist of id-title mapping. ("id" is a custom id given to title of each page encountered in the wiki corpus)
    titleOffset.txt : Offset for title.txt file
    vocab.txt : It has all the words and the file number in which those words can be found along with the document frequency.
    offset.txt : Offset for vocab.txt
    [b|t|i|r|l|c]*.txt : It consists of words found in various sections of the article along with document id and frequency. (these files make up the final inverted index)
    offset_[b|t|i|r|l|c]*.txt : Offset for various field files.

### How to run:
python3 wiki_indexer.py

This function takes as input the corpus file and creates the entire index in a field separated manner. It also creates a vocabulary list and a file containg the title-id map. Along with these files, it also creates the offsets for all the files.

python3 wiki_search.py

The function reads the query to be searched from a file queries.txt. It returns the top k results from the Wikipedia corpus and writes it to queries_op.txt file.
k is specified by the user along with the queries.
