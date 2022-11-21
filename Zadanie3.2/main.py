import copy


def token_generator(filename, filetype):
    if filetype == 'txt':
        with open(filename, 'r', encoding='UTF-8') as file:
            for line in file:
                words = line.split()  # dzieli po ciagu bialych znakow
                for word in words:
                    yield word


def word_generator(filename, filetype):
    sentence = []
    for token in token_generator(filename, filetype):
        yield token


def delete_characters(sentence):
    characters = [",", ".", ":", ";", "!", "?", "-"]
    sentence = sentence.lower()
    for i in range(len(characters)):
        if characters[i] in sentence:
            sentence = sentence.replace(characters[i], "")  # usuwanie znakow
    return sentence


def count_words(filename, filetype, n_most_frequent):
    words_freq = {}

    for word in word_generator(filename, filetype):
        word = delete_characters(word)  # usuwam znaki interpunkcyjne
        if word != "":  # zabezpieczenie przed pustym stringiem po usunieciu interpunkcji
            #print(word)
            if word not in words_freq:
                words_freq[word] = 1
            else:
                words_freq[word] += 1
        #if word == 'nigdy':
        #    break

    #print(words_freq)
    return search_most_frequent(words_freq, n_most_frequent)


def search_most_frequent(words_freq, n_most_frequent, dict_most_frequent={}):

    words_freq_copy = copy.copy(words_freq) #kopiuje slownik do modyfikacji w petli for

    if words_freq == {}:
        print("Nie ma aż tylu częstości wystąpywań w załączonym tekście!")
        return dict_most_frequent

    maximum = max(words_freq.values())

    for i in words_freq:

        if words_freq_copy[i] == maximum:
            dict_most_frequent[i] = maximum
            words_freq_copy.pop(i)

    n_most_frequent = n_most_frequent - 1
    if n_most_frequent>0:
        return search_most_frequent(words_freq_copy, n_most_frequent, dict_most_frequent)
    return dict_most_frequent


print(count_words("potop.txt", "txt", 3))
