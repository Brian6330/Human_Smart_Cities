import pysolr

import text_cleaner

solr = pysolr.Solr("http://localhost:8983/solr/hsc-data/", always_commit=True)

search_results = solr.search('*')

# for id in search_results.:
authors = []
for result in search_results:
    authors.append(result['author'])
print('Extracted {} unique authors.'.format(len(set(authors))))

# Get unique authors
authors_with_keywords = []
for current_author in set(authors):
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

print(authors_with_keywords)
print('done')
