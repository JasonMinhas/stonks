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
    visualize_stock_df(hist_stock)


def run_scenario(hist_stock):
    # todo I want to be able to just enter the date in as a simple 'YYYY-MM-DD' format
    # hist_stock.start_date = dt.datetime(2008, 1, 1).astimezone()
    # hist_stock.end_date = dt.datetime(2023, 12, 21).astimezone()

    hist_stock.add_column_for_best_x_days(10, hist_stock.start_date, hist_stock.end_date)
    hist_stock.year_periods = hist_stock.get_year_periods()

    # original return calculations
    hist_stock.return_pct = hist_stock.calculate_return('close', hist_stock.start_date, hist_stock.end_date)
    hist_stock.annualized_return_pct = (1 + hist_stock.return_pct) ** (1 / hist_stock.year_periods) - 1

    # alternative return calculations
    hist_stock.alt_return_pct = hist_stock.calculate_return('alt_close', hist_stock.start_date, hist_stock.end_date)
    hist_stock.alt_annualized_return_pct = (1 + hist_stock.alt_return_pct) ** (1 / hist_stock.year_periods) - 1

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
    # annotate starting price
    plt.annotate('$'+'%0.2f' % y_close_line.iloc[0], xy=(0, y_close_line.iloc[0]), xytext=(8, 0),
                 xycoords=('axes fraction', 'data'), textcoords='offset points')\

    # annotate close and alt close price
    for var in (y_close_line, y_alt_close_line):
        plt.annotate('$'+'%0.2f' % var.iloc[-1], xy=(1, var.iloc[-1]), xytext=(8, -15),
                     xycoords=('axes fraction', 'data'), textcoords='offset points')

    # annotate annualized close price
    plt.annotate(format(hist_stock.annualized_return_pct, ".2%"), xy=(1, y_close_line.iloc[-1]), xytext=(8, -28),
                 xycoords=('axes fraction', 'data'), textcoords='offset points')
    # annotate alt annualized close price
    plt.annotate(format(hist_stock.alt_annualized_return_pct, ".2%"), xy=(1, y_alt_close_line.iloc[-1]), xytext=(8, -28),
                 xycoords=('axes fraction', 'data'), textcoords='offset points')

    # todo highlight all the mismatch days. Show marker and percent label
    plt.show()


if __name__ == "__main__":
    item = sc.InventoryItem('test', 10, 5)

    main()
