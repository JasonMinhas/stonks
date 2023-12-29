import pandas as pd
import general_functions as gf
import datetime as dt
import os
import helper_classes_and_functions as sc
import yfinance as yf
import matplotlib.pyplot as plt


def main():
    StockData = sc.StockData(
        'SPY',
        dt.date(2008, 1, 1),
        dt.date(2023, 12, 21)
    )
    scenario1 = sc.StockSimulator(StockData)

    run_scenario(StockData)
    visualize_stock_df(StockData)


def run_scenario(StockData):
    StockData.get_close_series_with_best_x_days_removed(10)

    # original return calculations
    StockData.return_pct = StockData.get_return_pct()
    StockData.annualized_return_pct = (1 + StockData.return_pct) ** (1 / StockData.periods_year) - 1

    # alternative return calculations
    StockData.alt_return_pct = StockData.get_alt_return_pct()
    StockData.alt_annualized_return_pct = (1 + StockData.alt_return_pct) ** (1 / StockData.periods_year) - 1


def visualize_stock_df(StockData):
    # define series to be plotted
    y_close_line = StockData.stock_df['close']
    y_alt_close_line = StockData.alt_stock_df['alt_close']
    x = StockData.stock_df['date']

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
    plt.annotate(format(StockData.annualized_return_pct, ".2%"), xy=(1, y_close_line.iloc[-1]), xytext=(8, -28),
                 xycoords=('axes fraction', 'data'), textcoords='offset points')
    # annotate alt annualized close price
    plt.annotate(format(StockData.alt_annualized_return_pct, ".2%"), xy=(1, y_alt_close_line.iloc[-1]), xytext=(8, -28),
                 xycoords=('axes fraction', 'data'), textcoords='offset points')

    # todo highlight all the mismatch days. Show marker and percent label
    plt.show()


if __name__ == "__main__":
    main()
