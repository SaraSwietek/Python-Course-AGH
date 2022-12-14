from datetime import datetime
from dateutil.relativedelta import relativedelta

def menu(options, special_option={})  :  # opcja specjalna opcjonalna
    options = list(options.items())
    while True:
      for ind, option in enumerate(options, start=1):
        print("{}. {}".format(ind, option[0]))
      try:
        choice = int(input(">>"))
        if 0 < choice <= len(options):
          func, args, kwargs = options[choice - 1][1]
          return func(*args, **kwargs)
        else:
          print("---Wybrałeś złą opcję! Spróbuj ponownie.---")
      except ValueError:
        pass  # simply continue the loop


def login():

    username = input("Login: >> ")
    password = input("Password: >> ")
    status = input("Czytelnik (c) czy bibliotekarz (b)?: >> ")

    members_dict = txt_to_dict("members.txt")

    if username in members_dict.keys():
        pass #uzytkownik istnieje

        if members_dict[username][:len(members_dict[username]) - 2] == password:
            pass #haslo OK

            if members_dict[username].replace(password+"|", "") == status:
                # status OK
                print("ZALOGOWANY")
                return status #zwracam status zalogowanego uzytkownika, zeby wyswietlic odpowiednie menu
            elif status == "b":
                print("Podany login i haslo nie maja uprawnien bibliotekarza!")
                return login()
            elif status == "c":
                print("Podany login i haslo nie maja uprawnien czytelnika!")
                return login()
            else:
                print("Błąd przy określeniu typu konta! Wybierz (c) lub (b)")
                return login()
        else:
            print("Złe hasło! Spróbuj ponownie.")
            return login()
    else:
        print("Użytkownik nie istnieje! Spróbuj ponownie.")
        return login()



def txt_to_dict(file):
    data = open(file, "r", encoding='UTF-8')
    key_list = []
    value_list = []

    for i in data:
        a, b = i.split(";")
        b = b.strip()
        key_list.append(a)
        value_list.append(b)

    data.close()

    return dict(zip(key_list, value_list))


def register():

    username = input("Podaj login: ")
    password = input("Podaj haslo: ")
    status = input("Czytelnik (c) czy bibliotekarz (b)?: >> ")

    if status== "c" or status == "b":
        pass
    else:
        print("Błąd przy określeniu typu konta! Wybierz (c) lub (b)")
        register()


    members_dict = txt_to_dict("members.txt")

    if username in members_dict.keys():
        print("Użytkownik o takim loginie już istnieje!")
        register()
    else:
        database = open("members.txt", "a", encoding='UTF-8')
        database.write(username + "; " + password + "|" + status + "\n" )
        print("Użytkownik został utworzony.")
        database.close()

def return_book():
    username = input("Podaj nazwe uzytkownika, ktory chce zwrocic ksiazke: >> ")
    isbn = input("Podaj isbn ksiazki ktora chcesz zwrocic: >> ")
    books_dict = txt_to_dict("books.txt")

    details = books_dict[isbn].split("|")

    if isbn not in books_dict:
        print("Ksiazka o isbn "+isbn+" nie istnieje! Sprobuj ponownie!")
        return_book()
    elif username not in details[2]:
        print("Podana ksiazka nie jest przypisana do uzytkownika "+username+". Sprobuj ponownie!")
        return_book()
    elif username in details[2]:
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


def add_book():
    books_dict = txt_to_dict("books.txt")

    isbn = input("Podaj isbn: >> ")
    author = input("Podaj autora: >> ")
    title = input("Podaj tytul : >> ")

    if isbn in books_dict.keys():
        print("Książka o takim isbn już istnieje!")
        add_book()
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

    except KeyError:
        print("Numer ISBN " + isbn + " nie został znalezniony w bazie danych")
        remove_book()



def browse_books(): #(wyszukiwanie po tytule, autorze lub słowach kluczowych)
    books_dict = txt_to_dict("books.txt")

    menu_browser = menu({"Szukaj po isbn": (search_isbn, (), {}),
                                "Szukaj po tytule": (search_title, (), {}),
                                "Szukaj po autorze": (search_author, (), {}),
                                "Wyswietl wszystkie ksiazki": (list_books, (), {}),
                                "Wyjdz": (exit, (1,), {})})


def search_isbn():

    books_dict = txt_to_dict("books.txt")

    try:
        isbn = input("Wpisz szukany ISBN: >>")
        book_details = books_dict[isbn].split("|")
        describe_books([book_details])
    except KeyError:
        print("Numer ISBN " + isbn + " nie został znalezniony w bazie danych")
    finally:
        browse_books()

def search_title():
    books_dict = txt_to_dict("books.txt")
    title = input("Wpisz szukany tytuł/słowa kluczowe: >>")
    found_titles = []

    #po calym tytule

    for i in books_dict.values():
        details = i.split("|")

        if title in details[1] or title in details[1].lower():
            if details not in found_titles:
                found_titles.append(details)

    #po slowach kluczowych

    keywords = title.split()

    for i in books_dict.values():
        details = i.split("|")

        for word in keywords:
            if word in details[1] or word in details[1].lower():
                if details not in found_titles:
                    found_titles.append(details)

    describe_books(found_titles)

#list_of_details musi byc lista zagniezdzona, zeby dziala zarowno
#dla pojedynczych tytulow jak i kilku
def describe_books(list_of_details):

    for details in list_of_details:

        print("ISBN: " + details[4])
        print("Autor: " + details[0])
        print("Tytul: " + details[1])

        if details[2] == "x":
            print("Ksiazka dostepna w bibliotece")
        else:
            borrowed = details[2].split("*")
            print("Ksiazka wypozyczona do dnia: ",borrowed[1], " przez: ",borrowed[0])

        if details[3] == "0":
            pass
        else:
            print("Ksiazka zarezerwowana.")

        print("\n")

def search_author():
    books_dict = txt_to_dict("books.txt")
    author = input("Wpisz szukanego autora: >>")
    found_authors = []

    # po calym tytule

    for i in books_dict.values():
        details = i.split("|")

        if author in details[0] or author in details[0].lower():
            if details not in found_authors:
                found_authors.append(details)

    describe_books(found_authors)

def list_books():
    books_dict = txt_to_dict("books.txt")
    books_list = []

    for i in books_dict.values():
        details = i.split("|")
        books_list.append(details)

    describe_books(books_list)

def borrow_book():
    username = input("Podaj swoja nazwe uzytkownika: >> ")
    isbn = input("Podaj isbn ksiazki ktora chcesz pozyczyc: >> ")
    books_dict = txt_to_dict("books.txt")

    details = books_dict[isbn].split("|")

    if isbn not in books_dict:
        print("Ksiazka o isbn " + isbn + " nie istnieje! Sprobuj ponownie!")
        borrow_book()
    elif details[2]!="x":
        print("Podana ksiazka jest wypozyczona uzytkownikowi " + username + ". Sprobuj ponownie!")
        borrow_book()
    elif details[2]=="x":
        print("Ksiazka zostala pomyslnie wypozyczona na miesiac! Data zwrotu: ",next_month())
        details[2] = username + "*" + next_month()

        new_details = ""

        for i in range(len(details)):
            new_details = new_details + details[i] + "|"

        del books_dict[isbn]
        f = open("books.txt", "w", encoding='UTF-8')
        for book in books_dict:
            f.write(book + "; " + books_dict[book] + "\n")
        f.write(isbn + "; " + new_details[:-1] + "\n")
        f.close()

def reserve_book():
    username = input("Podaj swoja nazwe uzytkownika: >> ")
    isbn = input("Podaj isbn ksiazki ktora chcesz zarezerwowac: >> ")
    books_dict = txt_to_dict("books.txt")

    details = books_dict[isbn].split("|")

    if isbn not in books_dict:
        print("Ksiazka o isbn " + isbn + " nie istnieje! Sprobuj ponownie!")
        reserve_book()
    elif details[3]!="0":
        print("Podana ksiazka jest zarezerwowana przez uzytkownika " + details[3] + ". Sprobuj zarezerwowac inna ksiazke!")
        reserve_book()
    elif details[3]=="0":
        print("Ksiazka zostala pomyslnie zarezerwowana!")
        details[3] = username

        new_details = ""

        for i in range(len(details)):
            new_details = new_details + details[i] + "|"

        del books_dict[isbn]
        f = open("books.txt", "w", encoding='UTF-8')
        for book in books_dict:
            f.write(book + "; " + books_dict[book] + "\n")
        f.write(isbn + "; " + new_details[:-1] + "\n")
        f.close()

def extend_deadline():
    username = input("Podaj swoja nazwe uzytkownika: >> ")
    isbn = input("Podaj isbn ksiazki ktora chcesz przedluzyc: >> ")
    books_dict = txt_to_dict("books.txt")

    details = books_dict[isbn].split("|")

    if isbn not in books_dict:
        print("Ksiazka o isbn " + isbn + " nie istnieje! Sprobuj ponownie!")
        extend_deadline()
    elif username not in details[2]:
        print("Podana ksiazka nie jest zarezerwowana przez uzytkownika " + details[3] + ". Sprobuj ponownie!")
        extend_deadline()
    elif username in details[2]:
        print("Ksiazka zostala pomyslnie przedluzona na przyszly miesiac! Termin zwrotu: ",next_month())
        details[2] = username+"*"+next_month()

        new_details = ""

        for i in range(len(details)):
            new_details = new_details + details[i] + "|"

        del books_dict[isbn]
        f = open("books.txt", "w", encoding='UTF-8')
        for book in books_dict:
            f.write(book + "; " + books_dict[book] + "\n")
        f.write(isbn + "; " + new_details[:-1] + "\n")
        f.close()

def next_month():
    date_after_month = datetime.today() + relativedelta(months=1)
    return date_after_month.strftime('%d.%m.%Y')

if __name__ == '__main__':

    menu_type = menu({"Zaloguj się": (login, (), {}),
                  "Wyjdz": (exit, (1,), {})})


    if menu_type == "b": #menu bibliotekarza

        while(True):
            main_menu_librarian = menu({"Przyjmij zwrot książki": (return_book, (), {}),
                                    "Dodaj nową książkę": (add_book, (), {}),
                                    "Usuń książkę z systemu": (remove_book, (), {}),
                                    "Dodaj bibliotekarza/czytelnika": (register, (), {}),
                                    "Przeglądaj katalog": (browse_books, (), {}),
                                    "Wyjdz": (exit, (1,), {})})

    elif menu_type == "c": #menu czytelnika

        while(True):
            main_menu_member = menu({"Wypożycz książkę": (borrow_book, (), {}),
                                    "Zarezerwuj aktualnie niedostępną książkę": (reserve_book, (), {}),
                                    "Przedłuż wypożyczenie": (extend_deadline, (), {}),
                                    "Przeglądaj katalog": (browse_books, (), {}),
                                    "Wyjdz": (exit, (1,), {})})
    else:
        print("COS ZLE")


