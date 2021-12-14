def combine_manual_keywords(uploaders_title_dict: dict):
    authors_with_keywords = []

    for entry in uploaders_title_dict:
        content_list = []
        for document in uploaders_title_dict.get(entry):
            my_file = open("../Data/keywords/" + document, "r")
            lines = my_file.readlines()
            content_list.append(([line.rstrip() for line in lines]))
        flat_list = [item for sublist in content_list for item in sublist]
        authors_with_keywords.append({entry: list(set(flat_list))})

    return authors_with_keywords


def complete_manual_term_list(uploader_title_dict: dict):
    content_list = []
    for entry in uploader_title_dict:
        for document in uploader_title_dict.get(entry):
            my_file = open("../Data/keywords/" + document, "r")
            lines = my_file.readlines()
            content_list.append(([line.rstrip() for line in lines]))
    complete_term_list = [item for sublist in content_list for item in sublist]
    return list(set(complete_term_list))