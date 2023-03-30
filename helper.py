import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import hvplot.pandas
import numpy as np

def wrangle_dataframe(df, name):

    # filter Year >= 1990
    df = df[df.Year >= 1990]

    # drom column "Code" with loc
    df = df.loc[:, df.columns != 'Code']

    # rename column Entity to Country
    df.rename(columns = {'Entity': 'Country'}, inplace = True)

    # filter Countries: Switzerland, Spain, Germany, UK
    df = df[df.Country.isin(['Switzerland', 'Spain', 'Germany', 'United Kingdom'])]

    # reset index
    df.reset_index(drop = True, inplace = True)

    df_pivot = df.pivot(index = 'Year', columns = 'Country', values = name)
    df_pivot.head()

    return df


def add_growth_columns(df, new_col_absolute, new_col_percent, growth_col):

    # add new columns with difference and percentage change
    df[new_col_absolute] = df[growth_col].diff().round(3)
    df[new_col_percent] = df[growth_col].pct_change().round(3) * 100

    # if year is 1990, set growth to 0 (there is no previous year)
    df.loc[df.Year == 1990, new_col_absolute] = 0
    df.loc[df.Year == 1990, new_col_percent] = 0

    # replace NaN with 0
    df.fillna(0, inplace = True)

    # replace inf with 0
    df.replace([np.inf, -np.inf], 0, inplace = True)

    return df


def lineplot(df, x_var, y_var, by_var, title_var, width = 700, height = 400):
    plot = df.hvplot.line(x = x_var, y = y_var, by = by_var, width = width, height = height)
    plot.opts(title = title_var)
    display(plot)