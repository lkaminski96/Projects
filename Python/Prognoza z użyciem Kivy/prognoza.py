# -*- coding: utf-8 -*-
# import potrzebnych bibliotek
import urllib2
import json
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout


class Prognoza(App):
    """ Klasa reprezentujaca Prognoze Pogody."""
    def build(self):
        """ Metoda odpowiadajaca za budowanie aplikacji."""
        # box - glowny kontener okna, ktory zawiera inne widgety
        self.box = BoxLayout(orientation='vertical')
        # aktualna - przycisk pozwalajacy wyswietlic aktualna pogode
        self.aktualna = Button(text='Aktualna Pogoda', size=(200, 100))
        self.aktualna.bind(on_press=self.aktualnie)
        # dlgterm - przycisk pozwalajacy wyswietlic prognoze dlugoterminowa
        self.dlgterm = Button(text='Prognoza na 5 dni', size=(200, 100))
        self.dlgterm.bind(on_press=self.terminowa)
        # powrot - przycisk pozwalajacy wrocic do okna wyboru prognozy
        self.powrot = Button(text='Powrót', size=(100, 50), size_hint=(None, None), pos_hint={'center_x': 0.95})
        self.powrot.bind(on_press=self.wroc)
        # dodanie przyciskow do kontenera
        self.box.add_widget(self.aktualna)
        self.box.add_widget(self.dlgterm)
        return self.box

    def aktualnie(self, button):
        """ Metoda wyswietlajaca aktualna prognoze pogody.

        button - nacisniety przycisk
        Zwraca kontener zawierajacy widok prognozy.
        """
        # usuwanie niepotrzebnych widgetow
        self.box.remove_widget(self.aktualna)
        self.box.remove_widget(self.dlgterm)
        # pogoda - zawiera widget prognozy pogody
        self.pogoda = AktualnaPogoda()
        # dodawanie widgetow na prosbe uzytkownika
        self.box.add_widget(self.powrot)
        self.box.add_widget(self.pogoda)
        return self.box

    def terminowa(self, button):
        """ Metoda wyswietlajaca dlugoterminowa prognoze pogody.

        button - nacisniety przycisk
        Zwraca kontener zawierajacy widok prognozy.
        """
        # usuwanie niepotrzebnych widgetow
        self.box.remove_widget(self.aktualna)
        self.box.remove_widget(self.dlgterm)
        # pogoda - zawiera widget prognozy pogody
        self.pogoda = PogodaDlgTerm()
        # dodawanie widgetow na prosbe uzytkownika
        self.box.add_widget(self.powrot)
        self.box.add_widget(self.pogoda)

        return self.box

    def wroc(self, button):
        """ Metoda wracajaca do okna glownego.

        button - nacisniety przycisk
        Zwraca kontener zawierajacy mozliwosc wyboru wyswietlenia prognozy.
        """
        # usuwanie niepotrzebnych widgetow
        self.box.remove_widget(self.pogoda)
        self.box.remove_widget(self.powrot)
        # dodawanie widgetow na prosbe uzytkownika
        self.box.add_widget(self.aktualna)
        self.box.add_widget(self.dlgterm)
        return self.box


class AktualnaPogoda(BoxLayout):
    """ Klasa przedstawiajaca instancje aktualnej pogody.

    Dziedziczy po kontenerze Box.
    """
    def __init__(self):
        """ Inicjalizator obiektu."""
        super(AktualnaPogoda, self).__init__()
        # ustawienie orientacji
        self.orientation = 'vertical'
        # pobranie danych ze strony internetowej
        link = urllib2.urlopen('https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20'
                               'where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22Torun%'
                               '2C%20pl%22%20)%20and%20u%3D%27c%27&format=json&env=store%3A%2F%2Fdatatables.org%2'
                               'Falltableswithkeys')
        # wczytanie danych ze strony
        datajason = link.read()
        book = json.loads(datajason, encoding='UTF-8')
        # aktualna data wygenerowania pogody
        data = Label(text=book["query"]["results"]["channel"]["item"]["condition"]["date"])
        # aktualne stopnie
        stopnie = Label(text=book["query"]["results"]["channel"]["item"]["condition"]["temp"] + ' stopni Celcjusza')
        # link do obrazka
        opis = book["query"]["results"]["channel"]["item"]["description"].split('"')
        # strona - zawiera link do obrazka
        strona = opis[1]
        # linkos - lista zawierajaca link podzielony wzgledem odpowiedniego znacznika
        linkos = strona.split('/')
        # usuniecie ostatniej czesci linku
        del (linkos[-1])
        # wyzerowanie linku
        self.link = ''
        # sklejenie linku spowrotem w calosc bez koncowki
        for tekst in linkos:
            self.link += tekst + '/'
        # i - zmienna pozwalajaca na zliczanie ilosci dni do pobrania danych
        i = 0
        for dzien in book["query"]["results"]["channel"]["item"]["forecast"]:
            if i == 0:
                # obraz - przechowuje obrazek odpowiadajacy pogodzie
                # max - zawiera maksymalna temperature
                # min - zawiera minimalna temperature
                obraz = AsyncImage(source=self.link + dzien["code"] + '.gif')
                max = Label(text='Maksymalna Temp: ' + dzien["high"])
                min = Label(text='Minimalna Temp: ' + dzien["low"])
                break
        # dodanie widgetow do kontenera(Box)
        self.add_widget(data)
        self.add_widget(stopnie)
        self.add_widget(obraz)
        self.add_widget(max)
        self.add_widget(min)


class PogodaDlgTerm(GridLayout):
    """ Klasa przedstawiajaca instancje prognozy pogody dlugoterminowej.

    Dziedziczy po kontenerze Grid.
    """
    def __init__(self):
        """ Inicjalizator obiektu."""
        super(PogodaDlgTerm, self).__init__()
        # ustawienie kolumn i wiersz dla siatki
        self.cols = 4
        self.rows = 6
        # pobranie danych ze strony internetowej
        link = urllib2.urlopen('https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20'
                               'where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22Torun%'
                               '2C%20pl%22%20)%20and%20u%3D%27c%27&format=json&env=store%3A%2F%2Fdatatables.org%2'
                               'Falltableswithkeys')
        # wczytanie danych do programu ze strony
        datajason = link.read()
        book = json.loads(datajason, encoding='UTF-8')
        # link do obrazka
        opis = book["query"]["results"]["channel"]["item"]["description"].split('"')
        # strona - zawiera link do obrazka
        strona = opis[1]
        # linkos - lista zawierajaca link podzielony wzgledem odpowiedniego znacznika
        linkos = strona.split('/')
        # usuniecie ostatniej czesci linku
        del (linkos[-1])
        # wyzerowanie linku
        self.link = ''
        # sklejenie linku spowrotem w calosc bez koncowki
        for tekst in linkos:
            self.link += tekst + '/'
        # dodanie naglowkow dla kolumn do siatki
        self.add_widget(Label(text='Data'))
        self.add_widget(Label(text='Pogoda'))
        self.add_widget(Label(text='Maksymalna Temp'))
        self.add_widget(Label(text='Minimalna Temp'))
        # i - zmienna pozwalajaca na zliczanie ilosci dni do pobrania danych
        i = 0
        # petla wyciagajaca dane z prognozy pogody
        for dzien in book["query"]["results"]["channel"]["item"]["forecast"]:
            # pomijam aktualna pogode
            if i == 0:
                i += 1
                continue
            # data - zawiera date prognozy i dodaje do siatki
            data = Label(text=dzien["day"] + ', ' + dzien["date"])
            self.add_widget(data)
            # obraz - zawiera obrazek odpowiedni do pogody i dodaje do siatki
            obraz = AsyncImage(source=self.link + dzien["code"] + '.gif')
            self.add_widget(obraz)
            # max - maksymalna temperatura i dodaje do siatki
            max = Label(text=dzien["high"])
            self.add_widget(max)
            # min - minimalna temperatura i dodaje do siatki
            min = Label(text=dzien["low"])
            self.add_widget(min)
            i += 1
            # jezeli jest juz 5 dni to przerywam pobieranie danych
            if i == 6:
                break


if __name__ == '__main__':
    Prognoza().run()