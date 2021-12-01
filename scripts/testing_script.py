import pysolr

import text_cleaner

solr = pysolr.Solr("http://localhost:8983/solr/hsc-data/", always_commit=True)

search_results = solr.search('*')

# for id in search_results.:
authors = []
for result in search_results:
    authors.append(result['author'])
print('extracted authors')

# Get unique authors
authors_with_keywords = []
for current_author in set(authors):
    # Iterate through all results
    combined_dict = {"empty": 1}
    for result in search_results:

        # When matching current author: tokenize and count
        if result['author'] is current_author:
            tokenized_text = text_cleaner.clean_text(result['content'][0].lower())
            occurrences = text_cleaner.create_CountSet(tokenized_text)

            combined_dict = text_cleaner.combineDicts(combined_dict, occurrences)
    sorted_keywords = sorted(combined_dict.items(), key=lambda x: x[1], reverse=True)

    authors_with_keywords.append({current_author: sorted_keywords})
    print('iterated through: ', current_author)

print(authors_with_keywords)
print('done')
