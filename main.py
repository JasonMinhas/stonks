import pandas as pd
import general_functions as gf
import datetime as dt
import os
import helper_classes_and_functions as sc
import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator,
                               FormatStrFormatter,
                               AutoMinorLocator)


def main():
    ticker = 'SPY'
    start_date = dt.date(2021, 1, 1)
    end_date = dt.date(2023, 12, 21)
    number_of_days_to_remove = 5

    original_scn, best_x_days_removed_scn = generate_scenarios(ticker, start_date, end_date, number_of_days_to_remove)
    visualize_stock_df(original_scn, best_x_days_removed_scn)


def generate_scenarios(ticker, start_date, end_date, number_of_days_to_remove):
    original_scn = sc.StockData(ticker, start_date, end_date)
    best_x_days_removed_scn = sc.StockData(ticker, start_date, end_date).remove_best_x_days(number_of_days_to_remove)

    return original_scn, best_x_days_removed_scn


def visualize_stock_df(original_scn, best_x_days_removed_scn):
    # define series to be plotted
    y_og_close_line = original_scn.stock_df['close']
    y_scn_close_line = best_x_days_removed_scn.stock_df['close'] #todo add circle label markers for the best X days
    x = original_scn.stock_df['date']
    number_of_days_removed = best_x_days_removed_scn.best_x_indices.size

    fig, (close_line_ax, table_ax) = plt.subplots(nrows=2, ncols=1, figsize=(14, 8),
                                                  gridspec_kw={'height_ratios': [2, 1]})

    # add title
    fig.suptitle(
        f'{original_scn.ticker} comparison between original Close and missing the best {number_of_days_removed} '
        f'return days removed for a {original_scn.periods_year} year period',
        fontsize=16)

    # assign plot lines
    og_line = close_line_ax.plot(x, y_og_close_line, label='Original', zorder=3)
    scn_line = close_line_ax.plot(x, y_scn_close_line, label=f'Missing Best {number_of_days_removed} Days', zorder=2)

    # set baseline bbox_to_anchor values
    bbox_to_anchor_value = (1, 1)

    # add legends
    og_legend = close_line_ax.legend(handles=og_line, bbox_to_anchor=[bbox_to_anchor_value[0], bbox_to_anchor_value[1]], loc='upper left')
    close_line_ax.add_artist(og_legend)
    close_line_ax.legend(handles=scn_line, bbox_to_anchor=[bbox_to_anchor_value[0], bbox_to_anchor_value[1]-.5], loc='upper left')

    # define font dict for labels
    font1 = {'color': 'dimgray', 'size': 13}

    # format y axis label to currency
    close_line_ax.yaxis.set_major_formatter('${x:1.0f}')
    close_line_ax.set_ylabel("Closing Price", fontdict=font1)

    # label axis
    close_line_ax.set_xlabel("Date", fontdict=font1)

    # annotate starting price
    close_line_ax.annotate('$'+'%0.2f' % y_og_close_line.iloc[0], xy=(0, y_og_close_line.iloc[0]), xytext=(8, 0),
                 xycoords=('axes fraction', 'data'), textcoords='offset points')

    # add text for both close prices
    close_line_ax.text(
        bbox_to_anchor_value[0]+.01, bbox_to_anchor_value[1]-.15,
        f"Last Close: ${'%0.2f' % y_og_close_line.iloc[-1]}", transform=close_line_ax.transAxes)
    close_line_ax.text(
        bbox_to_anchor_value[0]+.01, bbox_to_anchor_value[1]-.65,
        f"Last Close: ${'%0.2f' % y_scn_close_line.iloc[-1]}", transform=close_line_ax.transAxes)

    # add text for both annualized return percent
    close_line_ax.text(bbox_to_anchor_value[0]+.01, bbox_to_anchor_value[1]-.22,
                       f"Annualized Return %: {format(original_scn.annualized_return_pct, '.2%')}",
                       transform=close_line_ax.transAxes)
    close_line_ax.text(bbox_to_anchor_value[0]+.01, bbox_to_anchor_value[1]-.72,
                       f"Annualized Return %: {format(best_x_days_removed_scn.annualized_return_pct, '.2%')}",
                       transform=close_line_ax.transAxes)

    # format table axis
    # remove axis for table visual
    table_ax.axis("off")

    # add title
    table_ax.set_title(f'Best performing {number_of_days_removed} days')
    best_x_days_removed_df = original_scn.stock_df.loc[
        best_x_days_removed_scn.best_x_indices,
        ['date', 'close', 'return_pct_vs_prev_day']
    ].sort_values(by='date', ascending=False)
    # format close price and return pct
    best_x_days_removed_df['close'] = best_x_days_removed_df['close'].apply(lambda x: f"${x:1.2f}")
    best_x_days_removed_df['return_pct_vs_prev_day'] = best_x_days_removed_df['return_pct_vs_prev_day'].apply(lambda x: '{:.2%}'.format(x))

    cell_text = []
    for index, row in best_x_days_removed_df[['date', 'close', 'return_pct_vs_prev_day']].iterrows():
        cell_text.append([x for x in row])
    col_labels = ['Date', 'Close Price', 'Daily Return % Vs Previous Day']
    table_ax.table(cellText=cell_text,
                   colLabels=col_labels,
                   loc='center',
                   zorder=1
                   )

    # highlight difference between or and scn via verticle line
    x = original_scn.stock_df.loc[best_x_days_removed_scn.best_x_indices, 'date']
    ymin = best_x_days_removed_scn.stock_df.loc[best_x_days_removed_scn.best_x_indices, 'close']
    ymax = original_scn.stock_df.loc[best_x_days_removed_scn.best_x_indices, 'close']
    close_line_ax.vlines(x=x, ymin=ymin, ymax=ymax,
               colors='red',
               label='vline_multiple - partial height')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
