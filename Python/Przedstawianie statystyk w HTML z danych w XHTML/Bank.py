# -*- coding: utf-8 -*-
# import potrzebnych bibliotek
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import StringIO
import numpy as np
# UWAGA : Program kompliuje sie na moim komputerze 2 - 3 minuty


def rolnictwo(lista):
    """Funkcja zbierajaca statystyki wielkosci obszarow uprawnych.

    lista - przechowuje zbior list podanych rekordow dla poszczegolnych panstw
    Zwraca liste wszystkich statystyk dla poszczegolnych panstw.
    """
    # wynik - lista zawierajaca wynik koncowy dzialania funkcji(lata i wartosci dla poszczegolnych panstw)
    wynik = []
    for panstwo in lista:
        # rok - lista zawierajaca lata
        # wartosc - lista zawierajaca wartosci dla lat
        rok = []
        wartosc = []
        for element in panstwo:
            # sprawdzenie czy klucz posiada odpowiednia wartosc
            if element[1].get('key') == "AG.LND.AGRI.ZS":
                # dodanie roku do listy
                rok.append(int(element[2].text))
                # rozpatrywanie przypadku w ktorym wartosc jest None
                if element[3].text is None:
                    wartosc.append(element[3].text)
                else:
                    wartosc.append(float(element[3].text))
        # dodawanie list dla poszczegolnych panstw do listy wynikowej
        wynik.append(rok)
        wynik.append(wartosc)

    return wynik


def eksport(lista):
    """Funkcja zbierajaca statystyki wielkosci eksportu dobr i uslug.

    lista - przechowuje zbior list podanych rekordow dla poszczegolnych panstw
    Zwraca liste wszystkich statystyk dla poszczegolnych panstw.
    """
    # wynik - lista zawierajaca wynik koncowy dzialania funkcji(lata i wartosci dla poszczegolnych panstw)
    wynik = []
    for panstwo in lista:
        # rok - lista zawierajaca lata
        # wartosc - lista zawierajaca wartosci dla lat
        rok = []
        wartosc = []
        for element in panstwo:
            # sprawdzenie czy klucz posiada odpowiednia wartosc
            if element[1].get('key') == "NE.EXP.GNFS.CD":
                # dodanie roku do listy
                rok.append(int(element[2].text))
                # rozpatrywanie przypadku w ktorym wartosc jest None
                if element[3].text is None:
                    wartosc.append(element[3].text)
                else:
                    wartosc.append(float(element[3].text))
        # dodawanie list dla poszczegolnych panstw do listy wynikowej
        wynik.append(rok)
        wynik.append(wartosc)

    return wynik


def ludnosc(lista):
    """Funkcja zbierajaca statystyki gestosci zaludnienia.

    lista - przechowuje zbior list podanych rekordow dla poszczegolnych panstw
    Zwraca liste wszystkich statystyk dla poszczegolnych panstw.
    """
    # wynik - lista zawierajaca wynik koncowy dzialania funkcji(lata i wartosci dla poszczegolnych panstw)
    wynik = []
    for panstwo in lista:
        # rok - lista zawierajaca lata
        # wartosc - lista zawierajaca wartosci dla lat
        rok = []
        wartosc = []
        for element in panstwo:
            # sprawdzenie czy klucz posiada odpowiednia wartosc
            if element[1].get('key') == "EN.POP.DNST":
                # dodanie roku do listy
                rok.append(int(element[2].text))
                # rozpatrywanie przypadku w ktorym wartosc jest None
                if element[3].text is None:
                    wartosc.append(element[3].text)
                else:
                    wartosc.append(float(element[3].text))
        # dodawanie list dla poszczegolnych panstw do listy wynikowej
        wynik.append(rok)
        wynik.append(wartosc)

    return wynik


def turysci(lista):
    """Funkcja zbierajaca statystyki ilosci przyjzdzajacych turystow.

    lista - przechowuje zbior list podanych rekordow dla poszczegolnych panstw
    Zwraca liste wszystkich statystyk dla poszczegolnych panstw.
    """
    # wynik - lista zawierajaca wynik koncowy dzialania funkcji(lata i wartosci dla poszczegolnych panstw)
    wynik = []
    for panstwo in lista:
        # rok - lista zawierajaca lata
        # wartosc - lista zawierajaca wartosci dla lat
        rok = []
        wartosc = []
        for element in panstwo:
            # sprawdzenie czy klucz posiada odpowiednia wartosc
            if element[1].get('key') == "ST.INT.ARVL":
                # dodanie roku do listy
                rok.append(int(element[2].text))
                # rozpatrywanie przypadku w ktorym wartosc jest None
                if element[3].text is None:
                    wartosc.append(element[3].text)
                else:
                    wartosc.append(float(element[3].text))
        # dodawanie list dla poszczegolnych panstw do listy wynikowej
        wynik.append(rok)
        wynik.append(wartosc)

    return wynik


def sprawdz(lista):
    """Funkcja usuwajaca puste wartosci.

    lista - przechowuje lata i wartosci dla poszczegolnych lat
    Zwraca liste wyselekcjonowanych danych ktore sa dostepne dane dla poszczegolnych panstw.
    """
    # do_usuniecia - lista zawierajaca indeksy pol ktore zostana usuniete z glownej listy
    do_usuniecia = []
    # petla przechodzaca po wartosciach
    for i in range(len(lista) / 2):
        # j - indeks wartosci dla poszczgolnego panstwa
        j = 2 * i + 1
        # k - indeks pod ktorym nie ma wartosci
        k = 0
        # sprawdzanie ktore elementy sa bez wartosci oraz dodawanie ich do listy do usuniecia
        for el in lista[j]:
            if el is None:
                # zastosowanie unikalnosci indeksow
                if not k in do_usuniecia:
                    do_usuniecia.append(k)

            k += 1
    # sortowanie listy z indeksami do usuniecia w sposob rosnacy
    do_usuniecia.sort()
    # nowalista - lista zawierajaca statystyki dostepne dla wszystkich panstw odpowiednio [Lata],[Wartosc]
    nowalista = []
    for i in range(len(lista)):
        # wartosc - lista zawierajaca poszczegolne dane z glownej listy
        wartosc = []
        # dodawanie wartosci, ktore sa dostepne dla wszystkich panstw do tabeli wartosc
        for j in range(len(lista[i])):
            # zastosowanie unikalnosci indeksow dla ktorych nie ma wartosci
            if not j in do_usuniecia:
                wartosc.append(lista[i][j])
        # dodawanie listy zawierajacej wynik dla poszczegolnych danych
        nowalista.append(wartosc)

    return nowalista


def generuj(Panstwa, tytul):
    """Funkcja generujaca wykres do pliku.

    Panstwa - zawiera liste wszystkich danych poszczegolnych panstw do wykresu
    tytul - zawiera tytul wykresu
    Zwraca obrazek do dokumentu html.
    """
    # wyrzucenie lat dla ktorych nie ma dostepnych wartosci dla wszystkich panstw
    Panstwa = sprawdz(Panstwa)
    # generowanie wykresu
    plt.plot(Panstwa[0], Panstwa[1], label=u"Polska", color='red', linewidth=(1.5))
    plt.plot(Panstwa[2], Panstwa[3], label=u"Ukraina", color='yellow', linewidth=(1.5))
    plt.plot(Panstwa[4], Panstwa[5], label=u"Niemcy", color='black', linewidth=(1.5))
    plt.plot(Panstwa[6], Panstwa[7], label=u"Czechy", color='blue', linewidth=(1.5))
    # ustalenie skali dla osi OX
    plt.xticks(np.arange(min(Panstwa[0]), max(Panstwa[0]) + 1, 5.0))
    # nadanie tytulu oraz legendy z pozycjonowaniem
    plt.title(tytul)
    plt.legend(loc='best')
    # nadanie nazw osia OX i OY
    plt.xlabel(u"Lata", fontsize="23")
    plt.ylabel(u"Wartości dla lat", fontsize="23")
    # utworzenie siatki
    plt.grid(ls="solid", color=(0.7, 0.8, 1.0))
    # bufor 'imitujący' obiekt pliku
    imgdata = StringIO.StringIO()
    plt.savefig(imgdata, format="svg")
    # pobieram dane z bufora
    svg_txt = imgdata.getvalue()
    # czyszczę bufor ("zamykam" wirtualny plik)
    imgdata.close()
    # zamykam tworzenie wykresu
    plt.close()

    return svg_txt

#: panstwa_pliki - lista zawierajaca nazwy plikow do odczytu danych
panstwa_pliki = ['pol_Country_en_xml_v2.xml', 'ukr_Country_en_xml_v2.xml',
                 'deu_Country_en_xml_v2.xml', 'cze_Country_en_xml_v2.xml']
#: tytulu - lista zawierajaca tytuly do wykresow
tytuly = [u'Wielkość Obszarów Uprawnych', u'Wielkość Eksportu Dóbr i Usług',
          u'Gęstość Zaludnienia', u'Ilość Przyjeżdżających Turystów']

#: korzen - zawiera szablon dokumentu
korzen = ET.Element("html")
#: head - nagłowek
head = ET.SubElement(korzen, "head")
#: title - tytul
title = ET.SubElement(head, "title")
title.text = u"Statystyki Banku Światowego"
#: body - zawiera zawartosc dokumentu
body = ET.SubElement(korzen, "body")

# glowna petla
for i in range(len(tytuly)):
    # Panstwa - lista zawierajaca listy rekordow dla poszczegolnych panstw odpowiednio [Lata], [Wartosci]
    # do_wykresu - lista zawierajaca liste wyselekcjonowanych lat i wartosci dla poszczegolnych lat
    Panstwa = []
    do_wykresu = []
    # parsowanie danych xml
    for j in range(len(panstwa_pliki)):
        tree = ET.parse(panstwa_pliki[j])
        root = tree.getroot()
        # lista - zawiera rekordy do znalezienia lat i wartosci dla poszczegolnych panstw
        lista = []
        # dodawanie recordow do listy
        for record in root.findall('data'):
            lista += record
        # dodawanie wytworzonej listy z rekordami do "glownej" listy przechowywujacej dane o wszystkich panstwach
        Panstwa.append(lista)
    # w zaleznosci od parametru i wywoluje odpowiednia funkcje
    if i == 0:
        do_wykresu = rolnictwo(Panstwa)
    elif i == 1:
        do_wykresu = eksport(Panstwa)
    elif i == 2:
        do_wykresu = ludnosc(Panstwa)
    else:
        do_wykresu = turysci(Panstwa)
    # wykres - przechowuje obraz wykresu z rozszerzeniem .svg
    wykres = generuj(do_wykresu, tytuly[i])
    # plik svg jest poprawnym dokumentem XML
    # zanim go przeczytamy, informujemy bibliotekę o nowej przestrzni nazw
    # do której należą niektóre z elementów pliku SVG
    # dokumentacja: http://effbot.org/zone/element-namespaces.htm
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

    # wczytuje dokument, metoda fromstring zwraca korzeń , czyli element svg
    svg_tree_root = ET.fromstring(wykres)

    # dodaje obrazek do dokumentu
    paragraph = ET.SubElement(body, "p")
    paragraph.append(svg_tree_root)


# zapisujemy wynik do pliku
with open("stats.html", "w") as f:
    f.write(ET.tostring(korzen))





