from dataclasses import dataclass, field
import datetime as dt
import pandas as pd
import general_functions as gf
import yfinance as yf
from dateutil.relativedelta import relativedelta
from typing import Optional

def get_stock_data(ticker):
    stock_ticker = yf.Ticker(ticker)
    hist_stock_df = stock_ticker.history(period="max")

    return hist_stock_df


def clean_stock_data(hist_stock_df):
    hist_stock_df = hist_stock_df.reset_index()
    hist_stock_df = gf.clean_headers(hist_stock_df)
    hist_stock_df = gf.strip_df(hist_stock_df)
    hist_stock_df['date'] = pd.to_datetime(hist_stock_df['date']).dt.date

    return hist_stock_df


@dataclass
class StockData():
    ticker: str
    start_date: str
    end_date: str
    stock_df: Optional[pd.DataFrame] = None
    # todo property that identifies whether this is the orginal data or it has been changed

    def periods_year(self) -> int:
        return relativedelta(self.end_date, self.start_date).years

    # todo create a method that calculates return

    # todo create a method that calculates annualized return

    # todo create method to simulate skipping best x days

    def __post_init__(self):
        # convert dates to datetime
        self.start_date = dt.datetime.strptime(self.start_date, '%Y-%m-%d').date()
        self.end_date = dt.datetime.strptime(self.end_date, '%Y-%m-%d').date()

        # check if end date is after start date
        if self.periods_year() < 0:
            raise ValueError(f"The start_date argument, {self.start_date}, should be before the end_date argument, {self.end_date}")

        # get stock data
        stock_df = get_stock_data(self.ticker)
        stock_df = clean_stock_data(stock_df)
        self.stock_df = stock_df[
            (stock_df['date'] >= self.start_date)
            & (stock_df['date'] <= self.end_date)
        ]






stock1 = StockData('PATH', '2020-01-01', '2023-01-01')


print(stock1)


print('stop')