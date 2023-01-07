import pandas as pd
from datetime import timedelta, datetime
import matplotlib.pyplot as plt

if __name__ == '__main__':
    df1 = pd.read_csv("Plant_1_Generation_Data.csv", parse_dates=['DATE_TIME'])  # header=0 default
    df2 = pd.read_csv("Plant_2_Generation_Data.csv", parse_dates=['DATE_TIME'])
    df = pd.concat([df1, df2])  # łączenie 2 plantów

    df = df.dropna().reset_index(drop=True)  # usuwanie NaN i Null + reset indeksow

    # wybor tygodnia + przykladowego generatora

    start_date = datetime(2020, 5, 15)
    end_date = start_date + timedelta(weeks=1)

    df_week = df[(df['DATE_TIME'] >= start_date) & (df['DATE_TIME'] <= end_date)]  # df dla 1 tygodnia
    df_week_single_gen = df_week.loc[df['SOURCE_KEY'] == 'oZZkBaNadn6DNKz']  # dla generatora oZZkBaNadn6DNKz

    # grupowanie po generatorach (source key) i czasie (date time)
    # obliczanie sredniej dla kazdego generatora w danym momencie
    df_week_mean_all_gen = df_week.groupby("DATE_TIME")['AC_POWER'].mean()

    ax = df_week_mean_all_gen.plot(x='DATE_TIME', y='AC_POWER', label="Mean value all")
    df_week_single_gen.plot(ax=ax, x='DATE_TIME', y='AC_POWER', color="orange", label="Sample")
    plt.title("Comparison (Sample vs. Sample generator)")
    plt.ylabel("AC-Power")
    plt.xlabel("Date")
    plt.legend()
    plt.show()

    # Znajdź przypadki, kiedy AC_POWER któregoś z generatorów było na poziomie < 80% średniej.
    # Których generatorów najczęściej to dotyczy?

    df_mean_all_gen = pd.DataFrame(df.groupby("DATE_TIME")['AC_POWER'].mean())
    df_mean_all_gen['DATE_TIME'] = df_mean_all_gen.index
    df_mean_all_gen['AC_POWER_80%'] = 0.8*df_mean_all_gen['AC_POWER']
    df_mean_all_gen.reset_index(drop=True, inplace=True)
    df_mean_all_gen.drop(['AC_POWER'], axis=1, inplace=True)
    df = df.merge(df_mean_all_gen, how = 'left', on='DATE_TIME')
    df_compare = df[(df['AC_POWER'] < df['AC_POWER_80%'])]

    print("Generatory które najczęściej wytwarzają energię poniżej 80% średniej:")
    print(df_compare.groupby("SOURCE_KEY").size().to_frame('size').sort_values(["size"], ascending=False))

    # Porównanie najsłabszego generatora ze średnią

    df_week_weak_gen = df_week.loc[df['SOURCE_KEY'] == 'Quc1TzYxW2pYoWX']  # dla generatora Quc1TzYxW2pYoWX
    ax = df_week_mean_all_gen.plot(x='DATE_TIME', y='AC_POWER', label="Mean value all")
    df_week_weak_gen.plot(ax=ax, x='DATE_TIME', y='AC_POWER', color="orange", label="Weak sample")

    plt.title("Comparison (Sample vs. Weakest Generator)")
    plt.ylabel("AC-Power")
    plt.xlabel("Date")
    plt.legend()
    plt.show()
