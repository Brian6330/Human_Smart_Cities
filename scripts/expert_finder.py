import pysolr

solr = pysolr.Solr("http://localhost:8983/solr/hsc-data/", always_commit=True)


def search_for_keyword(author_keyword_dict: list[dict], search_term="swiss", type_tuple=True, cut_off=49) -> list:
    matching_authors = []

    # Tuples must be handled differently (automatic variant)
    if type_tuple:
        for current_dict in author_keyword_dict:
            for author in current_dict:
                i = 0  # Keep track of the index, to know how "good" the match is
                for term in current_dict.get(author):
                    if term[0] == search_term:
                        matching_authors.append(tuple([author, ((cut_off-i)/cut_off)]))
                    i += 1

        # Sort authors by best match of keywords (the higher the occurrence of the keyword, the better)
        sorted_matching_authors = sorted(matching_authors, key=lambda tup: tup[1], reverse=True)

        return sorted_matching_authors

    # Manually extracted keywords just searches for matching author
    else:
        for current_dict in author_keyword_dict:
            for author in current_dict:
                for term in current_dict.get(author):
                    if term == search_term:
                        matching_authors.append(author)
        return matching_authors

