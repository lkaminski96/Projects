#Import bibliotek, gotowych metod/funkcji potrzebnych do realizacji tego zdania
from random import randint
from math import cos
from math import sin


class Branch:
    """Klasa reprezentujaca galaz.

    Zawiera punkt poczatkowy, punkt koncowy, dlugosc, grubosc,
    kolor galezi, kat nachylenia oraz poziom na ktorym znajduje sie dana galaz.
    """

#s - potrzebna do losowania losowych liczb z przedzialu w dalszej czesci kodu
#poziom - oznacza poziom naszego drzewa
#alpha - kat startowy dla drzewa
    s = 10
    poziom = 9
    alpha = 60

    def __init__(self, punkt1, punkt2, d, g, c, k, t):
        """Konstruktor klasy.

        Przyjmuje:
        punkt1 - punkt poczatkowy sciezki
        punkt2 - punkt koncowy sciezki/poczatkowy nastepnej
        d - dlugosc galezi
        g - grubosc galezi
        c - kolor galezi
        k - kat nachylenia galezi
        t - zmienna pomocnicza w oszacowywaniu poziomu
        """
        self.p1 = punkt1
        self.p2 = punkt2
        self.dlugosc = float(d)
        self.grubosc = g
        self.kolor = c
        self.kat = k
        self.tmp = t

    def __str__(self):
        """Przeciazenie metody str."""
        return (r'<path d="M {} {} L {} {} Z"'
                ' stroke="rgb(100,{},0)"'
                ' stroke-width="{}"/>').format(
                    self.p1[0], self.p1[1],
                    self.p2[0], self.p2[1], self.kolor, self.grubosc)

#glowna czesc zadania
    def podziel(self):
        """Metoda odpowiadajaca za fraktale.

        Metoda ta odpowiada ze zwrocenie fraktali.
        Przechodzi po wszystkich poziomach drzewa generujac fraktale przy pomocy
        metody fraktal() oraz dodatkowych obliczen ze wzorow podanych w zadaniu.
        Zwraca 3 fraktale jako obiekty typu Branch.
        """
        def fraktal(dlugosc, alpha, poziom):
            """Metoda wyznaczajaca fraktal.

            Metoda ta przyjmuje dlugosc, kat oraz poziom drzewa.
            Na bazie podanych parametrow wylicza fraktal z podanych w zadaniu wzorow.
            Zwraca liste zawierajaca punkX oraz punktY fraktalu.
            """
#obliczanie punktow punktu Abis dla kazdego poziomu galezi
            x = float(self.p2[0] + self.dlugosc * cos(alpha))
            y = float(self.p2[1] + self.dlugosc * sin(alpha))
            return [round(x), round(y)]

#petla przechodzaca po wszystkich poziomach drzewa
        while self.tmp <= self.poziom:
#obliczanie grubosci, dlugosci galezi oraz kolorowanie jej
            self.grubosc = float((2 * self.grubosc + 1) / 3)
            self.dlugosc = float((2 * self.dlugosc) / 3)
            self.kolor += 6

            #sprawdzenie czy kolor nie wyszedl po za skale maksymalnej wartosci
            if self.kolor > 255:
                self.kolor = 255

#rozbicie obliczen na poziom 1 i wyzej
#Abis jest to punkt prawy dla kazdej galezi
#B jest to punkt srodkowy dla kazdej galezi
#C jest to punkt srodkowy dla kazdej galezi

#obliczenia dla pierwszego poziomu
            if self.tmp < 2:
#obliczenie fraktalu, prawa galaz dla kazdej galezi
#podstawienie obliczonych wartosci z punktu Abis do pozostalych wedlug podanych wzorow
                Abis = fraktal(self.dlugosc, self.alpha, self.poziom)
                B = [round(self.p2[0]), round(Abis[1])]
                C = [round(-Abis[0] + 2 * self.p2[0]), round(Abis[1])]

#zwiekszenie poziomu drzewa o jeden
                self.tmp += 1

#tutaj nastepuje zwrocenie obiektow typu Branch z nowo obliczonymi wartosciami
                return [Branch(self.p2, Abis, self.dlugosc, self.grubosc, self.kolor, self.alpha, self.tmp),
                        Branch(self.p2, B, self.dlugosc, self.grubosc, self.kolor, self.alpha, self.tmp),
                        Branch(self.p2, C, self.dlugosc, self.grubosc, self.kolor, self.alpha, self.tmp)]
#obliczenia poziomow wyzej niz pierwszy
            else:
#obliczanie kata dla punktu prawego
                self.zetprim = randint(-1, 1) * randint(1, self.s)
                self.beta = self.alpha + self.zetprim

#obliczanie kata dla punktu srodkowego
                self.zetbis = randint(-1, 1) * randint(1, self.s)
                self.gamma = self.alpha + self.zetbis

#obliczanie kata dla punktu lewego
                self.zetter = randint(-1, 1) * randint(1, self.s)
                self.teta = self.alpha + self.zetter

#obliczenie fraktalu, prawa galaz dla kazdej galezi
#podstawienie obliczonych wartosci z punktu Abis do pozostalych wedlug podanych wzorow
                Abis = fraktal(self.dlugosc, self.beta, self.poziom)
                B = [round(self.p2[0]), round(Abis[1])]
                C = [round(-Abis[0] + 2 * self.p2[0]), round(Abis[1])]

#zwiekszenie poziomu drzewa o jeden
                self.tmp += 1

#tutaj nastepuje zwrocenie obiektow typu Branch z nowo obliczonymi wartosciami
                return [Branch(self.p2, Abis, self.dlugosc, self.grubosc, self.kolor, self.beta, self.tmp),
                        Branch(self.p2, B, self.dlugosc, self.grubosc, self.kolor, self.gamma, self.tmp),
                        Branch(self.p2, C, self.dlugosc, self.grubosc, self.kolor, self.teta, self.tmp)]

#utworzenie pnia - poczatkowej galezi dla drzewa
galezie = [Branch([450, 900], [450, 750], 150, 25, 60, 0, 0)]

plik = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 900" version="1.1">\n'''


def list_to_svg(galezie):
    """Funkcja generujaca liste nowo obliczonych galezi.

    Funckja dopisuje kazda wyliczona galaz w postaci lini zawierajacej
    sciezke z okreslonymi parametrami.
    """
    res = '\n'.join([str(g) for g in galezie])
    return res

#petla odpowiadajaca za przejscie po wszystkich poziomach
#dopisuje galezie otrzymane z funkcji list_to_svg
#tworzy nowe puste listy
#dla kazdej galezi wywoluje metode dzielaca na fraktale
#nadpisuje poprzednia liste obiektami otrzymanymi z metody
for i in range(10):
    plik = plik + list_to_svg(galezie) + '\n'
    nowe = []
    for g in galezie:
        nowe += g.podziel()
    galezie = nowe

plik = plik + '</svg>'
#zapis do pliku
with open('drzewo.svg', 'w') as f:
    f.write(plik)