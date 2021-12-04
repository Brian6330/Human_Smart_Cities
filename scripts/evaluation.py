import pysolr

import keyword_counter

solr = pysolr.Solr("http://localhost:8983/solr/hsc-data/", always_commit=True)

search_results = solr.search('*')
authors = keyword_counter.determine_authors(search_results)
author_keyword_dict = keyword_counter.determine_keywords(search_results, authors)


def calculate_statistics(search_results):
    for current_author in authors:
        file_titles = []
        for result in search_results:
            file_titles.append(search_results['title'])

        keywords = []
        for title in file_titles:
            print("")

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
