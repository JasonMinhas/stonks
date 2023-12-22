# practice based on https://www.dataquest.io/blog/portfolio-project-predicting-stock-prices-using-pandas-and-scikit-learn/

import pandas as pd
import datetime as dt
import os
import yfinance as yf
import matplotlib.pyplot as plt

stonk_ticker = yf.Ticker("SPY")
stonk_hist_df = stonk_ticker.history(period="max")
stonk_hist_df = stonk_hist_df.reset_index()
stonk_hist_df['Date'] = stonk_hist_df['Date'].apply(lambda x: pd.to_datetime(x)).dt.date
stonk_hist_df.to_excel("historical_stonk_data/SPY_stonk_data.xlsx", index=False)


# stonk_hist_df = pd.read_csv("historical_stonk_data/MSFT_stonk_data.csv", index_col='Date')


# stonk_hist_df.plot.line(y="Close")
# plt.show()


print('yolo')