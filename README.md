# Human_Smart_Cities


## How to Set up SOLR (WIP)
Source: https://solr.apache.org/guide/8_10/solr-tutorial.html

Once properly downloaded, from the folder where you've extracted it (e.g. solr-8.10.0) run:  
`solr-8.10.0:$ ./bin/solr start -e cloud`

Make sure to use port 8983 if you want to use the script to start.

Add a collection (can be done in the browser on http://localhost:8983/solr), the collection should have default config, the rest of the parameters can be ignored for now.

Use pip (or similar) to install pySolr (e.g. `pip install pysolr`).  
Then you can use the script to add and remove content, as well as make queries. The same can of course be done in the browser.

Once you're done, use `solr stop -all` to stop all running solr instances

## Uploading Files
- Open http://localhost:8983/solr.
- Navigate to the collection you wish to upload files in.
- Go to the entry "documents" under your collection, i.e. http://localhost:8983/solr/#/YOUR_COLLECTION/documents
- Change Request Handler to `/update/extract` and select Document Type "File Upload".
- Select the document to upload.
- If uploading a pdf, add the following Extracting Request Handler Parameter "literal.id" and enter a unique ID.
- Now click "Submit Document" and check that your document has been uploaded. 

## Querying data
- Appending `~` to the query, allows one to use the default error-tolerance of solr, which is 2 characters.