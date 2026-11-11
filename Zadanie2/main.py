import random
from itertools import combinations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

kolumny = ["długość działki kielicha", "szerokość działki kielicha", "długość płatka", "szerokość płatka"]

df = pd.read_csv('data2.csv', header=None, names=kolumny)
df = (df - df.min()) / (df.max() - df.min())

klaster = pd.Series()

liczba_klastrow = int(input("Podaj liczbe klastrów mistrzu: "))

if liczba_klastrow <= 0:
    raise ValueError(f"Liczba klastrów musi być większa niż 0, a podałeś {liczba_klastrow}!")
elif liczba_klastrow > len(df):
    raise ValueError("Liczba klastrów nie może być większa niż liczba punktów na wykresie!")

for x, y in combinations(kolumny, 2):
    centroidy = []
    iteracje = 0

    for i in random.sample(range(len(df)), liczba_klastrow):
        centroidy.append((df[x].iloc[i], df[y].iloc[i]))

    while(True):
        iteracje += 1
        WCSS = 0

        klastry_x = [0] * liczba_klastrow
        klastry_y = [0] * liczba_klastrow
        liczebnosc = [0] * liczba_klastrow


        for i in df.index:
            odlegolsc = []

            for j in range(liczba_klastrow):
                odlegolsc.append((df.loc[i, x] - centroidy[j][0]) ** 2 + (df.loc[i, y] - centroidy[j][1]) ** 2)

            klaster[i] = odlegolsc.index(min(odlegolsc))
            WCSS += min(odlegolsc)

            klastry_x[klaster[i]] += df.loc[i, x]
            klastry_y[klaster[i]] += df.loc[i, y]

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

            sns.scatterplot(df, x=df[x], y=df[y], hue=klaster, legend=False, palette="viridis")

            for cx, cy in centroidy:
                plt.scatter(cx, cy, marker="X", s=100, c="red", edgecolors="black", zorder=999)
            plt.show()
            break

        centroidy = nowe
