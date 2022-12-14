from common_functions import txt_to_dict, next_month

#funkcja aktualizujaca books.txt po zmianach uzyta w dalszych funkcjach
def rewrite_book_list(books_dict,details,isbn):
    new_details = ""

    for i in range(len(details)):
        new_details = new_details + details[i] + "|"

    del books_dict[isbn]
    f = open("books.txt", "w", encoding='UTF-8')
    for book in books_dict:
        f.write(book + "; " + books_dict[book] + "\n")
    f.write(isbn + "; " + new_details[:-1] + "\n")
    f.close()

def borrow_book(username):
    isbn = input("Podaj isbn ksiazki ktora chcesz pozyczyc: >> ")

    try:
        books_dict = txt_to_dict("books.txt")
        details = books_dict[isbn].split("|")

        if details[2]!="x":
            print("Podana ksiazka jest wypozyczona uzytkownikowi " + username + ".")
        elif details[2]=="x":
            print("Ksiazka zostala pomyslnie wypozyczona na miesiac! Data zwrotu: ", next_month())
            details[2] = username + "*" + next_month()

            rewrite_book_list(books_dict, details, isbn)

    except KeyError:
        print("Numer ISBN " + isbn + " nie został znalezniony w bazie danych")


def reserve_book(username):
    isbn = input("Podaj isbn ksiazki ktora chcesz zarezerwowac: >> ")

    try:
        books_dict = txt_to_dict("books.txt")

        details = books_dict[isbn].split("|")

        if details[3]!="0":
            print("Podana ksiazka jest zarezerwowana przez uzytkownika " + details[3] + ".")
        elif details[3]=="0":
            print("Ksiazka zostala pomyslnie zarezerwowana!")
            details[3] = username

            rewrite_book_list(books_dict, details, isbn)

    except KeyError:
        print("Numer ISBN " + isbn + " nie został znalezniony w bazie danych")


def extend_deadline(username):
    isbn = input("Podaj isbn ksiazki ktora chcesz przedluzyc: >> ")

    try:
        books_dict = txt_to_dict("books.txt")
        details = books_dict[isbn].split("|")

        if username not in details[2]:
            print("Podana ksiazka nie jest zarezerwowana przez uzytkownika " + details[3] + ". Sprobuj ponownie!")

        elif username in details[2]:
            print("Ksiazka zostala pomyslnie przedluzona na przyszly miesiac! Termin zwrotu: ",next_month())
            details[2] = username+"*"+next_month()

            rewrite_book_list(books_dict, details, isbn)

    except KeyError:
        print("Numer ISBN " + isbn + " nie został znalezniony w bazie danych")