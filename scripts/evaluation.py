
def calc_precision(uuid, results, statistics):
    true_positives = statistics['true_positives']  # TODO
    false_positives = statistics['false_positives']  # TODO

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

def calc_recall(uuid, results, statistics):
        true_positives = statistics['true_positives']  # TODO
        false_negatives = statistics['false_negatives']  # TODO

        actual_positives = true_positives + false_negatives
        if actual_positives == 0:
            recall = 0
        else:
            recall = true_positives / actual_positives

        print("{:<10s} = {:>6.2f}%".format(
            uuid,
            100 * recall
        ))
