#-*- coding: utf-8 -*-
import gi
# biblioteka do losowania liczb
import random
# wymagamy biblioteki w wersji min 3.0
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


class Plansza(Gtk.Grid):
    """ Klasa przedstawiajaca plansze."""
    def __init__(self):
        """Inicjalizator obiektu, dziedziczenie po klasie Gtk.Grid."""
        Gtk.Grid.__init__(self)
        # n - stala w programie, odpowiadajaca za wielkosc planszy
        # ilosc_min - zawiera informacje o ilosci min na planszy
        # ilosc_przyciskow - zawiera informacje o ilosci przyciskow na planszy, potrzebne do kontrolowania wygranej
        # plansza - lista zawierajaca informacje o pozycjach min oraz liczbe min siasiadujacych z konkretnymi polami
        self.n = 5
        self.ilosc_min = 0
        self.ilosc_przyciskow = self.n * self.n
        self.plansza = list()
        self.buttons = []
        # generacja siatki
        for i in range(self.n):
            # dodanie pustej listy do listy buttons oraz planszy
            self.plansza.append([])
            self.buttons.append([])
            for j in range(self.n):
                # ustawienie poczatkowych wartosci dla planszy
                self.plansza[i].append(0)
                # button - tworzenie nowego przycisku z napisem
                button = Gtk.Button.new_with_label("")
                # dodanie utworzonego przycisku do listy przyciskow
                self.buttons[i].append(button)
                # dodanie przycisku do siatki
                self.attach(button, i, j, 1, 1)

        # ustawienie identycznych rozmiarow kolumn oraz wierszy dla siatki
        self.set_column_homogeneous(True)
        self.set_row_homogeneous(True)


class App(object):
    """ Klasa przedstawiajaca gre oraz mechanike Sapera."""

    def __init__(self):
        """ Inizjalizator obiektu."""
        # tytul okna, domyslny rozmiar okna oraz wysrodkowanie okna
        self.window = Gtk.Window(title="Saper")
        self.window.set_default_size(250, 250)
        self.window.set_position(1)
        # grid - obiekt zawierajacy wygenerowana plansze z klasy Plansza
        self.grid = Plansza()
        # podpiecie przyciskow pod zdarzenie clicked
        for i in range(self.grid.n):
            for j in range(self.grid.n):
                self.grid.buttons[i][j].connect("clicked", self.kliknieto, i, j)
        # wylosowanie n min w losowych miejscach i dodanie informacji do planszy
        while self.grid.ilosc_min < self.grid.n:
            # wylosujx - zawiera numer kolumny
            # wylosujy - zawiera numer wiersza
            wylosujx = random.randint(0, self.grid.n - 1)
            wylosujy = random.randint(0, self.grid.n - 1)
            # zapewnienie, ze pozycje min beda unikalne
            if self.grid.plansza[wylosujx][wylosujy] == 0:
                self.grid.ilosc_min += 1
                self.grid.plansza[wylosujx][wylosujy] = "M"
        # uzupelnienie planszy o ilosc posiadanych min dookola siebie dla kazdego przycisku
        for i in range(self.grid.n):
            for j in range(self.grid.n):
                # siasiedzi - lista zawierajaca pozycje sasiadow dla kazdego przycisku
                sasiedzi = list()
                # rozpatruje tylko te przyciski ktore posiadaja mine, uzupelniam plansze dla wszystkich przyciskow
                # w obrebie danej miny zwiekszajac ilosc min o jeden
                if self.grid.plansza[i][j] == "M":
                    # wywoluje funkcje zwracajaca liste pozycji sisiadow dla kazdej z min
                    # podajac plansze, wspolrzedne aktualnie rozpatrywanego pola
                    # oraz promien wokol ktorego szukam sasiadow
                    sasiedzi = self.znajdz_sasiadow(self.grid.plansza, j, i, 1)
                # dla kazdej pozycji roznej od miny dodaje informacje o tym, ze dane pole ma mine kolo siebie
                # zwiekszajac wartosc pola o jeden
                for para in sasiedzi:
                    if self.grid.plansza[para[1]][para[0]] == "M":
                        continue
                    self.grid.plansza[para[1]][para[0]] += 1
        # przycisk pozwalajacy zaczac gre od nowa
        od_nowa = Gtk.Button(label="Nowa gra")
        # podpiecie przycisku pod zdarzenie clicked
        od_nowa.connect("clicked", self.nowa_gra)
        # glowny - box zawierajacy plansze oraz przycisk
        self.glowny = Gtk.VBox()
        # dodanie planszy oraz przycisku do boxa
        self.glowny.pack_start(self.grid, True, True, 0)
        self.glowny.pack_end(od_nowa, False, False, 0)

        # podpiecie zdarzenia wylaczenia okna przyciskiem X
        self.window.connect("delete-event", lambda x, y: Gtk.main_quit())
        # dodanie glownego boxa do okna
        self.window.add(self.glowny)
        # wyswietlenie wszystkiego na oknie
        self.window.show_all()

    def odslon(self):
        """ Metoda odslaniajaca wszystkie pola w przypadku wygranej lub przegranej."""
        for i in range(self.grid.n):
            for j in range(self.grid.n):
                # wywolanie funkcji odslaniajacej przyciski
                self.podmien(i, j)

    def podmien(self, i, j):
        """ Metoda odslaniajaca przycisk wraz z nadaniem odpowiedniej labelki.

        i - numer kolumny w ktorej znajduje sie przycisk
        j - numer wiersza w ktorym znajduje sie przycisk
        """
        # Tutaj odbywa sie ustawienie odpowiedniej labelki w zaleznosci od tego, jaka informacje przechowuje
        # lista plansza oraz ustawienie przycisku na nieaktywny
        if self.grid.plansza[i][j] == "M":
            self.grid.buttons[i][j].get_child().set_markup('<span foreground="red"><b>M</b></span>')
            self.grid.buttons[i][j].set_sensitive(False)

        if self.grid.plansza[i][j] == 0:
            self.grid.buttons[i][j].get_child().set_markup('<span foreground="black"><b>0</b></span>')
            self.grid.buttons[i][j].set_sensitive(False)

        if self.grid.plansza[i][j] == 1:
            self.grid.buttons[i][j].get_child().set_markup('<span foreground="orange"><b>1</b></span>')
            self.grid.buttons[i][j].set_sensitive(False)

        if self.grid.plansza[i][j] == 2:
            self.grid.buttons[i][j].get_child().set_markup('<span foreground="orangered"><b>2</b></span>')
            self.grid.buttons[i][j].set_sensitive(False)

        if self.grid.plansza[i][j] == 3:
            self.grid.buttons[i][j].get_child().set_markup('<span foreground="tomato"><b>3</b></span>')
            self.grid.buttons[i][j].set_sensitive(False)

        if self.grid.plansza[i][j] > 3:
            self.grid.buttons[i][j].get_child().set_markup('<span foreground="brown"><b>{}</b></span>'
                                                           .format(self.grid.plansza[i][j]))
            self.grid.buttons[i][j].set_sensitive(False)

    def kliknieto(self, button, i, j):
        """ Metoda reagujaca na zdarzenia nacisniecia przycisku.

        button - nacisniety przycisk
        i - numer kolumny w ktorej znajduje sie przycisk
        j - numer wiersza w ktorym znajduje sie przycisk
        """
        # uaktualnienie ilosci mozliwych do nacisniecia przyciskow
        self.grid.ilosc_przyciskow -= 1
        # jezeli uzytkownik trafil na Mine, to odslaniam plansze
        if self.grid.plansza[i][j] == "M":
            self.odslon()
            return
        # jezeli uzytkownik nacisnal przycisk rozny od miny i byl to "ostatni" mozliwy przycisk nie zawierajacy miny
        # to odslaniam reszte planszy oraz wyswietlam odpowiedni komunikat o wygranej
        if self.grid.ilosc_przyciskow == self.grid.ilosc_min:
            self.odslon()
            # utworzenie komunikatu
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "WYGRANA")
            # uruchomienie komunikatu
            dialog.run()
            # usuniecie komunikatu
            dialog.destroy()
            return
        # jezeli zadna z powyzszych sytuacji nie zaszla, gra trwa dalej i odslaniam tylko nacisniety przycisk
        self.podmien(i, j)

    def znajdz_sasiadow(self, plansza, i, j, dystans):
        """ Metoda znajdujaca sasiadow w promieniu 1.

        plansza - plansza rozgrywki
        i - wspolrzedna "x" rozpatrywanego pola(numer wiersza)
        j - wspolrzedna "y" rozpatrywanego pola(numer kolumny)
        dystans - odleglosc w ktorej szukamy siasiadow
        Zwraca liste pozycji siasiadow. Rozwiazanie oparte o algorytm znajdowania sasiadow ze stackoverflow.
        """
        # sasiedzi - lista zawierajaca pozycje wszystkich siasiadow z wlasnie rozpatrywanym polem
        sasiedzi = []
        # zasieg_wiersza - lista przechowujaca informacje o tym, jakie numery wierszy sa brane pod uwage w przypadku
        # wyszukiwania sasiadow dla danego pola
        # zasieg_kolumn - lista przechowujaca informacje o tym, jakie numery kolumn sa brane pod uwage w przypadku
        # wyszukiwania sasiadow dla danego pola
        zasieg_wiersza = range(max(0, i - dystans), min(len(plansza), i + dystans + 1))
        zasieg_kolumny = range(max(0, j - dystans), min(len(plansza[0]), j + dystans + 1))
        # dla kazdego wiersza wraz z kolumnami
        for wiersz in zasieg_wiersza:
            for kolumna in zasieg_kolumny:
                # rozpatrywanie przypadkow takich, ktore maja rozne pozycje od wlasnie rozpatrywanego pola(i,j)
                # aby uniknac sytuacji wlozenia pozycji pola ktore jest wlasnie rozpatrywane(sasiad dla samego siebie)
                if (wiersz != i) or (kolumna != j):
                    sasiedzi.append((wiersz, kolumna))
        return sasiedzi

    def nowa_gra(self, button):
        """ Metoda pozwalajaca rozpoczac rozgrywke od nowa.

        button - nacisniety przycisk
        """
        # ustawienie poczatkowych wartosci tak jak w przypadku klasy Plansza
        self.grid.ilosc_min = 0
        self.grid.ilosc_przyciskow = self.grid.n * self.grid.n
        self.grid.plansza = list()
        # zerowanie ustawien planszy, przyciskow oraz ich napisow
        for i in range(self.grid.n):
            self.grid.plansza.append([])
            for j in range(self.grid.n):
                self.grid.plansza[i].append(0)
                self.grid.buttons[i][j].get_child().set_markup("")
                self.grid.buttons[i][j].set_sensitive(True)
        # losowanie pozycji min na nowo
        while self.grid.ilosc_min < self.grid.n:
            # wylosujx - zawiera numer kolumny
            # wylosujy - zawiera numer wiersza
            wylosujx = random.randint(0, self.grid.n - 1)
            wylosujy = random.randint(0, self.grid.n - 1)
            # zapewnienie unikalnosci pozycji min
            if self.grid.plansza[wylosujx][wylosujy] == 0:
                self.grid.ilosc_min += 1
                self.grid.plansza[wylosujx][wylosujy] = "M"
        # uzupelnienie planszy na nowo o ilosc posiadanych min dookola siebie dla kazdego pola
        for i in range(self.grid.n):
            for j in range(self.grid.n):
                # siasiedzi - lista zawierajaca pozycje sasiadow dla kazdego przycisku
                sasiedzi = list()
                # rozpatruje tylko te przyciski ktore posiadaja mine, uzupelniam plansze dla wszystkich przyciskow
                # w obrebie danej miny zwiekszajac ilosc min o jeden
                if self.grid.plansza[i][j] == "M":
                    # wywoluje funkcje zwracajaca liste pozycji sasiadow dla kazdej z min
                    # podajac plansze, wspolrzedne aktualnie rozpatrywanego pola
                    # oraz promien wokol ktorego szukam sasiadow
                    sasiedzi = self.znajdz_sasiadow(self.grid.plansza, j, i, 1)
                # dla kazdej pozycji roznej od miny dodaje informacje o tym, ze dane pole ma mine kolo siebie
                # zwiekszajac wartosc pola o jeden
                for para in sasiedzi:
                    if self.grid.plansza[para[1]][para[0]] == "M":
                        continue
                    self.grid.plansza[para[1]][para[0]] += 1


if __name__ == "__main__":
    app = App()

    Gtk.main()
