import pysolr
import keyword_counter
import statistics_hsc
import util_hsc

solr = pysolr.Solr("http://localhost:8983/solr/hsc-data/", always_commit=True)

search_results = solr.search('*')
authors = keyword_counter.determine_authors(search_results)
automatic_author_keyword_dict = keyword_counter.determine_keywords(search_results, authors)


# TODO adapt this for statistics
def search_for_keyword(author_keyword_dict, search_term="swiss", type_tuple=True):
    matching_authors = []
    # Tuples must be handled differently (automatic variant)
    if type_tuple:
        for current_dict in author_keyword_dict:
            for author in current_dict:
                i = 0  # Keep track of the index, to know how "good" the match is
                for term in current_dict.get(author):
                    if term[0] == search_term:
                        matching_authors.append(tuple([author, i]))
                    i += 1
        # Sort authors by best match of keywords (the higher the occurrence of the keyword, the better)
        sorted_matching_authors = sorted(matching_authors, key=lambda tup: tup[1])

        # Extract only the authors in order of best match
        sorted_matching_authors_only = [a_tuple[0] for a_tuple in sorted_matching_authors]
        # TODO Score by index
        return list(sorted_matching_authors_only)

    # Manually extracted keywords just searches for matching author
    else:
        for current_dict in author_keyword_dict:
            for author in current_dict:
                for term in current_dict.get(author):
                    if term == search_term:
                        matching_authors.append(author)
        # Remove duplicates and return the list
        return list(matching_authors)


# print(search_for_keyword(manual_keyword_author_dict, "data"))
# print(search_for_keyword(automatic_author_keyword_dict, "data", type_tuple=True))
