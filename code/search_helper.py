import config


def find_file_no(low, high, offset_list, word, fptr):
    # print("IN FIND_FILE_NO")
    # print("TO search: ", word, " low:", low, " high:", high)

    while low < high:
        mid = int((low + high) / 2)
        fptr.seek(offset_list[mid])
        word_ptr = fptr.readline().strip().split()
        # print("word_ptr: ", word_ptr)
        if word == word_ptr[0]:
            return word_ptr[1:], mid
        elif word < word_ptr[0]:
            high = mid
        else:
            low = mid + 1
    return [], -1


def find_docs(fptr_field_file, file_no, field, word):
    # print("IN find_docs")
    field_offset = []
    doc_freq = []

    filename = config.OUTPUT_FOLDER_PATH + 'offset_' + field + file_no + '.txt'
    with open(filename, 'r') as f:
        for line in f:
            offset, df = line.strip().split()
            field_offset.append(int(offset))
            doc_freq.append(int(df))
    doc_list, mid = find_file_no(0, len(field_offset), field_offset, word, fptr_field_file)
    if mid == -1:  # word not found (eg: in case of simple query word, for a specific field)
        return doc_list, 0
    else:
        # print("doc_list: ", doc_list, " doc_freq[mid]: ", doc_freq[mid])
        return doc_list, doc_freq[mid]  # doc_freq[mid] will basically be equal to len of doc_list


def fetch_doc_titles(low, high, title_offset_list, doc_id, fptr_id_title):
    # print("IN fetch_doc_titles; doc_id:", doc_id)
    # print("low high: ", low, high)
    while low < high:
        mid = int((low + high) / 2)
        fptr_id_title.seek(title_offset_list[mid])
        word_ptr = fptr_id_title.readline().strip().split()
        # print("Word_ptr: ", word_ptr)
        if int(doc_id) == int(word_ptr[0]):
            return word_ptr[1:], mid
        elif int(doc_id) < int(word_ptr[0]):
            high = mid
        else:
            low = mid + 1
    return [], -1


