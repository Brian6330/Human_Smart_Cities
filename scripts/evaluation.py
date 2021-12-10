import random

import pysolr

import keyword_counter
import text_cleaner

solr = pysolr.Solr("http://localhost:8983/solr/hsc-data/", always_commit=True)

search_results = solr.search('*')
authors = keyword_counter.determine_authors(search_results)
automatic_author_keyword_dict = keyword_counter.determine_keywords(search_results, authors)

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


def combine_manual_keywords(uploader_title_dict):
    authors_with_keywords = []

    for entry in uploader_title_dict:
        content_list = []
        for document in uploader_title_dict.get(entry):
            my_file = open("../Data/keywords/" + document, "r")
            lines = my_file.readlines()
            content_list.append(([line.rstrip() for line in lines]))
        flat_list = [item for sublist in content_list for item in sublist]
        # TODO Test with set
        authors_with_keywords.append({entry: flat_list})

    return authors_with_keywords


def search_for_keyword(author_keyword_dict, search_term="swiss", type_tuple=False):
    matching_authors = []
    # Tuples must be handled differently (automatic variant)
    if type_tuple:
        for current_dict in author_keyword_dict:
            for author in current_dict:
                i = 0 # Keep track of the index, to know how "good" the match is
                for term in current_dict.get(author):
                    if term[0] == search_term:
                        matching_authors.append(tuple([author, i]))
                    i += 1
        # Sort authors by best match of keywords (the higher the occurrence of the keyword, the better)
        sorted_matching_authors = sorted(matching_authors, key=lambda tup: tup[1])
        # Extract only the authors in order of best match
        sorted_matching_authors_only = [a_tuple[0] for a_tuple in sorted_matching_authors]
        return set(sorted_matching_authors_only)

    # Manually extracted keywords just searches for matching author
    else:
        for current_dict in author_keyword_dict:
            for author in current_dict:
                for term in current_dict.get(author):
                    if term == search_term:
                        matching_authors.append(author)
        return set(matching_authors)


def complete_manual_term_list(uploader_title_dict):
    content_list = []
    for entry in uploader_title_dict:
        for document in uploader_title_dict.get(entry):
            my_file = open("../Data/keywords/" + document, "r")
            lines = my_file.readlines()
            content_list.append(([line.rstrip() for line in lines]))
    complete_term_list = [item for sublist in content_list for item in sublist]
    return complete_term_list


# def select_random_author(all_authors):
#     return all_authors[random.randint(0, len(all_authors))]


# def calculate_statistics(search_results):
# for current_author in authors:
#     file_titles = []
#     for result in search_results:
#         file_titles.append(search_results['title'])
#
#     keywords = []
#     for title in file_titles:
#         print("")

# true_positives = calc_true_positives(current_author, combined_dict, manual_dict)


def calc_true_positives(author, combined_dict, manual_dict):
    # TODO
    print("")


def calc_false_positives(author, combined_dict, manual_dict):
    # TODO
    print("")


def calc_true_negatives(author, combined_dict, manual_dict):
    # TODO
    print("")


def calc_false_positives(author, combined_dict, manual_dict):
    # TODO
    print("")


def calc_precision(uuid, results, true_positives, false_positives):
    total_positives = true_positives + false_positives

    # Rare that it happens, but always possible
    if total_positives == 0:
        precision = 1
    else:
        precision = true_positives / total_positives
    print("{:<10s} = {:>6.2f}%".format(
        uuid,
        100 * precision
    ))


def calc_recall(uuid, results, true_positives, false_negatives):
    actual_positives = true_positives + false_negatives
    if actual_positives == 0:
        recall = 0
    else:
        recall = true_positives / actual_positives

    print("{:<10s} = {:>6.2f}%".format(
        uuid,
        100 * recall
    ))


manual_keyword_author_dict = combine_manual_keywords(uploader_title_dict)
complete_manual_term_list = complete_manual_term_list(uploader_title_dict)

# TODO Challenger

# TODO Statistics

print(search_for_keyword(manual_keyword_author_dict, "data"))
print(search_for_keyword(automatic_author_keyword_dict, "data", type_tuple=True))
