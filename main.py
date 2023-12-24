import pandas as pd
import general_functions as gf
import datetime as dt
import os
import classes as sc
import yfinance as yf
import matplotlib.pyplot as plt


def main():
    hist_stock = sc.StockDataFrameClass("SPY")
    hist_stock = run_scenario(hist_stock)
    hist_stock = visualize_stock_df(hist_stock)


def run_scenario(hist_stock):
    hist_stock.add_column_for_best_x_days(10, '2008-01-02', '2023-12-21')

    return hist_stock


def visualize_stock_df(hist_stock):
    hist_stock.df.plot.line(y=['close', 'alt_close'])
    plt.show()


if __name__ == "__main__":
    main()
