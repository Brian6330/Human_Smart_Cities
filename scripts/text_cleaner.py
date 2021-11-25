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


# words_counted = []
# for i in words:
#     words_counted.append((words.count(i), i))
#     if counter % 1000 == 0:  # speed improvement, because otherwise console output limits speed
#         print("Line " + str(int(counter / 1000)) + "k of: " + str(int(len(words) / 1000)) + "k")
#     counter += 1

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
        if (dict1[z]):
            count += dict1[z]
        if (dict2[z]):
            count += dict2[z]

        newDict[z] = count

    return newDict
    
