from itertools import combinations

import matplotlib.pyplot as plt
import miary_statystyczne
import pandas as pd


def main():
    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.titlesize": 14,
            "axes.labelsize": 12,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
        }
    )

    df = pd.read_csv(
        "data1.csv",
        header=None,
        names=[
            "Długość działki kielicha",
            "Szerokość działki kielicha",
            "Długość płatka",
            "Szerokość płatka",
            "Gatunek",
        ],
    )

    df["Gatunek"] = df["Gatunek"].map(
        {
            0: "setosa",
            1: "versicolor",
            2: "virginica",
        }
    )

    print(df["Gatunek"].value_counts())

    dane = [
        "Długość działki kielicha",
        "Szerokość działki kielicha",
        "Długość płatka",
        "Szerokość płatka",
    ]

    baza = pd.DataFrame(
        index=dane,
        columns=[
            "Minimum",
            "Śr. arytm. (± odch. stand.)",
            "Mediana (Q1 - Q3)",
            "Maksimum",
        ],
    )

    for x in baza.index:
        baza.loc[x] = [
            min(df[x]),
            f"{miary_statystyczne.srednia_arytmetyczna(df[x]):.2f} ± {miary_statystyczne.odchylenie_standardowe(df[x]):.2f}",
            f"{miary_statystyczne.mediana(df[x])} ({miary_statystyczne.kwartyle(df[x])})",
            max(df[x]),
        ]

    print(baza.to_markdown(tablefmt="grid"))

    fig, axes = plt.subplots(4, 2, figsize=(12, 14))

    for x in range(4):
        # Histogram
        axes[x][0].hist(df[dane[x]], bins=8, edgecolor="black")
        axes[x][0].set(
            title=dane[x],
            xlabel="Długość (cm)" if "Długość" in dane[x] else "Szerokość (cm)",
            ylabel="Liczebność",
        )

        # Boxplot
        df.boxplot(
            column=dane[x],
            by="Gatunek",
            ax=axes[x][1],
            grid=False,
            medianprops={"color": "gray"},
        )

        axes[x][1].grid(axis="y", alpha=0.35)

        axes[x][1].set(
            title="",
            xlabel="Gatunek",
            ylabel="Długość (cm)" if "Długość" in dane[x] else "Szerokość (cm)",
        )

    plt.suptitle("")
    plt.tight_layout(h_pad=2, w_pad=2)
    plt.show()

    # Wykresy punktowe i regresja liniowa
    fig, axes = plt.subplots(3, 2, figsize=(12, 14))

    for ax, (x, y) in zip(axes.flat, combinations(dane, 2)):
        a, b = miary_statystyczne.regresja_liniowa(df[x], df[y])

        ax.scatter(df[x], df[y], s=7, alpha=0.6)
        ax.plot(df[x], a * df[x] + b, color="red", linewidth=1.5)

        ax.set(
            xlabel=x,
            ylabel=y,
            title=f"r = {miary_statystyczne.pearson(df[x], df[y]):.2f}; y = {a:.2f}x {b:+.2f}",
        )

    plt.tight_layout(h_pad=2.5, w_pad=2.5)
    plt.show()


if __name__ == "__main__":
    main()
