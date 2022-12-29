import pandas as pd
from datetime import timedelta, datetime
import matplotlib.pyplot as plt


if __name__ == '__main__':
    df1 = pd.read_csv("Plant_1_Generation_Data.csv", parse_dates=['DATE_TIME'])  # header=0 default
    df2 = pd.read_csv("Plant_2_Generation_Data.csv", parse_dates=['DATE_TIME'])
    df = pd.concat([df1, df2])  # łączenie 2 plantów

    df = df.dropna().reset_index(drop=True)  # usuwanie NaN i Null + reset indeksow

    # plot AC_POWER dla wybranego generatora w wybranym tygodniu

    start_date = datetime(2020, 5, 15)
    end_date = start_date + timedelta(weeks=1)

    df_week = df[(df['DATE_TIME'] >= start_date) & (df['DATE_TIME'] <= end_date)]  # df dla 1 tygodnia
    df_week = df_week.loc[df['PLANT_ID'] == 4135001]  # dla generatora 4135001

    df_plot = df_week.plot(x='DATE_TIME', y='AC_POWER')

    # obliczanie sredniej dla obu generatorow

    df_gen1 = df.loc[df['PLANT_ID'] == 4135001]
    df_gen2 = df.loc[df['PLANT_ID'] == 4136001]

    gen1_mean = df_gen1.AC_POWER.mean()
    gen2_mean = df_gen2.AC_POWER.mean()

    df_plot.hlines(y=gen1_mean, xmin=start_date, xmax=end_date, color='purple', label='Plant 1')
    df_plot.hlines(y=gen2_mean, xmin=start_date, xmax=end_date, color='red', label='Plant 2')

    df_plot.legend()
    plt.show()

    # przypadki, kiedy AC_POWER któregoś z generatorów było na poziomie < 80% średniej

    df_compare_to_mean1 = df_gen1[(df_gen1['AC_POWER'] <= gen1_mean*0.8)]
    df_compare_to_mean2 = df_gen2[(df_gen2['AC_POWER'] <= gen2_mean*0.8)]

    print("--- AC_POWER generatora 2 jest częściej na poziomie < 80% średniej ---")
    print("Plant 1: AC_POWER < 80% średniej: ", round(df_compare_to_mean1.size / df_gen1.size * 100, 2), "% czasu")
    print("Plant 2: AC_POWER < 80% średniej: ", round(df_compare_to_mean2.size / df_gen2.size * 100, 2), "% czasu")