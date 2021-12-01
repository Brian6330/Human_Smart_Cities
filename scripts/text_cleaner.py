# Tokenize words and remove stop-words
from nltk.tokenize import word_tokenize
from stop_words import get_stop_words

# First time setup required for nltk; https://www.nltk.org/data.html

stop_words = get_stop_words('english')


def clean_text(text):
    tokenized_words = word_tokenize(text)
    cleaned_word_list = []
    for word in tokenized_words:
        if len(word) > 3 and word not in stop_words:
            cleaned_word_list.append(word)

    return cleaned_word_list


def create_count_set(word_list):
    word_set = set(word_list)
    word_dict = {}
    for x in word_set:
        count = 0
        for y in word_list:
            if y == x:
                count += 1

        word_dict[x] = count

    return word_dict


def combine_dicts(dict1, dict2):
    new_dict = {}
    word_set = set()
    for x in dict1:
        word_set.add(x)
    for y in dict2:
        word_set.add(y)

    for z in word_set:
        count = 0
        if z in dict1:
            count += dict1[z]
        if z in dict2:
            count += dict2[z]
        new_dict[z] = count

    return new_dict
