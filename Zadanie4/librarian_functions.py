from common_functions import txt_to_dict, describe_books


def return_book():
    isbn = input("Podaj isbn ksiazki ktora chcesz zwrocic: >> ")
    books_dict = txt_to_dict("books.txt")

    details = books_dict[isbn].split("|")

    if isbn not in books_dict:
        print("Ksiazka o isbn "+isbn+" nie istnieje!")
    else:
        print("Ksiazka zostala pomyslnie zwrocona!")
        details[2] = "x"

        new_details=""

        for i in range(len(details)):
            new_details = new_details+details[i]+"|"

        del books_dict[isbn]
        f = open("books.txt", "w", encoding='UTF-8')
        for book in books_dict:
            f.write(book + "; " + books_dict[book] + "\n")
        f.write(isbn + "; " + new_details[:-1] + "\n")
        f.close()


def register():

    username = input("Podaj login: ")
    password = input("Podaj haslo: ")
    status = input("Czytelnik (c) czy bibliotekarz (b)?: >> ")

    if status == "c" or status == "b":
        pass
    else:
        print("Błąd przy określeniu typu konta! Musisz wybrac (c) lub (b)")


    members_dict = txt_to_dict("members.txt")

    if username in members_dict.keys():
        print("Użytkownik o takim loginie już istnieje!")
    else:
        database = open("members.txt", "a", encoding='UTF-8')
        database.write(username + "; " + password + "|" + status + "\n" )
        print("Użytkownik został utworzony.")
        database.close()


def add_book():
    books_dict = txt_to_dict("books.txt")

    isbn = input("Podaj isbn: >> ")
    author = input("Podaj autora: >> ")
    title = input("Podaj tytul : >> ")

    if isbn in books_dict.keys():
        print("Książka o takim isbn już istnieje!")
    else:
        database = open("books.txt", "a", encoding='UTF-8')
        database.write(isbn + "; " + author + "|" + title + "|x|0|" + isbn + "\n")
        print("Książka została dodana.")
        database.close()


def remove_book():
    try:
        isbn = input("Podaj ISBN książki do usunięcia: >>")

        books_dict = txt_to_dict("books.txt")
        details = books_dict[isbn].split("|")
        describe_books([details])

        decision = (input("Czy jestes pewien, ze chcesz usunac ta ksiazke? (TAK) (NIE)")).lower()

        if decision == "tak":
            del books_dict[isbn]
            f = open("books.txt", "w", encoding='UTF-8')
            for book in books_dict:
                f.write(book + "; " + books_dict[book] + "\n")
            f.close()
            print("Ksiazka zostala pomyslnie usunieta!")

        else:
            print("Ksiazka nie zostala usunieta!")

    except KeyError:
        print("Numer ISBN " + isbn + " nie został znalezniony w bazie danych")
