
def przelicz(liczbaS):
    """Funkcja przeliczajaca liczbe z systemu binarnego na dziesietny.
    
        Funkcja przyjmuje liczbe binarna zapisana jako typ string
        oraz zwraca liczbe dziesietna typu int.
        Przyklad:
        Wysylamy do funkcji liczbe typu string,
        znajdujaca sie w zmiennej liczbaS. Nastepnie konwertujemy
        pierwszy znak z typu string na int do zmiennej dziesietna.
        Pozniej podajemy system w jakim podalismy nasza liczbe.
        Dalej w petli w for przechodzimy po calej liczbie poczawszy
        od indeksu 1 az do dlugosci podanej liczby - 1.
        W petli for wykonujemy schemat Hornera, czyli dla kazdego obiegu
        petli wykonujemy dzialanie pomnozenia naszej aktualnej liczby z
        podstawa oraz dodanie kolejnej liczby przy czym nalezy zwrocic
        uwage na to ze dodawana liczba jest konwertowana z typu string na int.
        Na koniec zwracamy otrzymana liczbe dziesietna.
        Przyklad: liczbaS = '100001'
        dziesietna = 1
        podstawa = 2
        dlugosc podanej liczby = 6
        Iteracja pierwsza :
        dziesietna = 1 * 2 + 0 -> dziesietna = 2
        Iteracja druga :
        dziesietna = 2 * 2 + 0 -> dziesietna = 4
        Iteracja trzecia :
        dziesietna = 4 * 2 + 0 -> dziesietna = 8
        Iteracja czwarta :
        dziesietna = 8 * 2 + 0 -> dziesietna = 16
        Iteracja piata :
        dziesietna = 16 * 2 + 1 -> dziesietna = 33
        Wynik zwracany to 33.
    """
    
    #dziesietna - przechowuje liczbe juz po konwersji na typ int.
    #podstawa - przechowuje system w jakim jest podana dana liczba.
    dziesietna = int(liczbaS[0])
    podstawa = 2
    
    #glowna petla przeliczajaca z podanego systemu na system dziesietny.
    for i in range(1, len(liczbaS)):
        dziesietna = dziesietna * podstawa + int(liczbaS[i])
    return dziesietna
    
#otwieranie pliku liczby.txt oraz dzielenie pliku na linie metoda splitlines().
#odczyt - przechowywuje zawartosc pliku.
#linie - przechowuje liczby w postaci listy.
with open('liczby.txt', 'r') as f:
    odczyt = f.read()
linie = odczyt.splitlines()
    
#liczbaMax - przechowuje informacje odnosnie najwiekszej liczby z plik.
#liczbaMin - przechowuje informacje odnosnie najmniejszej liczby z pliku.
#indexMax - zawiera informacje o numerze wiersza najwiekszej liczby.
#indexMax - zawiera informacje o numerze wiersza najmniejszej liczby.
#przypisanie pierwszej liczby jako liczby zarowno MAX jak i MIN .
#przypisanie indeksu MAX dla pierwszej liczby jak i MIN.
liczbaMax = przelicz(linie[0])
liczbaMin = przelicz(linie[0])
indexMax = 1
indexMin = 1
    
#zmienne poczatkowe:
#ilosc - przechowuje informacje na temat ilosci liczb, ktore maja wiecej zer niz jedynek.
#podzielne2 - przechowuje informacje na temat ilosci liczb, ktore sa podzielne przez 2.
#podzielne8 - przechowuje informacje na temat ilosci liczb, ktore sa podzielne przez 8.
ilosc = 0
podzielne2 = 0
podzielne8 = 0
    
#glowna petla odpowiadajaca za przejscie po wszystkich elementach listy.
for i in range(1, len(linie)):
    
#zera - przechowuje informacje odnosnie ilosci zer dla konkretnej liczby z listy.
#jedynki - przechowuje informacje odnosnie ilosci jedynek dla konkretnej liczby z listy .
#binarna - zawiera liczbe w postaci binarnej typu string.
    zera = 0
    jedynki = 0
    binarna = linie[i]
    
#petla zliczajaca jedynki i zera dla kazdej z podanych liczb.
    for j in range(len(binarna)):
        if binarna[j]:
            jedynki += 1
        else:
            zera += 1
    if zera > jedynki:
        ilosc += 1
   
#liczba - zawiera liczbe w postaci dziesietnej typu int, zwrocona z funkcji przelicz().
    liczba = przelicz(binarna)
   
#sprawdzenie warunkow kolejno czy liczba jest podzielna przez 2.
#oraz czy liczba jest podzielna przez 8.
    if liczba % 2 == 0:
        podzielne2 += 1
    if liczba % 8 == 0:
        podzielne8 += 1
    
#sprawdzenie warunkow kolejno czy biezaca liczba jest.
#wieksza od dotychczasowej najwiekszej wraz z pobraniem wiersza oraz.
#czy biezaca liczba jest mniejsza od dotychczasowej.
    if liczba > liczbaMax:
       liczbaMax = liczba
       liczbaMaxB = binarna
       indexMax = i + 1
    if liczba < liczbaMin:
       liczbaMin = liczba
       liczbaMinB = binarna
       indexMin = i + 1
 
print "Odp.1 : Ilosc liczb, ktora zawiera wiecej zer niz jedynek jest", ilosc,
print "Odp.2 : Ilosc liczb podzielnych przez 2 wynosi: ", podzielne2,
print ". Ilosc liczb podzielnych przez 8 wynosi: ", podzielne8,
print "Odp.3 : Liczba najwieksza to ", liczbaMaxB, " numer wiersza to ", indexMax,
print ". Liczba najmniejsza to ", liczbaMinB, " numer wiersza to ", indexMin
   