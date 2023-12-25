import pandas as pd
import general_functions as gf
import datetime as dt
import os
import classes as sc
import yfinance as yf
import matplotlib.pyplot as plt


def main():
    hist_stock = sc.StockDataFrameClass("PATH")
    hist_stock = run_scenario(hist_stock)
    hist_stock = visualize_stock_df(hist_stock)


def run_scenario(hist_stock):
    hist_stock.add_column_for_best_x_days(5, hist_stock.start_date, hist_stock.end_date)

    return hist_stock


def visualize_stock_df(hist_stock):
    # define series to be plotted
    y_close_line = hist_stock.df['close']
    y_alt_close_line = hist_stock.df['alt_close']
    x = hist_stock.df['date']

    # assign plot lines
    plt.plot(x, y_close_line)
    plt.plot(x, y_alt_close_line)

    # add data labels for end prices
    for var in (y_close_line, y_alt_close_line):
        plt.annotate('$'+'%0.2f' % var.iloc[-1], xy=(1, var.iloc[-1]), xytext=(8, 0),
                     xycoords=('axes fraction', 'data'), textcoords='offset points')

    plt.annotate('$'+'%0.2f' % y_close_line.iloc[0], xy=(0, y_close_line.iloc[0]), xytext=(8, 8),
                 xycoords=('axes fraction', 'data'), textcoords='offset points')

    # todo highlight all the misatch days
    # todo add annualized return for both lines


    plt.show()


if __name__ == "__main__":
    main()
