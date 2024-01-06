import pandas as pd
import general_functions as gf
import datetime as dt
import os
import helper_classes_and_functions as sc
import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.offsetbox import (AnnotationBbox, DrawingArea, OffsetImage, TextArea)


def main():
    ticker = 'SPY'
    start_date = dt.date(2010, 1, 1)
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
    number_of_days_removed = best_x_days_removed_scn.best_x_indices.size

    fig, ax = plt.subplots(figsize=(12, 5))

    # assign plot lines and add legend
    og_line = plt.plot(x, y_og_close_line, label='Original')
    scn_line = plt.plot(x, y_scn_close_line, label=f'Missing Best {number_of_days_removed} Days')
    og_legend = plt.legend(handles=og_line, bbox_to_anchor=[1, 1], loc='upper left')
    plt.gca().add_artist(og_legend)
    plt.legend(handles=scn_line, bbox_to_anchor=[1, .5], loc='upper left')

    # define font dict for labels
    font1 = {'color': 'dimgray', 'size': 13}

    # format y axis label to currency
    ax.yaxis.set_major_formatter('${x:1.0f}')
    plt.ylabel("Closing Price", fontdict=font1)

    # label axis
    plt.xlabel("Date", fontdict=font1)

    # add title
    plt.title(
        f'{original_scn.ticker} comparison between original Close and missing the best {number_of_days_removed} return days removed for a {original_scn.periods_year} year period')

    # annotate starting price
    plt.annotate('$'+'%0.2f' % y_og_close_line.iloc[0], xy=(0, y_og_close_line.iloc[0]), xytext=(8, 0),
                 xycoords=('axes fraction', 'data'), textcoords='offset points')

    # add text for both close prices
    plt.text(1.01, .875, f"Last Close: ${'%0.2f' % y_og_close_line.iloc[-1]}", transform=ax.transAxes)
    plt.text(1.01, .375, f"Last Close: ${'%0.2f' % y_scn_close_line.iloc[-1]}", transform=ax.transAxes)


    # add text for both annualized return percent
    plt.text(1.01, .825, f"Annualized Return %: {format(original_scn.annualized_return_pct, '.2%')}",
             transform=ax.transAxes)
    plt.text(1.01, .325, f"Annualized Return %: {format(best_x_days_removed_scn.annualized_return_pct, '.2%')}",
             transform=ax.transAxes)

    # todo highlight all the mismatch days. Show marker and percent label
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()
