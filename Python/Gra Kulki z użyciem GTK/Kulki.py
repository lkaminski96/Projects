#-*- coding: utf-8 -*-
import gi
# biblioteka do losowania liczb
import random
# wymagamy biblioteki w wersji min 3.0
gi.require_version('Gtk', '3.0')
# metody do korzystania z Gtk oraz GdkPixbuf(pomoc w czytaniu obrazka)
from gi.repository import Gtk
from gi.repository import GdkPixbuf


class Kulki():
    """ Klasa przedstawiajaca obiekt Kulki."""
    def __init__(self):
        """ Inicjalizator obiektu."""
        # zmienne kolejno sluzace do:
        # wynik - zawiera aktualny wynik rozgrywki
        # naciesniecia - zawiera ilosc nacisnietych przez uzytkownika przyciskow
        # szerokosc - zawiera szerokosc okna
        # wysokosc - zawiera wysokosc okna
        # tabela_wynikow - lista zawierajaca 5 ostatnich najlepszych wynikow gracza, na poczatku zerowana
        self.wynik = 0
        self.nacisniecia = 0
        self.szerokosc = 550
        self.wysokosc = 550
        self.tabela_wynikow = []
        # tytul oknca
        self.window = Gtk.Window(title="Kulki")
        # ustalanie domyslnego rozmiaru okna
        self.window.set_default_size(self.szerokosc, self.wysokosc)
        # tablica_kulek - zawiera liste kulek do generowania
        self.tablica_kulek = ["kulka1.svg", "kulka2.svg", "kulka3.svg", "kulka4.svg", "kulka5.svg"]
        # plansza - zawiera informacje o tym czy w danym miejscu znajduje sie juz jakas kulka
        self.plansza = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        # kolor - lista zawierajaca kolory kulek
        self.kolor = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]
        # tworzenie siatki
        # grid - zmienna przechowywujaca siatke do przyciskow
        grid = Gtk.Grid()
        # utowrzenie pustej listy buttons, ktora przechowywac bedzie liste buttonow
        self.buttons = []
        # generacja siatki
        for i in range(10):
            # dodanie pustej listy do listy buttons
            self.buttons.append([])
            for j in range(10):
                # button - tworzenie nowego ToggleButtona
                button = Gtk.ToggleButton()
                # ustalanie domyslnego rozmiaru buttona
                Gtk.Widget.set_size_request(button, 40, 40)
                # dodanie utworzonego buttona do listy buttonow
                self.buttons[i].append(button)
                # dodanie buttona do siatki
                grid.attach(button, i, j, 1, 1)
                # podpiecie buttona do zdarzenia w przypadku jego nacisniecia
                button.connect("pressed", self.wlaczono, i, j)
        # kolumny maja miec identyczna szerokosc, wiersze identyczna wysokosc
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)

        # wolne - lista zawierajaca informacje o wolnych miejscach
        wolne = []
        # dodanie wolnych miejsc do listy
        for i in range(10):
            for j in range(10):
                    wolne.append((i, j))
        # generowanie 50 kulek w losowych miejscach
        for i in range(50):
            # loskul - zawiera liczbe od 0 - 4 odpowiadajaca za kolor kulki
            # wylosuj - zawiera informacje o wylosowanym wolnym miejscu w liscie
            # kulka - zawiera zaladowany obrazek z ustawionym scalowaniem z wczesniej wylosowanym kolorem kulki
            loskul = random.randint(0, 4)
            kulka = Gtk.Image.new_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file_at_scale(self.tablica_kulek[loskul], 35, 35, True))
            wylosuj = random.randint(0, len(wolne) - 1)
            # x - zawiera polozenie kulki w pionie
            # y - zawiera polozenie kulki w poziomie
            x = wolne[wylosuj][0]
            y = wolne[wylosuj][1]
            # ustawienie obrazka na przycisku
            self.buttons[x][y].set_image(kulka)
            # ustawienie pola wolnego na planszy na zajete
            self.plansza[x][y] = 1
            # zapamietanie wylosowanego koloru
            self.kolor[x][y] = loskul
            # usuniecie wolnego miejsca z listy
            del wolne[wylosuj]
        # od_nowa - przycisk zawierajacy informacje o tym czy rozpoczac gre od nowa
        od_nowa = Gtk.Button(label="Graj od początku")
        # podpiecie buttona pod zdarzenie clicked
        od_nowa.connect("clicked", self.generuj_od_nowa)
        # biezace - zawiera label z biezaca iloscia zdobytych punktow przez uzytkownika
        self.biezace = Gtk.Label()
        # ustawienie tekstu dla labela i wyrownanie
        self.biezace.set_label("Liczba punktow:<b> {} </b>".format(self.wynik))
        self.biezace.set_use_markup(True)
        self.biezace.set_xalign(0)
        # tworzenie boxow
        # glowny - box pionowy glowny zawierajacy pozostale boxy przesylany do okna
        # srodek - box poziomy zawierajacy ranking oraz siatke z przyciskami
        # rankingbox - box pionowy zawierajacy ranking z wynikami
        self.glowny = Gtk.VBox()
        self.srodek = Gtk.HBox()
        self.rankingbox = Gtk.VBox()
        # ranking - zawiera label z napisem Ranking
        ranking = Gtk.Label()
        ranking.set_label("<b> Ranking: </b>")
        ranking.set_use_markup(True)
        # dodanie labela ranking do boxa rankingbox
        self.rankingbox.pack_start(ranking, False, False, 0)
        # tworzenie labelow do wyswietlenia zdobytych punktow
        self.wynik0 = Gtk.Label()
        self.wynik1 = Gtk.Label()
        self.wynik2 = Gtk.Label()
        self.wynik3 = Gtk.Label()
        self.wynik4 = Gtk.Label()
        # dodawanie labelow do boxa rankingowego
        self.rankingbox.pack_start(self.wynik0, False, False, 1)
        self.rankingbox.pack_start(self.wynik1, False, False, 1)
        self.rankingbox.pack_start(self.wynik2, False, False, 1)
        self.rankingbox.pack_start(self.wynik3, False, False, 1)
        self.rankingbox.pack_start(self.wynik4, False, False, 1)
        # dodanie rankingboxu i siatki do srodkowego boxa
        self.srodek.pack_start(self.rankingbox, False, False, 2)
        self.srodek.pack_start(grid, False, False, 0)
        # dodanie labela z biezacymi punkatmi, boxa sordkowego oraz przycisku od nowej gry
        # do boxa glownego
        self.glowny.pack_start(self.biezace, False, False, 0)
        self.glowny.pack_start(self.srodek, False, False, 0)
        self.glowny.pack_start(od_nowa, False, False, 0)
        # podpiecie zdarzenia wylaczenia okna przyciskiem X
        self.window.connect("delete-event", lambda x, y: Gtk.main_quit())
        # dodanie boxa glownego do okna
        self.window.add(self.glowny)
        # wyswietlenie wszystkiego na oknie
        self.window.show_all()

    def ranking(self):
        """ Metoda wyswietlajaca ranking gracza, max 5 wynikow."""
        # sortowanie tablice rosnaco
        self.tabela_wynikow.sort()
        # odwrocenie talibcy, aby miec kolejnosc malejaca
        self.tabela_wynikow.reverse()

        if len(self.tabela_wynikow) == 6:
            # usniecie ostatniego elementu z listy
            del self.tabela_wynikow[5]
            # wyswietlenie 5 obecnie najlepszych wynikow ze zdobytymi punktami
            self.wynik0.set_label("<b> 1. </b>{}".format(self.tabela_wynikow[0]))
            self.wynik0.set_use_markup(True)
            self.wynik1.set_label("<b> 2. </b>{}".format(self.tabela_wynikow[1]))
            self.wynik1.set_use_markup(True)
            self.wynik2.set_label("<b> 3. </b>{}".format(self.tabela_wynikow[2]))
            self.wynik2.set_use_markup(True)
            self.wynik3.set_label("<b> 4. </b>{}".format(self.tabela_wynikow[3]))
            self.wynik3.set_use_markup(True)
            self.wynik4.set_label("<b> 5. </b>{}".format(self.tabela_wynikow[4]))
            self.wynik4.set_use_markup(True)

        if len(self.tabela_wynikow) == 1:
            #wyswietlenie jednego wyniku
            self.wynik0.set_label("<b> 1. </b>{}".format(self.tabela_wynikow[0]))
            self.wynik0.set_use_markup(True)

        elif len(self.tabela_wynikow) == 2:
            #wyswietlenie dwoch wynikow
            self.wynik0.set_label("<b> 1. </b>{}".format(self.tabela_wynikow[0]))
            self.wynik0.set_use_markup(True)
            self.wynik1.set_label("<b> 2. </b>{}".format(self.tabela_wynikow[1]))
            self.wynik1.set_use_markup(True)

        if len(self.tabela_wynikow) == 3:
            #wyswietlenie trzech wynikow
            self.wynik0.set_label("<b> 1. </b>{}".format(self.tabela_wynikow[0]))
            self.wynik0.set_use_markup(True)
            self.wynik1.set_label("<b> 2. </b>{}".format(self.tabela_wynikow[1]))
            self.wynik1.set_use_markup(True)
            self.wynik2.set_label("<b> 3. </b>{}".format(self.tabela_wynikow[2]))
            self.wynik2.set_use_markup(True)

        if len(self.tabela_wynikow) == 4:
            #wyswietlenie czterech wynikow
            self.wynik0.set_label("<b> 1. </b>{}".format(self.tabela_wynikow[0]))
            self.wynik0.set_use_markup(True)
            self.wynik1.set_label("<b> 2. </b>{}".format(self.tabela_wynikow[1]))
            self.wynik1.set_use_markup(True)
            self.wynik2.set_label("<b> 3. </b>{}".format(self.tabela_wynikow[2]))
            self.wynik2.set_use_markup(True)
            self.wynik3.set_label("<b> 4. </b>{}".format(self.tabela_wynikow[3]))
            self.wynik3.set_use_markup(True)

        if len(self.tabela_wynikow) == 5:
            #wyswietlenie pieciu wynikow
            self.wynik0.set_label("<b> 1. </b>{}".format(self.tabela_wynikow[0]))
            self.wynik0.set_use_markup(True)
            self.wynik1.set_label("<b> 2. </b>{}".format(self.tabela_wynikow[1]))
            self.wynik1.set_use_markup(True)
            self.wynik2.set_label("<b> 3. </b>{}".format(self.tabela_wynikow[2]))
            self.wynik2.set_use_markup(True)
            self.wynik3.set_label("<b> 4. </b>{}".format(self.tabela_wynikow[3]))
            self.wynik3.set_use_markup(True)
            self.wynik4.set_label("<b> 5. </b>{}".format(self.tabela_wynikow[4]))
            self.wynik4.set_use_markup(True)

    def generuj_od_nowa(self, button):
        """ Metoda generujaca plansze od nowa przy dzialaniu buttona.

        Przyjmuje nacisniety przycisk.
        button - obiekt typu ToggleButton
        """
        # tabela_wynikow - lista przechowywujaca ilosc zdobytych punktow podczas pojedynczych gier max 5
        self.tabela_wynikow.append(self.wynik)
        # uaktualnienie rankingu
        self.ranking()
        #czyszczenie planszy z obrazkow
        for i in range(10):
            for j in range(10):
                # sprawdzenie czy w danym miejscu na planszy znajduje sie kulka
                if self.plansza[i][j] == 1:
                    #czysc - przechowuje obrazek
                    czysc = self.buttons[i][j].get_image()
                    # czyszczene obrazka
                    czysc.clear()
        # zerowanie planszy
        self.plansza = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        # zerowanie kolorow kulek
        self.kolor = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]
        # zerowanie wyniku
        self.wynik = 0
        # ustawienie aktualnego wyniku na labelu biezace
        self.biezace.set_label("Liczba punktow:<b> {} </b>".format(self.wynik))
        self.biezace.set_use_markup(True)
        # wolne - przechowuje informacje o wolnych miejscach na planszy
        wolne = []
        # dodawanie wolnych miejsc do listy
        for i in range(10):
            for j in range(10):
                # sprawdzenie czy w danym miejscu jest wolne miejsce
                if self.plansza[i][j] == 0:
                    # dodanie wolnego miejsca do listy
                    wolne.append((i, j))
        # generowanie 50 kulek w losowych miejscach
        for i in range(50):
            # loskul - zawiera liczbe od 0 - 4 odpowiadajaca za kolor kulki
            # wylosuj - zawiera informacje o wylosowanym wolnym miejscu w liscie
            # kulka - zawiera zaladowany obrazek z ustawionym scalowaniem z wczesniej wylosowanym kolorem kulki
            loskul = random.randint(0, 4)
            kulka = Gtk.Image.new_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file_at_scale(self.tablica_kulek[loskul], 35, 35, True))
            wylosuj = random.randint(0, len(wolne) - 1)
            # x - zawiera polozenie kulki w pionie
            # y - zawiera polozenie kulki w poziomie
            x = wolne[wylosuj][0]
            y = wolne[wylosuj][1]
            # ustawienie obrazka na przycisku
            self.buttons[x][y].set_image(kulka)
            # ustawienie pola wolnego na planszy na zajete
            self.plansza[x][y] = 1
            # zapamietanie koloru kulki
            self.kolor[x][y] = loskul
            # usuniecie wolnego miejsca z listy
            del wolne[wylosuj]

    def sprawdz(self):
        """ Metoda sprawdzajaca wystapienia 5 kulek w dowolnej lini."""
        for i in range(6):
            for j in range(10):
                for kol in range(5):
                    if((self.kolor[i][j] == kol) & (self.kolor[i + 1][j] == kol) & (self.kolor[i + 2][j] == kol) &
                       (self.kolor[i + 3][j] == kol) & (self.kolor[i + 4][j] == kol)):
                        obraz = self.buttons[i][j].get_image()
                        obraz.clear()
                        self.plansza[i][j] = 0
                        self.kolor[i][j] = -1

                        obraz = self.buttons[i + 1][j].get_image()
                        obraz.clear()
                        self.plansza[i + 1][j] = 0
                        self.kolor[i + 1][j] = -1

                        obraz = self.buttons[i + 2][j].get_image()
                        obraz.clear()
                        self.plansza[i + 2][j] = 0
                        self.kolor[i + 2][j] = -1

                        obraz = self.buttons[i + 3][j].get_image()
                        obraz.clear()
                        self.plansza[i + 3][j] = 0
                        self.kolor[i + 3][j] = -1

                        obraz = self.buttons[i + 4][j].get_image()
                        obraz.clear()
                        self.plansza[i + 4][j] = 0
                        self.kolor[i + 4][j] = -1

        for i in range(10):
            for j in range(6):
                for kol in range(5):
                    if((self.kolor[i][j] == kol) & (self.kolor[i][j + 1] == kol) & (self.kolor[i][j + 2] == kol) &
                       (self.kolor[i][j + 3] == kol) & (self.kolor[i][j + 4] == kol)):
                        obraz = self.buttons[i][j].get_image()
                        obraz.clear()
                        self.plansza[i][j] = 0
                        self.kolor[i][j] = -1

                        obraz = self.buttons[i][j + 1].get_image()
                        obraz.clear()
                        self.plansza[i][j + 1] = 0
                        self.kolor[i][j + 1] = -1

                        obraz = self.buttons[i][j + 2].get_image()
                        obraz.clear()
                        self.plansza[i][j + 2] = 0
                        self.kolor[i][j + 2] = -1

                        obraz = self.buttons[i][j + 3].get_image()
                        obraz.clear()
                        self.plansza[i][j + 3] = 0
                        self.kolor[i][j + 3] = -1

                        obraz = self.buttons[i][j + 4].get_image()
                        obraz.clear()
                        self.plansza[i][j + 4] = 0
                        self.kolor[i][j + 4] = -1
        for i in range(6):
            for j in range(6):
                for kol in range(5):
                    if((self.kolor[i][j] == kol) & (self.kolor[i + 1][j + 1] == kol) & (self.kolor[i + 2][j + 2] == kol)
                       & (self.kolor[i + 3][j + 3] == kol) & (self.kolor[i + 4][j + 4] == kol)):
                        obraz = self.buttons[i][j].get_image()
                        obraz.clear()
                        self.plansza[i][j] = 0
                        self.kolor[i][j] = -1

                        obraz = self.buttons[i + 1][j + 1].get_image()
                        obraz.clear()
                        self.plansza[i + 1][j + 1] = 0
                        self.kolor[i + 1][j + 1] = -1

                        obraz = self.buttons[i + 2][j + 2].get_image()
                        obraz.clear()
                        self.plansza[i + 2][j + 2] = 0
                        self.kolor[i + 2][j + 2] = -1

                        obraz = self.buttons[i + 3][j + 3].get_image()
                        obraz.clear()
                        self.plansza[i + 3][j + 3] = 0
                        self.kolor[i + 3][j + 3] = -1

                        obraz = self.buttons[i + 4][j + 4].get_image()
                        obraz.clear()
                        self.plansza[i + 4][j + 4] = 0
                        self.kolor[i + 4][j + 4] = -1
        for i in range(6):
            for j in range(4, 10):
                for kol in range(5):
                    if((self.kolor[i][j] == kol) & (self.kolor[i + 1][j - 1] == kol) & (self.kolor[i + 2][j - 2] == kol)
                       & (self.kolor[i + 3][j - 3] == kol) & (self.kolor[i + 4][j - 4] == kol)):
                        obraz = self.buttons[i][j].get_image()
                        obraz.clear()
                        self.plansza[i][j] = 0
                        self.kolor[i][j] = -1

                        obraz = self.buttons[i + 1][j - 1].get_image()
                        obraz.clear()
                        self.plansza[i + 1][j - 1] = 0
                        self.kolor[i + 1][j - 1] = -1

                        obraz = self.buttons[i + 2][j - 2].get_image()
                        obraz.clear()
                        self.plansza[i + 2][j - 2] = 0
                        self.kolor[i + 2][j - 2] = -1

                        obraz = self.buttons[i + 3][j - 3].get_image()
                        obraz.clear()
                        self.plansza[i + 3][j - 3] = 0
                        self.kolor[i + 3][j - 3] = -1

                        obraz = self.buttons[i + 4][j - 4].get_image()
                        obraz.clear()
                        self.plansza[i + 4][j - 4] = 0
                        self.kolor[i + 4][j - 4] = -1

    def losuj_kulki(self):
        """ Metoda losujaca dodatkowe kulki do planszy."""
        # wolne - lista zawierajaca puste pola
        wolne = []
        # dodawanie wolnych miejsc do listy
        for i in range(10):
            for j in range(10):
                # sprawdzenie czy w danym miejscu jest wolne miejsce
                if self.plansza[i][j] == 0:
                    # dodanie wolnego miejsca do listy
                    wolne.append((i, j))
        # generowanie 3 kulek
        if len(wolne) >= 3:
            for i in range(3):
                # loskul - zawiera liczbe od 0 - 4 odpowiadajaca za kolor kulki
                # wylosuj - zawiera informacje o wylosowanym wolnym miejscu w liscie
                # kulka - zawiera zaladowany obrazek z ustawionym scalowaniem z wczesniej wylosowanym kolorem kulki
                loskul = random.randint(0, 4)
                kulka = Gtk.Image.new_from_pixbuf(
                    GdkPixbuf.Pixbuf.new_from_file_at_scale(self.tablica_kulek[loskul], 35, 35, True))
                wylosuj = random.randint(0, len(wolne) - 1)
                # x - zawiera polozenie kulki w pionie
                # y - zawiera polozenie kulki w poziomie
                x = wolne[wylosuj][0]
                y = wolne[wylosuj][1]
                # ustawienie obrazka na przycisku
                self.buttons[x][y].set_image(kulka)
                # ustawienie pola wolnego na planszy na zajete
                self.plansza[x][y] = 1
                # zapamietanie koloru kulki
                self.kolor[x][y] = loskul
                # usuniecie wolnego miejsca z listy
                del wolne[wylosuj]
        # generowanie 2 kulek
        elif len(wolne) == 2:
            for i in range(2):
                # loskul - zawiera liczbe od 0 - 4 odpowiadajaca za kolor kulki
                # wylosuj - zawiera informacje o wylosowanym wolnym miejscu w liscie
                # kulka - zawiera zaladowany obrazek z ustawionym scalowaniem z wczesniej wylosowanym kolorem kulki
                loskul = random.randint(0, 4)
                kulka = Gtk.Image.new_from_pixbuf(
                    GdkPixbuf.Pixbuf.new_from_file_at_scale(self.tablica_kulek[loskul], 35, 35, True))
                wylosuj = random.randint(0, len(wolne) - 1)
                # x - zawiera polozenie kulki w pionie
                # y - zawiera polozenie kulki w poziomie
                x = wolne[wylosuj][0]
                y = wolne[wylosuj][1]
                # ustawienie obrazka na przycisku
                self.buttons[x][y].set_image(kulka)
                # ustawienie pola wolnego na planszy na zajete
                self.plansza[x][y] = 1
                # zapamietanie koloru kulki
                self.kolor[x][y] = loskul
                # usuniecie wolnego miejsca z listy
                del wolne[wylosuj]
        # generowanie 1 kulki
        elif len(wolne) == 1:
            # loskul - zawiera liczbe od 0 - 4 odpowiadajaca za kolor kulki
            # wylosuj - zawiera informacje o wylosowanym wolnym miejscu w liscie
            # kulka - zawiera zaladowany obrazek z ustawionym scalowaniem z wczesniej wylosowanym kolorem kulki
            loskul = random.randint(0, 4)
            kulka = Gtk.Image.new_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file_at_scale(self.tablica_kulek[loskul], 35, 35, True))
            wylosuj = random.randint(0, len(wolne) - 1)
            # x - zawiera polozenie kulki w pionie
            # y - zawiera polozenie kulki w poziomie
            x = wolne[wylosuj][0]
            y = wolne[wylosuj][1]
            # ustawienie obrazka na przycisku
            self.buttons[x][y].set_image(kulka)
            # ustawienie pola wolnego na planszy na zajete
            self.plansza[x][y] = 1
            # zapamietanie koloru kulki
            self.kolor[x][y] = loskul
            # usuniecie wolnego miejsca z listy
            del wolne[wylosuj]
        # Koniec Gry
        if len(wolne) == 0:

            print "Koniec Gry!"

    def wlaczono(self, button, x, y):
        """ Metoda przesuwajaca kulki na planszy.

        Przyjmuje przycisk i jego wspolrzedne.
        button - obiekt typu ToggleButton
        x - pozycja kolumny nacisnietego buttona
        y - pozycja wiersza nacisnietego buttona
        """
        # zwiekszam nacisniecie guzika o jeden
        self.nacisniecia += 1
        # jezeli nacisnieto pierwszy przycisk
        if self.nacisniecia == 1:

            # sprawdzaenie czy plansza w tym miejscu jest niepusta
            if self.plansza[x][y] != 0:
                # tmpbutton - przechowuje polozenie pierwszego nacisnietego buttona
                self.tmpbutton = button
                # kulkaIM - pobiera i przechowuje obrazek
                self.kulkaIM = button.get_image()
                # pozycjax - przechowuje kolumne w ktorej znajduje sie wybrana kulka
                # pozycjay - przechowuje wiersz w ktorym znajduje sie wybrana kulka
                self.pozycjax = x
                self.pozycjay = y
            else:
                print "Nie wybrales Kulki!"
                # zmiana stanu przycisku
                button.set_active(True)
                # zerowanie nacisniec
                self.nacisniecia = 0
        #jezeli nacisnieto drugi przycisk
        if self.nacisniecia == 2:
            if self.plansza[x][y] != 1:
                #sprawdzam jaki kolor kulki mial nacisniety pierwszy przycisk
                if self.kolor[self.pozycjax][self.pozycjay] == 0:
                    # kulka - zawiera wygenerowany obrazek
                    kulka = Gtk.Image.new_from_pixbuf(
                        GdkPixbuf.Pixbuf.new_from_file_at_scale(self.tablica_kulek[0], 35, 35, True))
                    # ustawienie obrazka na buttonie
                    button.set_image(kulka)
                    # wyczyszczenie obrazka z pierwszego klikniecia
                    self.kulkaIM.clear()
                    # zapamietanie koloru kulki
                    self.kolor[x][y] = 0

                elif self.kolor[self.pozycjax][self.pozycjay] == 1:
                    # kulka - zawiera wygenerowany obrazek
                    kulka = Gtk.Image.new_from_pixbuf(
                        GdkPixbuf.Pixbuf.new_from_file_at_scale(self.tablica_kulek[1], 35, 35, True))
                    # ustawienie obrazka na buttonie
                    button.set_image(kulka)
                    # wyczyszczenie obrazka z pierwszego klikniecia
                    self.kulkaIM.clear()
                    # zapamietanie koloru kulki
                    self.kolor[x][y] = 1

                elif self.kolor[self.pozycjax][self.pozycjay] == 2:
                    # kulka - zawiera wygenerowany obrazek
                    kulka = Gtk.Image.new_from_pixbuf(
                        GdkPixbuf.Pixbuf.new_from_file_at_scale(self.tablica_kulek[2], 35, 35, True))
                    # ustawienie obrazka na buttonie
                    button.set_image(kulka)
                    # wyczyszczenie obrazka z pierwszego klikniecia
                    self.kulkaIM.clear()
                    # zapamietanie koloru kulki
                    self.kolor[x][y] = 2

                elif self.kolor[self.pozycjax][self.pozycjay] == 3:
                    # kulka - zawiera wygenerowany obrazek
                    kulka = Gtk.Image.new_from_pixbuf(
                        GdkPixbuf.Pixbuf.new_from_file_at_scale(self.tablica_kulek[3], 35, 35, True))
                    # ustawienie obrazka na buttonie
                    button.set_image(kulka)
                    # wyczyszczenie obrazka z pierwszego klikniecia
                    self.kulkaIM.clear()
                    # zapamietanie koloru kulki
                    self.kolor[x][y] = 3

                elif self.kolor[self.pozycjax][self.pozycjay] == 4:
                    # kulka - zawiera wygenerowany obrazek
                    kulka = Gtk.Image.new_from_pixbuf(
                        GdkPixbuf.Pixbuf.new_from_file_at_scale(self.tablica_kulek[4], 35, 35, True))
                    # ustawienie obrazka na buttonie
                    button.set_image(kulka)
                    # wyczyszczenie obrazka z pierwszego klikniecia
                    self.kulkaIM.clear()
                    # zapamietanie koloru kulki
                    self.kolor[x][y] = 4
                # ustawienie pola pierwszego przycisku na wolne
                self.kolor[self.pozycjax][self.pozycjay] = -1
                # zmiana pola na zajete
                self.plansza[x][y] = 1
                # zmiana pola na wolne
                self.plansza[self.pozycjax][self.pozycjay] = 0
                # zerowanie nacisnietych przyciskow
                self.nacisniecia = 0
                # zwieksz biezacy wynik o jeden
                self.wynik += 1
                # zmiana biezacego wyniku gracza
                self.biezace.set_label("Liczba punktow:<b> {} </b>".format(self.wynik))
                self.biezace.set_use_markup(True)
                # zmiana stanow nacisnietych przyciskow
                button.set_active(True)
                self.tmpbutton.set_active(False)
                # linia z 5 kulek
                self.sprawdz()
                # losowanie kulek
                self.losuj_kulki()
            else:
                print "Nie mozna w tym miejscu postawic kulki!"
                # zmiana stanow nacisnietych przyciskow
                button.set_active(True)
                self.tmpbutton.set_active(False)
                # zerowanie nacisnietych przyciskow
                self.nacisniecia = 0

# uruchamiam glowna petle tylko jesi program jest uruchamiany "wprost"
# bez tej linijki okienko pojawi sie przy importowaniu tego pliku zrodlowego z poziomu innego kodu
if __name__ == "__main__":
    a = Kulki()

    Gtk.main()
