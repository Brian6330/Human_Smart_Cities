import uuid
import os
import pysolr

# Syntax is http://localhost:8983/solr/YOUR-COLLECTION-HERE/
solr = pysolr.Solr("http://localhost:8983/solr/pdf-uploader/", always_commit=True)

for entry in os.scandir("../Data"):
    if (entry.path.endswith(".pdf") and entry.is_file):
        generated_id = {"literal.id": uuid.uuid4()}
        f = open(entry.path, mode='rb')
        solr.extract(file_obj=f, extractOnly=False, handler="update/extract", **generated_id)
        print("Uploaded file: {}".format(entry.path))


results = solr.search('*')
print("Saw {0} result(s) in total.".format(len(results)))
