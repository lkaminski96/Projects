# -*- coding: utf-8 -*-
# import potrzebnych bibliotek
import urllib2
from bs4 import BeautifulSoup
import gi
import re
import os
import random
# wymagamy biblioteki w wersji min 3.0
gi.require_version('Gtk', '3.0')
# metody do korzystania z Gtk
from gi.repository import Gtk


class Komiks():
    """Klasa przedstawiajaca obiekt Komiks."""
    def __init__(self):
        """ Inicjalizator obiektu."""
        self.window = Gtk.Window(title="Komiks")
        self.window.set_default_size(700, 700)
        # wysrodkowanie okna
        self.window.set_position(1)
        # proba utworzenia folderu cache jezeli nie istenieje
        try:
            os.mkdir('cache')
        except OSError:
            print "Folder juz istnieje!"
        # nrkomiksu - lista zawierajaca posiadane lokalnie komiksy
        # pierwszykomiks - zawiera nr. pierwszego komiksu
        self.nrkomiksu = []
        self.pierwszykomiks = 1
        # polaczenie ze strona internetowa
        response = urllib2.urlopen('https://xkcd.com')
        html = response.read()
        soup = BeautifulSoup(html, "html5lib")
        # wyszukanie wszystkich posiadanych komiksow w katalogu cache i dodanie ich do listy
        for root, dirs, files in os.walk("cache/"):
            for filename in files:
                numerek = re.findall('\d+', filename)
                self.nrkomiksu.append(int(numerek[0]))
        # sortowanie listy
        self.nrkomiksu.sort()
        # wyciagniecie numeru komiksu
        for link in soup.find_all(string=re.compile('Permanent link to this comic: https://xkcd.com/')):
            numer = link
        # number - przechowuje numer komiksu
        number = re.findall('\d+', numer)
        # najnowszykomiks - przechowuje nr. najnowszego komiksu
        # biezacykomiks - przechowuje nr. biezacego komiksu
        self.najnowszykomiks = int(number[0])
        self.biezacykomiks = int(number[0])

        # wyciagniecie tytulu i ustawienie go w oknie wraz z numerem komiksu
        for link in soup.find_all("div", {"id": "ctitle"}):
            tytul = link.get_text()
        self.title = Gtk.Label()
        self.title.set_label("<b> {} </b> {}".format(tytul, number[0]))
        self.title.set_use_markup(True)

        # wstawianie komiksu do okna
        self.obraz = Gtk.Image()
        # dodanie mozliwosci przesuwania obrazka w Oknie scrollowanym z odpowiednimi wlasciwosciami
        przesuwaj = Gtk.ScrolledWindow()
        przesuwaj.add(self.obraz)
        przesuwaj.set_min_content_height(600)
        przesuwaj.set_min_content_width(600)
        # widocznosc scroll barow
        przesuwaj.set_policy(0, 0)
        # sprawdzenie czy dany komiks byl juz sciagniety
        if int(number[0]) in self.nrkomiksu:
            # ustawienie komiksu w oknie
            self.obraz.set_from_file('cache/' + str(number[0]) + '.png')

        else:
            # jezeli nie to dodanie numeru komiksu do listy oraz sortowanie jej
            self.nrkomiksu.append(int(number[0]))
            self.nrkomiksu.sort()
            # wyciagniecie komiksu ze strony
            for link in soup.find_all("div", {"id": "comic"}):
                tmp = link.img.get('src')
                # dodanie przedrostka htttps jezeli owakiego komiks nie ma
                if tmp[:1] == '/':
                    image = 'https:' + tmp
                else:
                    image = tmp
                # zapisanie komiksu do pliku jako obrazek
                with open('cache/' + str(number[0]) + '.png', 'wb') as f:
                    f.write(urllib2.urlopen(image).read())
            # ustawienie komiksu w oknie
            self.obraz.set_from_file('cache/' + str(number[0]) + '.png')

        # wlasny numer komiksu
        podpis = Gtk.Label("Podaj numer komiksu, ktory chcialbys zobaczyc")
        self.wlasny = Gtk.Entry()
        self.wlasny.connect("activate", self.wybrany)

        # self.przyciski - vertical box przechowywujacy przyciski
        self.przyciski = Gtk.HBox(homogeneous=True)
        # przyciski, dodawanie przyciskow do HBox'a oraz podpinanie zdarzen do przyciskow
        # odpowiednio: pierwszy komiks, poprzedni, losowy, nastepny, ostatni(najnowszy)
        pierwszy = Gtk.Button(label=" |< ")
        self.przyciski.pack_start(pierwszy, False, True, 10)
        pierwszy.connect("clicked", self.pierwszy)

        wczesniejszy = Gtk.Button(label=" < Prev")
        self.przyciski.pack_start(wczesniejszy, False, True, 10)
        wczesniejszy.connect("clicked", self.poprzedni)

        losowy = Gtk.Button(label=" Random ")
        self.przyciski.pack_start(losowy, False, True, 10)
        losowy.connect("clicked", self.losuj)

        kolejny = Gtk.Button(label=" Next > ")
        self.przyciski.pack_start(kolejny, False, True, 10)
        kolejny.connect("clicked", self.nastepny)

        ostatni = Gtk.Button(label=" >| ")
        self.przyciski.pack_start(ostatni, False, True, 10)
        ostatni.connect("clicked", self.ostatni)

        # dodawanie elementow do glownego boxa
        self.glowny = Gtk.VBox()
        self.glowny.pack_start(self.title, False, False, 10)
        self.glowny.pack_start(przesuwaj, False, False, 10)
        self.glowny.pack_start(podpis, False, False, 0)
        self.glowny.pack_start(self.wlasny, False, False, 0)
        self.glowny.pack_start(self.przyciski, False, False, 10)

        # podpiecie zdarzenia wylaczenia okna przyciskiem X
        self.window.connect("delete-event", lambda x, y: Gtk.main_quit())
        # dodanie boxa glownego do okna
        self.window.add(self.glowny)
        # wyswietlenie wszystkiego na oknie
        self.window.show_all()

    def ustaw(self, numer):
        """Metoda ustawiajaca tytul, numer komiksu oraz komiks.

        numer - przechowuje numer komiksu
        """
        # uaktualnienie biezacego numeru komiksu
        self.biezacykomiks = numer
        # otwarcie polaczenia z odpowiednia strona na bazie numeru komiksu
        try:
            response = urllib2.urlopen('https://xkcd.com/' + str(numer) + '/')
        except:
            print "Nie mozna polaczyc sie ze strona!"
        else:
            # odczytanie i sprasowanie strony
            html = response.read()
            soup = BeautifulSoup(html, "html5lib")
            # wyciagniecie tytulu
            for link in soup.find_all("div", {"id": "ctitle"}):
                tytul = link.get_text()

            # ustawienie tytulu oraz numeru komiksu
            self.title.set_label("<b> {} </b> {}".format(tytul, numer))
            self.title.set_use_markup(True)

            # sprawdzenie czy dany komiks byl juz sciagniety
            if numer in self.nrkomiksu:
                # ustawienie komiksu w oknie
                self.obraz.set_from_file('cache/' + str(numer) + '.png')

            else:
                # jezeli nie to dodanie numeru komiksu do listy oraz sortowanie jej
                self.nrkomiksu.append(int(numer))
                self.nrkomiksu.sort()
                # wyciagniecie komiksu ze strony
                for link in soup.find_all("div", {"id": "comic"}):
                    tmp = link.img.get('src')
                    # dodanie przedrostka htttps jezeli owakiego komiks nie ma
                    if tmp[:1] == '/':
                        image = 'https:' + tmp
                    else:
                        image = tmp
                    # zapisanie komiksu do pliku jako obrazek
                    with open('cache/' + str(numer) + '.png', 'wb') as f:
                        f.write(urllib2.urlopen(image).read())
                # ustawienie komiksu w oknie
                self.obraz.set_from_file('cache/' + str(numer) + '.png')

    def wybrany(self, entry):
        """Metoda pobierajaca numer komiksu podany przez uzytkownika.

        entry - przechowuje zawartosc podana przez uzytkownika
        """
        # wybranykomiks - zawiera wyjety numer komiksu podany przez uzytkownika
        wybranykomiks = int(entry.get_text())
        # sprawdzenie czy podany numer zawiera sie w przedziale numerow komiksow
        if(wybranykomiks >= self.pierwszykomiks) & (wybranykomiks <= self.najnowszykomiks):
            self.biezacykomiks = wybranykomiks
            self.ustaw(wybranykomiks)
        else:
            print "Nie ma komiksu o podanym numerze!"
            return

    def pierwszy(self, button):
        """Metoda generujaca pierwszy komiks.

        button - obiekt typu Button
        """
        # wywolanie funkcji ustawiajacej okno
        self.ustaw(1)

    def poprzedni(self, button):
        """Metoda generujaca wczesniejsyz komiks.

        button - obiekt typu Button
        """
        # "uaktualnienie" numeru biezacego komiksu
        self.biezacykomiks -= 1
        # sprawdzenie czy komiks nie wychodzi po za zakres
        if self.biezacykomiks < self.pierwszykomiks:
            self.biezacykomiks += 1
            print "Nie ma poprzedniego komiksu!"
            return
        else:
            # wywolanie funkcji ustawiajacej okno
            self.ustaw(self.biezacykomiks)

    def losuj(self, button):
        """Metoda generujaca komiks o losowym numerze.

        button - obiekt typu Button
        """
        # losowynr - zawiera losowy numer komiksu
        losowynr = random.randint(1, self.najnowszykomiks)
        # wywolanie funkcji ustawiajacej okno
        self.ustaw(losowynr)

    def nastepny(self, button):
        """Metoda generujaca nastepny komiks.

        button - obiekt typu Button
        """
        # uaktualnienie biezacego numeru komiksu
        self.biezacykomiks += 1
        # sprawdzenie czy numer nie wychodzi po za zakres
        if self.biezacykomiks > self.najnowszykomiks:
            self.biezacykomiks -= 1
            return
        else:
            # wywolanie funkcji ustawiajacej okno
            self.ustaw(self.biezacykomiks)

    def ostatni(self, button):
        """Metoda generujaca ostatni komiks.

        button - obiekt typu Button
        """
        # wywolanie funkcji ustawiajacej okno
        self.ustaw(self.najnowszykomiks)


# uruchamiam glowna petle tylko jesi program jest uruchamiany "wprost"
# bez tej linijki okienko pojawi sie przy importowaniu tego pliku zrodlowego z poziomu innego kodu
if __name__ == "__main__":
    a = Komiks()

    Gtk.main()