import pysolr
import keyword_counter
import statistics_hsc
import util_hsc


solr = pysolr.Solr("http://localhost:8983/solr/hsc-data/", always_commit=True)

uploader_title_dict = {
    "Jeannette Nötzli": ["PERMOS_DataPolicy.txt"],
    "Prisco Frei (prisco.f@hotmail.com)": ["asrbradiationcodeportingdocumentationpriscofreifinal.txt"],
    "jk": ["toolkit-01-graphing-distributions.txt", "toolkit-02-quantifying-distributions.txt",
           "toolkit-03-transforming-distributions.txt", "toolkit-04-confidence-intervals.txt",
           "toolkit-04-confidence-intervals.txt", "toolkit-05-error-propagation.txt",
           "toolkit-06-nonlinear-averaging.txt", "toolkit-07-hypothesis-testing.txt",
           "toolkit-08-hodges-lehmann-estimators.txt", "toolkit-10-linear-regression.txt",
           "toolkit-11-serial-correlation.txt", "toolkit-12-weighted-averages-and-uncertainties.txt"],
    "Hüsler Fabia BAFU": ["Noetzli-2019-Mountain_permafrost_hydrology._Eine_Studie-(published_version).txt"],
    "Franziska Gerber and Varun Sharma, EPF Lausanne and WSL-SLF Davos, 2018": ["cosmowrfdocumentation.txt"],
    "karger": ["CHELSA_EUR11_technical_documentation.txt"],
}

search_results = solr.search('*')
authors = keyword_counter.determine_authors(search_results)
automatic_author_keyword_dict = keyword_counter.determine_keywords(search_results, authors)


manual_keyword_author_dict = util_hsc.combine_manual_keywords(uploader_title_dict)
manual_terms = util_hsc.complete_manual_term_list(uploader_title_dict)

automatic_terms = []
for current_dict in automatic_author_keyword_dict:
    for author in current_dict:
        for term in current_dict.get(author):
            automatic_terms.append(term[0])

all_terms = automatic_terms + manual_terms

tp, fp, fn, tn = statistics_hsc.evaluate_matches(manual_keyword_author_dict, automatic_author_keyword_dict, all_terms)
print("True positives: {}; False Positives: {}; False Negatives: {}; True Negatives: {}".format(tp, fp, fn, tn))

precision = statistics_hsc.calc_precision(tp, fp)
recall = statistics_hsc.calc_recall(tp, fn)

print("Precision: {}; Recall {}".format(precision, recall))
