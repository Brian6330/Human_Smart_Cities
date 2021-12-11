import text_cleaner


# Returns list of dictionaries
def determine_keywords(search_results, cut_off=49) -> list[dict]:
    """
    Returns a list of dictionaries containing authors and a tuple of word: occurrences:
    search_results: The solr search results to be processed
    cut_off: Up to what "rank" of keywords should be kept, default is 49 leading to the 50 most prevalent keywords
    """
    # Get unique authors
    authors = determine_authors(search_results)
    authors_with_keywords = []
    for current_author in authors:

        # Skip if empty string
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

        if cut_off <= len(sorted_keywords):
            authors_with_keywords.append({current_author: sorted_keywords[0:cut_off]})
        else:
            authors_with_keywords.append({current_author: sorted_keywords})

        print('Iterated through documents for {}'.format(current_author))

    return authors_with_keywords


def determine_authors(search_results) -> list[str]:
    """
    Returns a list of unique authors, found within the solr search_results:
    search_results: The solr search results to be processed
    """
    authors = []
    for result in search_results:
        authors.append(result['author'])
    print('Extracted {} unique authors.'.format(len(set(authors))))
    # To remove duplicates, we can simply convert to a set and back to a list (note: order is destroyed!)
    return list(set(authors))
