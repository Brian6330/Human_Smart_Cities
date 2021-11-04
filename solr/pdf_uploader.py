from tika import parser
import pysolr


solr = pysolr.Solr("http://localhost:8983/solr/upload-test/", always_commit=True)


#### Testing Tika to manually import extracted text
file_data = parser.from_file("Data/asrbradiationcodeportingdocumentationpriscofreifinal.pdf")

# file_data['content'] is used to get the content of the pdf file.
output = file_data['content']

# This output.encode encodes the text into utf-8 format.
output = output.encode('utf-8', errors='replace')

# for debugging: saves the extracted text to a file called output.txt
# with open('output_file.txt', 'w') as the_file:
#     the_file.write(str(output))

# solr.add([
#     {
#         "title": "tika tika tika",
#         "text": output
#     }
# ])

###


# TODO get the following working to POST pdf files
# f = open("Data/asrbradiationcodeportingdocumentationpriscofreifinal.pdf", mode='r', encoding='utf-8', errors='ignore')
# f_bi = open("Data/asrbradiationcodeportingdocumentationpriscofreifinal.pdf", mode='rb', encoding='utf-8', errors='ignore')
# solr.extract(f)


results = solr.search('*') # Can be replaced by what you one
print("Saw {0} result(s).".format(len(results)))
print("Current result after simple query:", results)
