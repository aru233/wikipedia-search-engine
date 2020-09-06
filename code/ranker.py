from collections import defaultdict
import math


def rank(qtype, results, docFreq, nfiles):
    docs = defaultdict(float)

    # s1 = defaultdict(int)
    # s2 = defaultdict(int)
    queryIdf = {}

    for key in docFreq:
        queryIdf[key] = math.log((float(nfiles) - float(docFreq[key]) + 0.5) / (float(docFreq[key]) + 0.5))
        docFreq[key] = math.log(float(nfiles) / float(docFreq[key]))

    for word in results:
        fieldWisePostingList = results[word]
        for field in fieldWisePostingList:
            if len(field) > 0:
                field = field
                postingList = fieldWisePostingList[field]
                if field == 't':
                    factor = 0.25
                if field == 'b':
                    factor = 0.25
                if field == 'i':
                    factor = 0.20
                if field == 'c':
                    factor = 0.1
                if field == 'r':
                    factor = 0.05
                if field == 'l':
                    factor = 0.05
                for i in range(0, len(postingList), 2):
                    # s1[postingList[i]] += float((1 + math.log(float(postingList[i+1]))) * docFreq[word]) ** 2
                    # s2[postingList[i]] += float(queryIdf[word]) ** 2
                    docs[postingList[i]] += float(factor * (1 + math.log(float(postingList[i + 1]))) * docFreq[word])

    # for key in docs:
    #    docs[key] /= float(math.sqrt(s1[key])) * float(math.sqrt(s2[key]))

    return docs
