import pandas as pd
import general_functions as gf
import yfinance as yf
from dateutil.relativedelta import relativedelta
from dataclasses import dataclass


def get_data(ticker):
    stock_ticker = yf.Ticker(ticker)
    hist_stock_df = stock_ticker.history(period="max")

    return hist_stock_df


def clean_stock_data(hist_stock_df):
    hist_stock_df = hist_stock_df.reset_index()
    hist_stock_df = gf.clean_headers(hist_stock_df)
    hist_stock_df = gf.strip_df(hist_stock_df)
    hist_stock_df['date'] = hist_stock_df['date'].apply(lambda x: pd.to_datetime(x))

    return hist_stock_df


class StockDataFrameClass:
    def __init__(self, ticker):
        self.df = clean_stock_data(get_data(ticker))
        self.start_date = min(self.df['date'])
        self.end_date = max(self.df['date'])

    def get_year_periods(self):
        year_periods = relativedelta(self.end_date, self.start_date).years

        return year_periods

    def calculate_return(self, close_or_clt_close, start_date, end_date):
        # filter for relevant timeframe
        temp_df = self.df[(self.df['date'] >= start_date) & (self.df['date'] <= end_date)]
        # take only first and last row which would be the min and max date
        temp_df = temp_df.iloc[[0, -1]]
        # find percentage difference between the min and max date
        return_pct = temp_df[close_or_clt_close].pct_change().iloc[-1]

        return return_pct

    def add_column_for_best_x_days(self, number_of_days_to_remove, start_date, end_date):
        # filter for relevant timeframe
        temp_df = self.df[(self.df['date'] >= start_date) & (self.df['date'] <= end_date)].copy(deep=True)
        # create new series for the percent change between all the rows
        temp_df['pct_returns_vs_prev_day'] = temp_df['close'].pct_change().fillna(0)
        temp_df['pct_alternate_returns_vs_prev_day'] = temp_df['pct_returns_vs_prev_day']
        # Get indices of top x rows
        top_x_indices = temp_df.nlargest(number_of_days_to_remove, 'pct_returns_vs_prev_day').index
        # replace top x indices with 0 and store in alternate series
        temp_df['pct_alt_returns_vs_prev_day'] = temp_df['pct_returns_vs_prev_day']
        temp_df.loc[top_x_indices, 'pct_alt_returns_vs_prev_day'] = 0

        # calculate alternate close price
        temp_value = temp_df.iloc[0]['close']
        for index, row in temp_df.iterrows():
            alt_return_pct = row['pct_alt_returns_vs_prev_day']
            temp_value = temp_value + (temp_value * alt_return_pct)
            temp_df.at[index, 'alt_close'] = temp_value

        # todo objective is to be able to insert multiple days. Create a veriable that names is based on date and days filter like this 'alt_df_1962-01-02_to_2023-12-22_remove_best_X'
        # todo is it best practice to iterate through and create multiple classes
        # https://medium.com/swlh/python-dataclasses-with-properties-and-pandas-5c59b05e9131
        self.df = temp_df


class StockData():
    ticker: str
    start_date: str
    end_date: str
    # todo add optional parameter to simulate skipping bext x days

    def periods_year(self) -> int:
        return self.end_date - self.start_date

    # todo create a method that calculates return

    # todo create a method that calculates annualized return

    # todo create method to simulate skipping best x days

    def __init__(self, ticker: str, start_date: str, end_date: str):
        self.ticker = ticker
        self.start_date = start_date  # todo turn to datetime
        self.end_date = end_date  # todo turn to datetime


@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand


def __init__(self, name: str, unit_price: float, quantity_on_hand: int = 0):
    self.name = name
    self.unit_price = unit_price
    self.quantity_on_hand = quantity_on_hand
