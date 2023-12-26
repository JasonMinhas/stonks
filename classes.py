from dataclasses import dataclass
import datetime as dt
import pandas as pd
import general_functions as gf
import yfinance as yf
from dateutil.relativedelta import relativedelta
from typing import Optional

# todo look into creating a class and subclass hierarchy where the subclass hold the alternative values. It needs to be able to calculate return, annualized return

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
    start_date: dt.date
    end_date: dt.date
    stock_df: Optional[pd.DataFrame] = None

    def periods_year(self) -> int:
        return relativedelta(self.end_date, self.start_date).years

    # Calculate return percentage
    def get_return_pct(self) -> float:
        # take only first and last row which would be the min and max date
        first_and_last_rows = self.stock_df.iloc[[0, -1]]
        # find percentage difference between the min and max date
        return_pct = first_and_last_rows['close'].pct_change().iloc[-1]

        return return_pct

    # Calculate return percentage
    def get_alt_return_pct(self) -> float:
        # take only first and last row which would be the min and max date
        first_and_last_rows = self.alt_stock_df.iloc[[0, -1]]
        # find percentage difference between the min and max date
        return_pct = first_and_last_rows['alt_close'].pct_change().iloc[-1]

        return return_pct

    # Calculate annualized return percentage
    def get_annualized_return_pct(self, ) -> float:
        self.stock_df.annualized_return_pct = (1 + self.stock_df.return_pct) ** (1 / self.periods_year) - 1

    # Create df to simulate skipping best x days
    def get_close_series_with_best_x_days_removed(self, number_of_days_to_remove):
        # create alt DataFrame that will hold new returns_pct_vs_prev_day and close values
        self.alt_stock_df = self.stock_df[['date', 'returns_pct_vs_prev_day']]
        self.alt_stock_df = self.alt_stock_df.add_prefix('alt_')
        # Get indices of top x rows
        self.top_x_indices_removed = self.alt_stock_df.nlargest(number_of_days_to_remove,
                                                                'alt_returns_pct_vs_prev_day').index
        # replace top x indices with 0 and store in alternate series
        self.alt_stock_df.loc[self.top_x_indices_removed, 'alt_returns_pct_vs_prev_day'] = 0

        # calculate alternate close price
        temp_value = self.stock_df.iloc[0]['close']
        for index, row in self.alt_stock_df.iterrows():
            alt_return_pct = row['alt_returns_pct_vs_prev_day']
            temp_value = temp_value + (temp_value * alt_return_pct)
            self.alt_stock_df.at[index, 'alt_close'] = temp_value

    def __post_init__(self):
        # check if end date is after start date
        if self.periods_year() < 0:
            raise ValueError(
                f"The start_date argument, {self.start_date}, should be before the end_date argument, {self.end_date}")
        # todo add max/min dates for complete stock dataset. Then creates a method to repull the stock_df with new dates
        # get stock data
        stock_df = get_stock_data(self.ticker)
        stock_df = clean_stock_data(stock_df)
        self.stock_df = stock_df[
            (stock_df['date'] >= self.start_date)
            & (stock_df['date'] <= self.end_date)
            ]

        # Get periods in years
        self.periods_year = relativedelta(self.end_date, self.start_date).years

        # get return percentage compared to previous day
        self.stock_df['returns_pct_vs_prev_day'] = self.stock_df['close'].pct_change().fillna(0)
