import random
from itertools import combinations

import pandas as pd

kolumny = ["długość działki kielicha", "szerokość działki kielicha", "długość płatka", "szerokość płatka"]

df = pd.read_csv('data2.csv', header=None, names=kolumny)

wynik = []

liczba_klastrow = int(input("Podaj liczbe klastrów mistrzu: "))
if liczba_klastrow <= 0:
    raise ValueError(f"Liczba klastrów musi być większa niż 0, a podałeś {liczba_klastrow}!")

def center_init(minimum, maksimum):
    return random.uniform(minimum, maksimum)

for x, y in combinations(kolumny, 2):
    centroidy = []

    maksimum_x = df[x].max()
    minimum_x = df[x].min()

    maksimum_y = df[y].max()
    minimum_y = df[y].min()

    for i in range (liczba_klastrow):
        centroidy.append((center_init(maksimum_x, minimum_x), center_init(maksimum_y, minimum_y)))

    dupa = pd.DataFrame({
        x: df[x],
        y: df[y],
        "klaster": None,
    })

    while (True):

        klastry_x = []
        klastry_y = []
        liczebnosc = []
        WCSS = 0

        for i in range(liczba_klastrow):
            klastry_x.append(0)
            klastry_y.append(0)
            liczebnosc.append(0)


        for i in dupa.index:
            odlegolsc = []

            for j in range(liczba_klastrow):
                odlegolsc.append((dupa.loc[i, x] - centroidy[j][0]) ** 2 + (dupa.loc[i, y] - centroidy[j][1]) ** 2)

            dupa.loc[i, "klaster"] = odlegolsc.index(min(odlegolsc))
            WCSS += min(odlegolsc)

            klastry_x[odlegolsc.index(min(odlegolsc))] += dupa.loc[i, x]
            klastry_y[odlegolsc.index(min(odlegolsc))] += dupa.loc[i, y]

            liczebnosc[odlegolsc.index(min(odlegolsc))] += 1

        nowe = []

        for i in range(liczba_klastrow):
            if liczebnosc[i] == 0:
                nowe.append(centroidy[i])
            else:
                nowe.append((
                    klastry_x[i] / liczebnosc[i],
                    klastry_y[i] / liczebnosc[i],
                ))

        if centroidy == nowe:
            print(f"WCSS: {WCSS}\n")
            break

        centroidy = nowe

    wynik.append(dupa)

print(wynik)