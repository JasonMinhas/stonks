from dataclasses import dataclass
import datetime as dt
import pandas as pd
import general_functions as gf
import yfinance as yf
from dateutil.relativedelta import relativedelta
from typing import Optional


@dataclass
class StockData:
    ticker: str
    start_date: dt.date
    end_date: dt.date
    periods_year: Optional[int] = None
    stock_df: Optional[pd.DataFrame] = None
    description: Optional[str] = 'This is the original dataset.'
    return_pct: Optional[float] = None
    annualized_return_pct: Optional[float] = None
    best_x_indices: Optional[list] = None

    def get_stock_data(self):
        stock_ticker = yf.Ticker(self.ticker)
        stock_df = stock_ticker.history(period="max")

        self.stock_df = stock_df

    def clean_stock_df(self):
        self.stock_df = self.stock_df.reset_index()
        self.stock_df = gf.clean_headers(self.stock_df)
        self.stock_df = gf.strip_df(self.stock_df)
        self.stock_df['date'] = pd.to_datetime(self.stock_df['date']).dt.date

    # Filter df to specific timeframe
    def filter_stock_df(self):
        self.stock_df = self.stock_df[
            (self.stock_df['date'] >= self.start_date)
            & (self.stock_df['date'] <= self.end_date)
            ]

    # Calculate return percentage
    def get_return_pct(self):
        # take only first and last row which would be the min and max date
        first_and_last_rows = self.stock_df.iloc[[0, -1]]
        # find percentage difference between the min and max date
        self.return_pct = first_and_last_rows['close'].pct_change().iloc[-1]

    # Calculate annualized return percentage
    def get_annualized_return_pct(self):
        self.annualized_return_pct = (1 + self.return_pct) ** (1 / self.periods_year) - 1

    # Create df to simulate skipping best x days
    def remove_best_x_days(self, number_of_days_to_remove):
        self.description = f'This scenario simulates removing the best performing {number_of_days_to_remove} days.'

        # Get indices of top x rows
        self.best_x_indices = self.stock_df.nlargest(number_of_days_to_remove,
                                                               'return_pct_vs_prev_day').index
        # replace top x indices with 0 and store in alternate series
        self.stock_df.loc[self.best_x_indices, 'return_pct_vs_prev_day'] = 0

        # calculate alternate close price
        temp_close_value = self.stock_df.iloc[0]['close']
        for index, row in self.stock_df.iterrows():
            new_return_pct = row['return_pct_vs_prev_day']
            temp_close_value = temp_close_value + (temp_close_value * new_return_pct)
            self.stock_df.at[index, 'close'] = temp_close_value

        # Update attributes since the close prices have been updated
        self.update_attributes()

        return self

    def update_attributes(self):
        # get return percentage
        self.get_return_pct()

        # get annualized return percentage
        self.get_annualized_return_pct()

    def __post_init__(self):
        # get stock data
        self.get_stock_data()
        # clean stock data
        self.clean_stock_df()
        # filter stock data by date
        self.filter_stock_df()
        # get periods in years
        self.periods_year = relativedelta(self.end_date, self.start_date).years
        # check if end date is after start date and raise error if true
        if self.periods_year < 0:
            raise ValueError(
                f"The start_date argument, {self.start_date}, should be before the end_date argument, {self.end_date}")
        # get return percentage compared to previous day
        self.stock_df['return_pct_vs_prev_day'] = self.stock_df['close'].pct_change().fillna(0)
        # Update attributes
        self.update_attributes()
