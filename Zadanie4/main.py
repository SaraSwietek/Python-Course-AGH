import librarian_functions as lf
import member_functions as mf
from common_functions import menu, login, browse_books

#plik books.txt zawiera:
#isbn; autor|tytul|x lub username*data (niewypozyczona lub wypozyczona)|0 lub username (rezerwacja)|isbn

#plik members.txt zawiera:
#username; haslo|typ czlonek lub bibliotekarz

#Dla sprobowania mozna uzyc tych kont:
#Czytelnik: mem, password mem
#Bibliotekarz: bib, password bib


if __name__ == '__main__':

    #menu_type to lista [rodzaj uzytkownika, username]
    menu_type = menu({"Zaloguj się": (login, (), {}),
                  "Wyjdz": (exit, (1,), {})})

    # menu bibliotekarza
    if menu_type[0] == "b":

        while True:
            main_menu_librarian = menu({"Przyjmij zwrot książki": (lf.return_book, (), {}),
                                    "Dodaj nową książkę": (lf.add_book, (), {}),
                                    "Usuń książkę z systemu": (lf.remove_book, (), {}),
                                    "Dodaj bibliotekarza/czytelnika": (lf.register, (), {}),
                                    "Przeglądaj katalog": (browse_books, (), {}),
                                    "Wyjdz": (exit, (1,), {})})

    # menu czytelnika
    elif menu_type[0] == "c":

        while True:
            main_menu_member = menu({"Wypożycz książkę": (mf.borrow_book, (menu_type[1],), {}),
                                    "Zarezerwuj aktualnie niedostępną książkę": (mf.reserve_book, (menu_type[1],), {}),
                                    "Przedłuż wypożyczenie": (mf.extend_deadline, (menu_type[1],), {}),
                                    "Przeglądaj katalog": (browse_books, (), {}),
                                    "Wyjdz": (exit, (1,), {})})


