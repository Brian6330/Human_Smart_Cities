# Tokenize words and remove stop-words
from nltk.tokenize import word_tokenize
from stop_words import get_stop_words

# First time setup required for nltk; https://www.nltk.org/data.html

stop_words = get_stop_words('english')


# TODO: Clean-up
def clean_text(text):
    tokenized_words = word_tokenize(text)
    cleaned_word_list = []
    for word in tokenized_words:
        if len(word) > 3 and word not in stop_words:
            cleaned_word_list.append(word)

    return cleaned_word_list


# TODO
def create_CountSet(word_list):
    word_set = set(word_list)
    wordDict = {}
    for x in word_set:
        count = 0
        for y in word_list:
            if y == x:
                count += 1

        wordDict[x] = count

    return wordDict


def combineDicts(dict1, dict2):
    newDict = {}
    wordSet = set()
    for x in dict1:
        wordSet.add(x)
    for y in dict2:
        wordSet.add(y)

    for z in wordSet:
        count = 0
        if z in dict1:
            count += dict1[z]
        if z in dict2:
            count += dict2[z]
        newDict[z] = count

    return newDict


def convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct