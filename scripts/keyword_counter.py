import text_cleaner


def determine_authors(search_results):
    # for id in search_results.:
    authors = []
    for result in search_results:
        authors.append(result['author'])
    print('Extracted {} unique authors.'.format(len(set(authors))))
    # To remove duplicates, we can simply convert to a set and back to a list
    return list(set(authors))


# Returns list of dictionaries
def determine_keywords(search_results, authors):
    # Get unique authors
    authors_with_keywords = []
    for current_author in authors:
        if not current_author:
            continue

        # Iterate through all results
        combined_dict = {}
        for result in search_results:

            # When matching current author: tokenize and count
            if result['author'] is current_author:
                tokenized_text = text_cleaner.clean_text(result['content'][0].lower())
                occurrences = text_cleaner.create_count_set(tokenized_text)

                combined_dict = text_cleaner.combine_dicts(combined_dict, occurrences)
        sorted_keywords = sorted(combined_dict.items(), key=lambda x: x[1], reverse=True)

        authors_with_keywords.append({current_author: sorted_keywords[0:49]})
        print('Iterated through documents for {}'.format(current_author))

    return authors_with_keywords
