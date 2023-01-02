from datetime import datetime
from dateutil.relativedelta import relativedelta


def menu(options, special_option={}):  # opcja specjalna opcjonalna
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


def describe_books(list_of_details):
    for details in list_of_details:

        print("ISBN: " + details[4])
        print("Autor: " + details[0])
        print("Tytul: " + details[1])

        if details[2] == "x":
            print("Ksiazka dostepna w bibliotece")
        else:
            borrowed = details[2].split("*")
            print("Ksiazka wypozyczona do dnia: ", borrowed[1], " przez: ", borrowed[0])

        if details[3] == "0":
            pass
        else:
            print("Ksiazka zarezerwowana.")

        print("\n")


def next_month():
    date_after_month = datetime.today() + relativedelta(months=1)
    return date_after_month.strftime('%d.%m.%Y')


def login():  # funkcja łączy dialog z użytkownikiem z logiką biznesową
    username = input("Login: >> ")
    password = input("Password: >> ")
    status = input("Czytelnik (c) czy bibliotekarz (b)?: >> ")  # czemu to nie jest menu?

    members_dict = txt_to_dict("members.txt")

    if username in members_dict.keys():
        pass  # uzytkownik istnieje

        if members_dict[username][:len(members_dict[username]) - 2] == password:
            pass  # haslo OK

            if members_dict[username].replace(password + "|", "") == status:
                # status OK
                print("ZALOGOWANY")
                return [status, username]  # zwracam status zalogowanego uzytkownika, zeby wyswietlic odpowiednie menu
            elif status == "b":
                print("Podany login i haslo nie maja uprawnien bibliotekarza!")
                return login()
            elif status == "c":
                print("Podany login i haslo nie maja uprawnien czytelnika!")
                return login()
            else:
                print("Błąd przy określeniu typu konta! Musisz wybrac (c) lub (b)")
                return login()
        else:
            print("Złe hasło!")
            return login()
    else:
        print("Użytkownik nie istnieje!")
        return login()


def browse_books():  # (wyszukiwanie po tytule, autorze lub słowach kluczowych)
    books_dict = txt_to_dict("books.txt")

    menu_browser = menu({"Szukaj po isbn": (search_isbn, (), {}),
                         "Szukaj po tytule/slowach kluczowych": (search_title, (), {}),
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


def search_title():
    books_dict = txt_to_dict("books.txt")
    title = input("Wpisz szukany tytuł/słowa kluczowe: >>")
    found_titles = []

    # po calym tytule

    for i in books_dict.values():
        details = i.split("|")

        if title in details[1] or title in details[1].lower():
            if details not in found_titles:
                found_titles.append(details)

    # po slowach kluczowych

    keywords = title.split()

    for i in books_dict.values():
        details = i.split("|")

        for word in keywords:
            if word in details[1] or word in details[1].lower():
                if details not in found_titles:
                    found_titles.append(details)

    describe_books(found_titles)

    if len(found_titles) == 0:
        print("Nie znaleziono ksiazki zawierajacej podane slowa kluczowe!")


def search_author():
    books_dict = txt_to_dict("books.txt")
    author = input("Wpisz szukanego autora: >>")
    found_authors = []

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
