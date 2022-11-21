import copy


#funkcje do generowania słów
def word_generator(filename, filetype):
    if filetype == 'txt':
        with open(filename, 'r', encoding='UTF-8') as file:
            for line in file:
                words = line.split()  # dzielimy po białych znakach
                for word in words:
                    word = delete_characters(word) # usuwam znaki interpunkcyjne
                    yield word


# funkcja służąca do usuwania znaków interpunkcyjnych ze stringa
def delete_characters(string):
    #czy jest jakiś mądrzejszy sposób na pozbycie się x84?
    characters = [",", ".", ":", ";", "!", "?", "-", "\x84", "\"", "(", ")"]
    string = string.lower()
    for i in range(len(characters)):
        if characters[i] in string:
            string = string.replace(characters[i], "")  # usuwanie znakow
    return string


#fukcja zwracająca wystąpienia słów w tekście w postaci słownika {słowo:wystąpienia}
def count_words(filename, filetype):
    words_freq = {}

    for word in word_generator(filename, filetype):
        if word != "":  # zabezpieczenie przed pustym stringiem po usunieciu interpunkcji
            if word not in words_freq:
                words_freq[word] = 1
            else:
                words_freq[word] += 1

    return words_freq


#funkcja przyjmująca słownik z wystąpieniami słów w tekście (words_freq)
#umożliwia wyświetlenie n najczęściej występujących słów (n_most_frequent)
#z uwzględnieniem remisów
def search_most_frequent(words_freq, n_most_frequent=None, dict_most_frequent={}):

    # jeśli n_most_frequent nie zostanie podane, to funkcja zwraca wszystkie wystąpienia
    if n_most_frequent==None:
        return words_freq

    words_freq_copy = copy.copy(words_freq) #kopiuje slownik do modyfikacji w petli for

    # zabezpieczenie dla tekstu w ktorym ilość wystąpien mniejsza od n_most_frequent
    # (np. same pojedyncze wystąpienia i n_most_frequent=2)
    if words_freq == {}:
        print("Nie ma aż tylu częstości wystąpywań w załączonym tekście!")
        return dict_most_frequent

    #wszystkie najczęstsze wystąpienia umieszczam w dict_most_frequent={} i usuwam z words_freq_copy
    #rekurencyjnie powtarzam dla zredukowanego słownika n_most_frequent razy
    #takie postępowanie pozwala na uwzględnienie remisów

    greatest_frequence = max(words_freq.values())

    for i in words_freq:

        if words_freq_copy[i] == greatest_frequence:
            dict_most_frequent[i] = greatest_frequence
            words_freq_copy.pop(i)

    n_most_frequent = n_most_frequent - 1
    if n_most_frequent>0:
        return search_most_frequent(words_freq_copy, n_most_frequent, dict_most_frequent)
    return dict_most_frequent


#5 najczęściej występujących słów w pliku potop.txt
print(search_most_frequent(count_words("potop.txt", "txt"), 5))

