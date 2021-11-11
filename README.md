# Human_Smart_Cities

## How to Set up SOLR (WIP)
Source: https://solr.apache.org/guide/8_10/solr-tutorial.html

From within the solr-8.10.1, run the following command:  
`solr-8.10.0:$ ./bin/solr start -e cloud`

Make sure to use port 8983 if you want to use the script to start.

Add a collection, (best done when starting up), 
the collection should use `sample_techproducts_configs` config, 
the rest of the parameters can be ignored for now.

Use pip (or similar) to install pySolr (e.g. `pip install pysolr`).  
Then you can use the python scripts to interact with solr. 


Once you're done, use ` .\bin\solr stop -all` to stop all running solr instances

## Uploading Files
- In `pdf_uploader`, enter your collection and let it run to upload all *.pdfs in root/Data.

### Uploading Files Manually
- Open http://localhost:8983/solr.
- Navigate to the collection you wish to upload files in.
- Go to the entry "documents" under your collection, i.e. http://localhost:8983/solr/#/YOUR_COLLECTION/documents
- Change Request Handler to `/update/extract` and select Document Type "File Upload".
- Select the document to upload.
- If uploading a pdf, add the following Extracting Request Handler Parameter "literal.id" and enter a unique ID.
- Now click "Submit Document" and check that your document has been uploaded. 

## Querying Tips
- Appending `~` to the query, allows one to use the default error-tolerance of solr, which is 2 characters.

## Deleting a collection
- ./bin/solr delete -c collection_name then restart with bin/solr restart -p 8983
- Alternatively, can be deleted in the web-interface.