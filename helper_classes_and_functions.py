from dataclasses import dataclass
import datetime as dt
import pandas as pd
import general_functions as gf
import yfinance as yf
from dateutil.relativedelta import relativedelta
from typing import Optional

@dataclass
class StockData():
    ticker: str
    start_date: dt.date
    end_date: dt.date
    stock_df: Optional[pd.DataFrame] = None

    def get_stock_data(self):
        stock_ticker = yf.Ticker(self.ticker)
        stock_df = stock_ticker.history(period="max")

        self.stock_df = stock_df

    def clean_stock_df(self):
        self.stock_df = self.stock_df.reset_index()
        self.stock_df = gf.clean_headers(self.stock_df)
        self.stock_df = gf.strip_df(self.stock_df)
        self.stock_df['date'] = pd.to_datetime(self.stock_df['date']).dt.date

    # todo need a way to filter df to specific timeframe

    def __post_init__(self):
        # get stock data
        self.get_stock_data()
        # clean stock data
        self.clean_stock_df()



@dataclass
class StockSimulator(best_x_days=0, worst_x_days=0):
    StockData: StockData
    periods_year: Optional[pd.DataFrame] = None
    return_pct: Optional[pd.DataFrame] = None
    annualized_return_pct: Optional[pd.DataFrame] = None

    def periods_year(self) -> int:
        return relativedelta(self.end_date, self.start_date).years

    # Calculate return percentage
    def get_return_pct(self) -> float:
        # take only first and last row which would be the min and max date
        first_and_last_rows = self.stock_df.iloc[[0, -1]]
        # find percentage difference between the min and max date
        return_pct = first_and_last_rows['close'].pct_change().iloc[-1]

        return return_pct

    # Calculate annualized return percentage
    def get_annualized_return_pct(self) -> float:
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
        for index, row in self.stock_df.iterrows():
            # if index is in top 10 index then  0 pct
            # Else use original pct

            alt_return_pct = row['alt_returns_pct_vs_prev_day']
            temp_value = temp_value + (temp_value * alt_return_pct)
            self.alt_stock_df.at[index, 'alt_close'] = temp_value

    def __post_init__(self): # todo run this everytime df get updated
        # Get periods in years
        self.StockData.periods_year = relativedelta(self.StockData.end_date, self.StockData.start_date).years

        # check if end date is after start date
        if self.StockData.periods_year < 0:
            raise ValueError(
                f"The start_date argument, {self.StockData.start_date}, should be before the end_date argument, {self.StockData.end_date}")

        # get return percentage compared to previous day
        self.StockData.stock_df['return_pct_vs_prev_day'] = self.StockData.stock_df['close'].pct_change().fillna(0)

        print('sdss')
