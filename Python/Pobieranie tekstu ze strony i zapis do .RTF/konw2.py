#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Import potrzebnych bibliotek
from PyRTF import *
# re - biblioteka do generowania wyrazen regularnych
import re
import urllib2
import json


def rtf_encode_znak(znak):
    """Funkcja zwracajaca znak w kodowaniu PyRTF.

    znak - przechowuje znak pobrany z funkcji rtf_encode
    """
    # kod - przechowuje informacje o liczbie odpowiadajacej znakowi w ASCII lub Unicode
    kod = ord(znak)
    # zwrot znaku jezeli jest w ASCII
    if kod < 128:
        return str(znak)
    # zwrot znaku po wczesniejszym encode'owaniu go do ASCII dla PyRTF
    return '\\u' + str(kod if kod <= 32767 else kod-65536) + '?'


def rtf_encode(tekst):
    """Funkcja zwracajaca tekst w kodowaniu PyRTF.

    tekst - przechowuje tekst do encode'owania
    """
    # zwrot tekstu po wczesniejszym przerobieniu kazdego znaku na kodowanie w PyRTF
    return ''.join(rtf_encode_znak(c) for c in tekst)


def usuntagi(tekst):
    """Funkcja zwracajaca tekst bez znacznikow html.

    tekst - zawiera tekst do przerobienia
    """
    # czysc - przechowuje wyrazenie regularne do usuwania znacznikow
    czysc = re.compile('<.*?>')
    # zwracany tekst po wczesniejszym usunieciu wyrazen regularnych
    return re.sub(czysc, '', tekst)


def stworz():
    """Funkcja generujaca dokument.

    Zwraca wygenerowany dokument
    """
    # pobieranie danych
    # link - zawiera dostep do danych ze strony
    # datajason - zawiera tekst pobrany ze strony
    # book - zawiera tekst jako slownik do latwiejszej edycji
    link = urllib2.urlopen('https://polska.googleblog.com/feeds/posts/default?alt=json')
    datajason = link.read()
    book = json.loads(datajason, encoding='UTF-8')

    # tworzenie dokumentu
    # doc - zawiera pusty dokument
    # ss - zawiera arkusz stylow dla dokumentu
    # section - utworzenie sekcji
    doc = Document()
    ss = doc.StyleSheet
    section = Section()
    # dodanie sekcji do dokumentu
    doc.Sections.append(section)

    # centrowanie - zawiera mozliwosc wysrodkowania elementu
    centrowanie = ParagraphPS(alignment=3)

    # tytul - zawiera tytul strony
    tytul = rtf_encode(book["feed"]["title"]["$t"]).encode('UTF-8')
    # p - zawiera nowy paragraph z odpowiednimi ustawieniami
    p = Paragraph(ss.ParagraphStyles.Heading1, centrowanie)
    # dodanie tekstu do paragraphu z odpowiednimi ustawieniami
    p.append(TEXT(tytul, bold=True))
    # dodanie paragrafu do sekcji
    section.append(p)

    # podtytul - zawiera tekst umieszczony pod tytulem
    podtytul = rtf_encode(book["feed"]["subtitle"]["$t"]).encode('UTF-8')
    # p - zawiera nowy pusty paragraph
    p = Paragraph()
    # dodanie tekstu do paragraphu z odpowiednimi ustawieniami
    p.append(podtytul)
    # dodanie paragrafu do sekcji
    section.append(p)

    # i - pomocnicza zmienna do przechodzenia po elementach w slowniku
    i = 0
    # generowanie artykulow
    for element in book["feed"]["entry"]:

        # data - przechowuje date umieszczenia artykulu
        data = rtf_encode(book["feed"]["entry"][i]["updated"]["$t"]).encode('UTF-8')
        # wyciecie roku, miesiaca i dnia
        data = data[:10]
        # p - zawiera nowy paragraph
        p = Paragraph()
        # dodanie daty do paragraphu z odpowiednimi ustawieniami
        p.append(TEXT(data, bold=True, italic=True))
        # dodanie paragrafu do sekcji
        section.append(p)

        # tytul - przechowuje tytul umieszczenego artykulu
        tytul = rtf_encode(book["feed"]["entry"][i]["title"]["$t"]).encode('UTF-8')
        # p - zawiera nowy paragraph z odpowiednimi ustawieniami
        p = Paragraph(ss.ParagraphStyles.Heading1, centrowanie)
        # dodanie tytulu do paragraphu z odpowiednimi ustawieniami
        p.append(TEXT(tytul, bold=True))
        # dodanie paragrafu do sekcji
        section.append(p)

        # zawartosc - zawiera cala tresc artykulu
        zawartosc = rtf_encode(book["feed"]["entry"][i]["content"]["$t"]).encode('UTF-8')
        # podziel - zawiera podzielony tekst
        podziel = zawartosc.split('<br />')
        # dodawanie tekstu
        for tekst in podziel:
            # tekst - zawiera wydzielony tekst
            # usuwanie znacznikow html
            tekst = usuntagi(tekst)
            # podmienianie odpowiednich znacznikow w srodku tekstu
            tekst = tekst.replace('&nbsp;', '')
            tekst = tekst.replace('&lt;', '<')
            tekst = tekst.replace('&gt;', '>')
            # p - zawiera nowy paragraph
            p = Paragraph()
            # dodanie tytulu do paragraphu
            p.append(tekst)
            # dodanie paragrafu do sekcji
            section.append(p)
        i += 1
    return doc


def zapisz(nazwa):
    """Funkcja otwierajaca plik do zapisu.

    nazwa - zawiera nazwe pliku do zapisu
    """
    return file('%s.rtf' % nazwa, 'w')


if __name__ == '__main__':
    # DR - obiekt do zapisu
    # dokument - przechowuje utworzony dokument
    DR = Renderer()
    dokument = stworz()
    # zapis dokumentu do pliku
    DR.Write(dokument, zapisz('wynik'))
