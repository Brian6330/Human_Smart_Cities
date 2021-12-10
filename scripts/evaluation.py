import random
from nltk.corpus import words
import pysolr
import keyword_counter

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


def combine_manual_keywords(uploaders_title_dict):
    authors_with_keywords = []

    for entry in uploaders_title_dict:
        content_list = []
        for document in uploaders_title_dict.get(entry):
            my_file = open("../Data/keywords/" + document, "r")
            lines = my_file.readlines()
            content_list.append(([line.rstrip() for line in lines]))
        flat_list = [item for sublist in content_list for item in sublist]
        authors_with_keywords.append({entry: list(set(flat_list))})

    return authors_with_keywords


def search_for_keyword(author_keyword_dict, search_term="swiss", type_tuple=False):
    matching_authors = []
    # Tuples must be handled differently (automatic variant)
    if type_tuple:
        for current_dict in author_keyword_dict:
            for author in current_dict:
                i = 0  # Keep track of the index, to know how "good" the match is
                for term in current_dict.get(author):
                    if term[0] == search_term:
                        matching_authors.append(tuple([author, i]))
                    i += 1
        # Sort authors by best match of keywords (the higher the occurrence of the keyword, the better)
        sorted_matching_authors = sorted(matching_authors, key=lambda tup: tup[1])
        # Extract only the authors in order of best match
        sorted_matching_authors_only = [a_tuple[0] for a_tuple in sorted_matching_authors]
        return list(set(sorted_matching_authors_only))

    # Manually extracted keywords just searches for matching author
    else:
        for current_dict in author_keyword_dict:
            for author in current_dict:
                for term in current_dict.get(author):
                    if term == search_term:
                        matching_authors.append(author)
        # Remove duplicates and return the list
        return list(set(matching_authors))


def complete_manual_term_list(uploader_title_dict):
    content_list = []
    for entry in uploader_title_dict:
        for document in uploader_title_dict.get(entry):
            my_file = open("../Data/keywords/" + document, "r")
            lines = my_file.readlines()
            content_list.append(([line.rstrip() for line in lines]))
    complete_term_list = [item for sublist in content_list for item in sublist]
    return complete_term_list


def calc_precision(true_positives, false_positives):
    total_positives = true_positives + false_positives

    # Rare that it happens, but always possible
    if total_positives == 0:
        return 1
    else:
        return true_positives / total_positives


def calc_recall(true_positives, false_negatives):
    actual_positives = true_positives + false_negatives

    # Rare that it happens, but always possible
    if actual_positives == 0:
        return 0
    else:
        return true_positives / actual_positives


def evaluate_matches(manual_dict, automatic_dict, term_list="",
                     random_list=False):
    author_choice_tp = 0
    author_choice_tn = 0
    author_choice_fp = 0
    author_choice_fn = 0

    for _ in range(200):
        selected_word = random.choice(term_list)
        if random_list:
            selected_word = random.sample(words.words(), 1)

        manual_matches = search_for_keyword(manual_dict, selected_word)
        automatic_matches = search_for_keyword(automatic_dict, selected_word, type_tuple=True)

        # Both lists have matches and the first or second expert are matching
        if manual_matches and automatic_matches:
            if len(automatic_matches) >= 2:
                if automatic_matches[0] in manual_matches or automatic_matches[1] in manual_matches:
                    author_choice_tp += 1
            elif automatic_matches in manual_matches:
                author_choice_tp += 1

        # If no matching results in manual list, but matching in automatic -> false positive
        elif not manual_matches and automatic_matches:
            author_choice_fp += 1

            # Manual matches but no automatic matches -> false negative
        elif manual_matches and not automatic_matches:
            author_choice_fn += 1

        # Both lists return no matches -> true negative
        elif not manual_matches and not automatic_matches:
            author_choice_tn += 1

    return author_choice_tp, author_choice_fp, author_choice_fn, author_choice_tn


manual_keyword_author_dict = combine_manual_keywords(uploader_title_dict)
manual_terms = complete_manual_term_list(uploader_title_dict)

automatic_terms = []
for current_dict in automatic_author_keyword_dict:
    for author in current_dict:
        for term in current_dict.get(author):
            automatic_terms.append(term[0])

all_terms = automatic_terms + manual_terms

tp, fp, fn, tn = evaluate_matches(manual_keyword_author_dict, automatic_author_keyword_dict, all_terms)
print("True positives: {}; False Positives: {}; False Negatives: {}; True Negatives: {}".format(tp, fp, fn, tn))

precision = calc_precision(tp, fp)
recall = calc_recall(tp, fn)

print("Precision: {}; Recall {}".format(precision, recall))

# print(search_for_keyword(manual_keyword_author_dict, "data"))
# print(search_for_keyword(automatic_author_keyword_dict, "data", type_tuple=True))
