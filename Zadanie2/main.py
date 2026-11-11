import random
import seaborn as sns
import matplotlib.pyplot as plt

from itertools import combinations

import pandas as pd

kolumny = ["długość działki kielicha", "szerokość działki kielicha", "długość płatka", "szerokość płatka"]

df = pd.read_csv('data2.csv', header=None, names=kolumny)
df = (df - df.min()) / (df.max() - df.min())

wynik = []

liczba_klastrow = int(input("Podaj liczbe klastrów mistrzu: "))

if liczba_klastrow <= 0:
    raise ValueError(f"Liczba klastrów musi być większa niż 0, a podałeś {liczba_klastrow}!")


for x, y in combinations(kolumny, 2):
    centroidy = []
    iteracje = 0

    maksimum_x = df[x].max()
    minimum_x = df[x].min()

    maksimum_y = df[y].max()
    minimum_y = df[y].min()

    for i in range (liczba_klastrow):

        centroidy.append((
            random.randrange(0, 1),
            random.randrange(0, 1)
        ))

    dupa = pd.DataFrame({
        x: df[x],
        y: df[y],
        "klaster": None,
    })

    while (True):
        iteracje += 1

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
            klaster = 0

            for j in range(liczba_klastrow):
                odlegolsc.append((dupa.loc[i, x] - centroidy[j][0]) ** 2 + (dupa.loc[i, y] - centroidy[j][1]) ** 2)

            klaster = odlegolsc.index(min(odlegolsc))
            dupa.loc[i, "klaster"] = klaster
            WCSS += min(odlegolsc)

            klastry_x[klaster] += dupa.loc[i, x]
            klastry_y[klaster] += dupa.loc[i, y]

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
            print(f"WCSS: {WCSS}\n"
                  f"Liczba iteracji: {iteracje}\n")

            sns.scatterplot(df, x=df[x], y=df[y], hue=dupa["klaster"], legend=False, palette="viridis")

            for cx, cy in centroidy:
                plt.scatter(cx, cy, marker="X", s=100, c="red", edgecolors="black", zorder=10)

            plt.show()
            break

        centroidy = nowe

    wynik.append(dupa)

print(wynik)