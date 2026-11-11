import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import math

from itertools import combinations

kolumny = ["długość działki kielicha", "szerokość działki kielicha", "długość płatka", "szerokość płatka"]

df = pd.read_csv('data2.csv', header=None, names=kolumny)

wynik = []

for x, y in combinations(kolumny, 2):
    center1 = (
        random.uniform(df[x].min(), df[x].max()),
        random.uniform(df[y].min(), df[y].max())
    )

    center2 = (
        random.uniform(df[x].min(), df[x].max()),
        random.uniform(df[y].min(), df[y].max())
    )

    center3 = (
        random.uniform(df[x].min(), df[x].max()),
        random.uniform(df[y].min(), df[y].max())
    )

    nowy_jeden = ()
    nowy_dwa = ()
    nowy_trzy = ()

    dupa = pd.DataFrame({
        x: df[x],
        y: df[y],
        "klaster": None,
    })

    while (True):

        klastryx = [0, 0, 0]
        klastryy = [0, 0, 0]
        liczebnosc = [0, 0, 0]

        for i in dupa.index:
            odlegolsc = []

            odlegolsc.append((dupa.loc[i, x] - center1[0]) ** 2 + (dupa.loc[i, y] - center1[1]) ** 2)
            odlegolsc.append((dupa.loc[i, x] - center2[0]) ** 2 + (dupa.loc[i, y] - center2[1]) ** 2)
            odlegolsc.append((dupa.loc[i, x] - center3[0]) ** 2 + (dupa.loc[i, y] - center3[1]) ** 2)

            dupa.loc[i, "klaster"] = odlegolsc.index(min(odlegolsc))

            klastryx[odlegolsc.index(min(odlegolsc))] += dupa.loc[i, x]
            klastryy[odlegolsc.index(min(odlegolsc))] += dupa.loc[i, y]

            liczebnosc[odlegolsc.index(min(odlegolsc))] += 1

        if liczebnosc[0] == 0:
            nowy_jeden = center1
        else:
            nowy_jeden = (
                klastryx[0] / liczebnosc[0],
                klastryy[0] / liczebnosc[0],
            )

        if liczebnosc[1] == 0:
            nowy_dwa = center2
        else:
            nowy_dwa = (
                klastryx[1] / liczebnosc[1],
                klastryy[1] / liczebnosc[1],
            )

        if liczebnosc[2] == 0:
            nowy_trzy = center3
        else:
            nowy_trzy = (
                klastryx[2] / liczebnosc[2],
                klastryy[2] / liczebnosc[2],
            )

        if center1 == nowy_jeden and center2 == nowy_dwa and center3 == nowy_trzy:
            break

        center1 = nowy_jeden
        center2 = nowy_dwa
        center3 = nowy_trzy

    wynik.append(dupa)

print(wynik)