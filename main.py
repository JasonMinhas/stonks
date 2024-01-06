import pandas as pd
import general_functions as gf
import datetime as dt
import os
import helper_classes_and_functions as sc
import yfinance as yf
import matplotlib.pyplot as plt
from ipywidgets import interact
import ipywidgets as widgets


def main():
    ticker = 'SPY'
    start_date = dt.date(2008, 1, 1)
    end_date = dt.date(2023, 12, 21)
    number_of_days_to_remove = 10

    original_scn, best_x_days_removed_scn = generate_scenarios(ticker, start_date, end_date, number_of_days_to_remove)
    visualize_stock_df(original_scn, best_x_days_removed_scn)


def generate_scenarios(ticker, start_date, end_date, number_of_days_to_remove):
    original_scn = sc.StockData(ticker, start_date, end_date)
    best_x_days_removed_scn = sc.StockData(ticker, start_date, end_date).remove_best_x_days(number_of_days_to_remove)

    return original_scn, best_x_days_removed_scn


def visualize_stock_df(original_scn, best_x_days_removed_scn):
    # define series to be plotted
    y_og_close_line = original_scn.stock_df['close']
    y_scn_close_line = best_x_days_removed_scn.stock_df['close']
    x = original_scn.stock_df['date']

    # assign plot lines
    plt.plot(x, y_og_close_line)
    plt.plot(x, y_scn_close_line)

    # todo format y axis label to currency

    # add title
    plt.title(
        f'{original_scn.ticker} comparison between original Close and missing the best {best_x_days_removed_scn.best_x_indices.size} return days removed for a {original_scn.periods_year} year period')

    # annotate starting price
    plt.annotate('$'+'%0.2f' % y_og_close_line.iloc[0], xy=(0, y_og_close_line.iloc[0]), xytext=(8, 0),
                 xycoords=('axes fraction', 'data'), textcoords='offset points')\

    # annotate close and alt close price
    for var in (y_og_close_line, y_scn_close_line):
        plt.annotate('$'+'%0.2f' % var.iloc[-1], xy=(1, var.iloc[-1]), xytext=(8, -15),
                     xycoords=('axes fraction', 'data'), textcoords='offset points')

    # todo add line key for original and scenario

    # todo format the labels to be more dynamic: if annualized return label are too close they will overlap
    # annotate original annualized close price
    plt.annotate(format(original_scn.annualized_return_pct, ".2%"), xy=(1, y_og_close_line.iloc[-1]), xytext=(8, -28),
                 xycoords=('axes fraction', 'data'), textcoords='offset points')
    # annotate alt annualized close price
    plt.annotate(format(best_x_days_removed_scn.annualized_return_pct, ".2%"), xy=(1, y_scn_close_line.iloc[-1]), xytext=(8, -28),
                 xycoords=('axes fraction', 'data'), textcoords='offset points')

    # todo highlight all the mismatch days. Show marker and percent label
    plt.show()


if __name__ == "__main__":
    main()
