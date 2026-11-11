import math
import sys


def srednia_arytmetyczna(zbior):
    if len(zbior) == 0:
        sys.exit("Błąd: pusty zbiór.")

    return sum(zbior) / len(zbior)


def odchylenie_standardowe(zbior):
    if len(zbior) < 2:
        sys.exit("Błąd: wymagane co najmniej 2 wartości.")

    srednia = srednia_arytmetyczna(zbior)
    wariancja = 0

    for x in zbior:
        wariancja += (x - srednia) ** 2

    wariancja /= len(zbior) - 1
    return math.sqrt(wariancja)


def mediana(zbior):
    if len(zbior) == 0:
        sys.exit("Błąd: pusty zbiór.")

    zbior = sorted(zbior)
    polowa = len(zbior) // 2

    if len(zbior) % 2 == 0:
        return (zbior[polowa] + zbior[polowa - 1]) / 2
    else:
        return zbior[polowa]


def kwartyle(zbior):
    if len(zbior) < 2:
        sys.exit("Błąd: wymagane co najmniej 2 wartości.")

    zbior = sorted(zbior)
    polowa = len(zbior) // 2

    q1 = mediana(zbior[:polowa])

    if len(zbior) % 2 == 0:
        q3 = mediana(zbior[polowa:])
    else:
        q3 = mediana(zbior[polowa + 1 :])

    return q1, q3


def kowariancja(zbior_a, zbior_b):
    if len(zbior_a) < 2 or len(zbior_b) < 2:
        sys.exit("Błąd: wymagane co najmniej 2 wartości.")

    if len(zbior_a) != len(zbior_b):
        sys.exit("Błąd: zbiory mają różne długości.")

    srednia_zbior_a = srednia_arytmetyczna(zbior_a)
    srednia_zbior_b = srednia_arytmetyczna(zbior_b)
    odchylenia = []

    for x, y in zip(zbior_a, zbior_b):
        x -= srednia_zbior_a
        y -= srednia_zbior_b
        odchylenia.append(x * y)

    return sum(odchylenia) / (len(odchylenia) - 1)


def pearson(zbior_a, zbior_b):
    if len(zbior_a) != len(zbior_b):
        sys.exit("Błąd: zbiory mają różne długości.")

    odchylenie_a = odchylenie_standardowe(zbior_a)
    odchylenie_b = odchylenie_standardowe(zbior_b)

    if odchylenie_a == 0 or odchylenie_b == 0:
        sys.exit("Błąd: zerowe odchylenie standardowe.")

    kowariancja_wynik = kowariancja(zbior_a, zbior_b)

    return kowariancja_wynik / (odchylenie_a * odchylenie_b)


def regresja_liniowa(zbior_a, zbior_b):
    if len(zbior_a) < 2 or len(zbior_b) < 2:
        sys.exit("Błąd: wymagane co najmniej 2 wartości.")

    if len(zbior_a) != len(zbior_b):
        sys.exit("Błąd: zbiory mają różne długości.")

    a_licznik = kowariancja(zbior_a, zbior_b)
    a_mianownik = 0
    x_srednia = srednia_arytmetyczna(zbior_a)

    for x in zbior_a:
        a_mianownik += (x - x_srednia) ** 2

    a_mianownik /= len(zbior_a) - 1

    if a_mianownik == 0:
        sys.exit("Błąd: zerowa wariancja X.")

    a = a_licznik / a_mianownik
    y_srednia = srednia_arytmetyczna(zbior_b)
    b = y_srednia - a * x_srednia

    return a, b
