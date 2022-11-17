from ndicts.ndicts import NestedDict  # do czego to jest?

def build(tab):  # czemu tab?
    automat = {}
    state = 0 #stan poczatkowy - inkrementowany wraz z tworzeniem nowych stanow
    acc_states = [] #tablica [stany akceptujace,wzorce]  # lista
    trie_level = [] #tablica [poziom drzewa,stan]

    #Funkcja new_branch sprawdza czy z danego stanu (a_state) wychodzi juz galaz z dana literka ze wzorca.
    #Jesli nie to tworzymy nowa galaz i nowe stany (state)
    #Jesli istnieje galaz z dana literka to przechodzimy do nastepnego stanu i sprawdzamy go rekurencyjnie.

    #l_index - indeks w tablicy liter  # to czemu nie letter_index? 5 literek Pani szkoda?
    #a_state - sprawdzany stan  # analogicznie
    #state - numer nastepnego stanu
    #letters - tablica liter
    #level - przypisanie poziomu drzewa danemu stanowi  # czy to jest potrzebne?

    def new_branch(l_index, a_state, state, letters, level):
        #przypadek 1: gdy podajemy 2 wzorce gdzie pierwszy jest przedluzeniem drugiego, np. 'hej' 'heja'
        #problem -> KeyError bo kolejny klucz nie istnieje
        #rozwiazanie -> Tworzymy pozycje z nowym kluczem i rozwijamy nowa galaz

        if a_state not in automat:
            for j in range(l_index, len(letters)):
                automat[a_state] = {letters[j]: state + 1}
                a_state += 1
                state += 1
                trie_level.append([level, state])
                level += 1

            return state

        #przypadek 2: klucz juz istnieje ale szukana wartosc nie
        #1 krok -> dodajemy wartosc
        #2 krok -> rozwijamy reszte galezi

        elif letters[l_index] not in automat[a_state]:
            automat[a_state][letters[l_index]] = state + 1
            state += 1
            trie_level.append([level, state])
            level += 1

            for j in range(l_index+1, len(letters)):
                automat[state] = {letters[j]: state+1}
                state += 1
                trie_level.append([level, state])
                level += 1

            return state

        #przypadek 3: klucz i dana wartosc istnieja
        #krok 1: kopiujemy stan do sprawdzenia nastepnej litery
        #krok 2: inkrementujemy l_index -> nastepna litera
        #krok 3: sprawdzamy rekurencyjnie dla nowych parametrow wejsciowych
        else:
            if l_index==(len(letters)-1): #zabezpieczenie dla wpisania podwojnie jednego wyrazenia
                return state              #-> jesli ostatnia literka wyrazenia w else to calosc juz istniala
            else:
                level += 1
                a_state = automat[a_state][letters[l_index]]
                l_index += 1
                return new_branch(l_index, a_state, state, letters, level)



    #BUDUJEMY DRZEWO

    # 1st tree
    letters = list(tab[0])
    level = 1
    for j in range(len(letters)):
        automat[state] = {letters[j]: state + 1}
        state += 1
        trie_level.append([level, state])
        level += 1

    acc_states.append([state, tab[0]])

    # following trees
    for i in range(1, len(tab)):
        letters = list(tab[i])
        level = 1
        state = new_branch(0, 0, state, letters, level)
        acc_states.append([state, tab[i]])

    acc_states_dict = dict(acc_states)
        
    #FAILLINKI

    fail = []  # tablica z zagniezdzonymi tablicami [stan skad wychodzi faillink, stan docelowy faillinku]
    joker = [0, 0]
    fail.append(joker)

    trie_level = {k: row[0] for row in trie_level for k in row[1:]} #lepiej z dict jednak, poprawie kiedy indziej :p

    nd = NestedDict(automat)

    for i in range(1, state+1):  # to Pani nie gwarantuje przejścia wszerz
        if i in automat[0].values():
            fail.append([i, 0])
        elif trie_level.get(i) == 2: #dla 2 poziomu drzewa


            for key, value in nd.items():
                if value == i:
                    if key[1] not in list(automat[0].keys()):
                        fail.append([i, 0])
                    if key[1] in list(automat[0].keys()):
                        fail.append([i, automat[0][key[1]]])

        else:
            lett = [] #sprawdzamy czy taka kombinacja wychodzi z 0

            k = i
            for n in range(trie_level.get(i)-1):
                for key, value in nd.items():
                    if value == k:
                        lett.append(key[1])
                        k = key[0]

            lett = list(reversed(lett))

            state = 0
            for l in range(len(lett)):
                if lett[l] in automat[state].keys():
                    state = automat[state][lett[l]]

            fail.append([i, state])

    fail_dict={}  # lepiej z dict jednak
    for i in range(len(fail)):
        fail_dict[fail[i][0]] = fail[i][1]

    return automat, fail_dict, acc_states_dict

def search(string, trie, fail, acc_states):
    indexes = []

    state = 0
    index_now = 0 #zabezpieczenia dla powtarzalnosci wzorcow (str.index podaje miejsce pierwszego wzorca)
    for i in string:
        if i in trie[state].keys():
            state = trie[state][i]
            index_now += 1
            if state in acc_states.keys(): #jesli stan akceptujacy to zwracam pozycje poczatkowa wzorca
                indexes.append(string.index(acc_states[state], (index_now-len(acc_states[state])), index_now))
                state = fail[state] #i ide faillinkiem dalej
                if state not in trie.keys(): #zabezpieczenie dla faillinka prowadzacego do stanu akceptujacego
                    indexes.append(string.index(acc_states[state], (index_now - len(acc_states[state])), index_now))
                    state = fail[state]
        else:
            state = fail[state] #jesli nie ma to idziemy po faillinku
            if i in trie[state].keys():
                state = trie[state][i]
            index_now += 1
            #jesli znowu nie ma to nie robimy nic (joker) i idziemy do nastepnej litery

    return indexes

if __name__ == '__main__':
    try:
        sample = ["abcbc", "bc"]  # przykladowy wzorzec
        automat, faillink, acc_states = build(sample)  # KeyError
        print("Drzewo: ", automat)
        print("Faillinki: ", faillink)
        print("Stany akceptujace: ", acc_states)
        indexes = search("aaabcbcbc", automat, faillink, acc_states)  # dużo argumentów
        print("Wystapienia wzorcow: ", indexes)
    except TypeError:
        print("Sprawdz czy wprowadziles napisy w sample i search (pierwsza zmienna)!")



