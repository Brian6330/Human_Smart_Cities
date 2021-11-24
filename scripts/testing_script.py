import pysolr

import text_cleaner

solr = pysolr.Solr("http://localhost:8983/solr/hsc-data/", always_commit=True)

search_results = solr.search('*')

# for id in search_results.:
# TODO per document / author to then discern the occurence of keywords per document
for result in search_results:

    text_cleaner.clean_text(result['content'][0])

print('done')