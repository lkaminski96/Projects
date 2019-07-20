
# import potrzebnych biobiotek matematycznych
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
   
def linear(dziedzina):
  """Funkcja interpolujaca Linear.
    
  dziedzina - dziedzina do interpolacji
  """
  # x - dziedzina funkcji glownej
  # y - przeciwdziedzina funkcji glownej
  # przeciwdziedzina - lista zawierajaca wartosci intepolacji
  x = np.arange(0, 10)
  y = np.sin(x)
  przeciwdziedzina = []
  for j in range(len(x) - 1):
    for i in range(len(dziedzina)):
      if(x[j] <= dziedzina[i]) & (dziedzina[i] < x[j + 1]):
      # y0 - wartosc funkcji dla x0
      # y1- wartosc funkcji dla x1
      # h - roznica w odleglosci miedzy x0 a x1
      # wynik - zawiera wartosc interpolacji dla konkretnego X
          y0 = y[j]
          y1 = y[j + 1]
          h = x[j + 1] - x[j]
          wynik = round(y0 + ((y1 - y0) / h) * (dziedzina[i] - x[j]), 8)
          przeciwdziedzina.append(wynik)
  return przeciwdziedzina
    
    
def lagrange(dziedzina):
  """Funkcja interpolujaca Lagrange.
    
  dziedzina - dziedzina do interpolacji
  """
  # x - dziedzina funkcji glownej
  # y - przeciwdziedzina funkcji glownej
  # przeciwdziedzina - lista zawierajaca wartosci intepolacji
  x = np.arange(0, 10)
  y = np.sin(x)
  przeciwdziedzina = []
  for k in range(len(dziedzina)):
      # wynik - zawiera wartosc interpolacji dla konkretnego X
      wynik = 0
      for i in range(len(y)):
         # czesc - zawiera wartosc czesciowego obliczenia mnozen X
         czesc = 1
         for j in range(len(x)):
           if i == j:
             continue
           # policzenie mnozen\n",
           czesc = czesc * ((dziedzina[k] - x[j]) / float(x[i] - x[j]))
           # wymnozenie obliczonego mnozenia z wartoscia funkcji dla x 
         czesc = czesc * y[i]
         wynik += czesc
      przeciwdziedzina.append(wynik)
  return przeciwdziedzina
    
    
def nearest(dziedzina):
  """Funkcja interpolujaca Nearest.
    
  dziedzina - dziedzina do interpolacji
  """
  # x - dziedzina funkcji glownej
  # y - przeciwdziedzina funkcji glownej
  # przeciwdziedzina - lista zawierajaca wartosci intepolacji
  x = np.arange(0, 10)
  y = np.sin(x)
  przeciwdziedzina = []
  # i - zmienna pomocnicza do iterowania po dziedzinie i przeciwdziedzinie
  i = 0
  for k in range(len(dziedzina)):
    #przyblizenie wartosci 
    dziedzina[k] = round(dziedzina[k], 1)
    # spawdzam czy index osiagnal maksymalna wartosc
    if i == (len(x) - 1):
      przeciwdziedzina.append(y[i])
      continue
    else:
     # polowa zawiera informacje o polowie odcinka dzielacego dwa punkty
      polowa = round(float(x[i + 1] + x[i]) / 2, 1)
      # sprawdzam czy polowa jest wieksza od biezacego X branego do wyliczenia wartosci przyblizenia
      if polowa >= dziedzina[k]:
        przeciwdziedzina.append(y[i])
      else:
        i += 1
        przeciwdziedzina.append(y[i])
  return przeciwdziedzina


def zero(dziedzina):
  """Funkcja interpolujaca Zero.
  
  dziedzina - dziedzina do interpolacji
  """
  # x - dziedzina funkcji glownej
  # y - przeciwdziedzina funkcji glownej
  # przeciwdziedzina - lista zawierajaca wartosci intepolacji
  x = np.arange(0, 10)
  y = np.sin(x)
  przeciwdziedzina = []
  # i - pomocnicza zmienna do operowania po X i Y dla funkcji glownej
  i = 0
  for k in range(len(dziedzina)):
  # sprawdzenie czy X z dziedziny do interpolacji zawiera sie w odpowiednim przedziale
    if(x[i] <= dziedzina[k]) & (dziedzina[k] < x[i + 1]):
      przeciwdziedzina.append(y[i])
    else:
      i = i + 1
      przeciwdziedzina.append(y[i])
  return przeciwdziedzina
    
#: x1- zawiera dziedzine do interpolacji
x = np.arange(0, 10)
y = np.sin(x)
x1 = np.arange(0, 9, 0.1)
    
#Interpolacje
#:lin - zawiera wartosci przyblizone dla interpolacji linear
lin = np.array(linear(x1))
#:lang - zawiera wartosci przyblizone dla interpolacji lagrange
lang = np.array(lagrange(x1))
#:zer - zawiera wartosci przyblizone dla interpolacji zero
zer = np.array(zero(x1))
#:near - zawiera wartosci przyblizone dla interpolacji nearest
near = np.array(nearest(x1))

# Wykres dla Punktow
plt.plot(x, y, label="punkty", color=(0.0, 0.0, 1.0), ls="", marker='o', markersize=(8))
    
# Wykres dla interpolacji Linear
plt.plot(x1, lin, label="linear", color=(1.0, 0.0, 0.0), linewidth=(1.5))
    
# Wykres dla interpolacji Lagrange
plt.plot(x1, lang, label="lagrange", color=(0.0, 0.0, 1.0), linewidth=(1.5))
    
# Wykres dla interpolacji Nearest
plt.plot(x1, near, label="nearest", color=(0.75, 0.75, 0.25), linewidth=(1.5))
    
# Wykres dla interpolacji Zero
plt.plot(x1, zer, label="zero", color=(0.25, 0.75, 0.75), linewidth=(1.5))
    
# ustawienie wartosci z dziedziny i przeciwdziedziny na osiach
plt.xticks(x)
    
# legenda
plt.legend(loc='lower left')
# napisy
plt.xlabel("Wartosci $\mathcal{X}$", fontsize="23")
plt.ylabel("Interpolacja wartosci $\mathcal{Y}$", fontsize="23")
# siatka
plt.grid(ls="solid", color=(0.7, 0.8, 1.0))
plt.show()