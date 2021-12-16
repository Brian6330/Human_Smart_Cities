import random
from nltk.corpus import words
from expert_finder import search_for_keyword

# search_results = solr.search('*')
# authors = keyword_counter.determine_authors(search_results)
# automatic_author_keyword_dict = keyword_counter.determine_keywords(search_results, authors)


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


def evaluate_matches(manual_dict: dict, automatic_dict: dict, iterations: int, term_list="",
                     random_list=False, threshold=49) -> (float, float, float, float, float):
    author_choice_tp = 0
    author_choice_tn = 0
    author_choice_fp = 0
    author_choice_fn = 0

    for _ in range(iterations):
        selected_word = random.choice(term_list)
        if random_list:
            selected_word = random.sample(words.words(), 1)

        manual_matches = search_for_keyword(manual_dict, selected_word, False, threshold)
        automatic_matches = search_for_keyword(automatic_dict, selected_word, True, threshold)

        # Both lists have matches
        if manual_matches and automatic_matches:
            if len(automatic_matches) >= 2:
                if automatic_matches[0][0] in manual_matches or automatic_matches[1][0] in manual_matches:
                    author_choice_tp += 1
            elif automatic_matches[0][0] in manual_matches:
                author_choice_tp += 1
            else:
                author_choice_fn

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
