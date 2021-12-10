import pysolr


def solr_search(server: str = 'http://localhost:8983/solr/hsc-data/', query: str = "*",
                fuzzy: bool = False) -> pysolr.Results:
    solr = pysolr.Solr(server, always_commit=True)

    if query == '':
        query = '*:*'
    if fuzzy:
        query = query + '~'

    return solr.search(query, **{'rows': 100})
