import pandas as pd
from alpha_vantage.timeseries import TimeSeries


api_key = 'PFC26TXPY9UH7ZF0'

ts = TimeSeries(key=api_key, output_format='json')
json = ts.get_daily_adjusted(symbol='TSLA', outputsize='full')


df = pd.DataFrame.from_dict(json[0], orient='index').reset_index()
df.rename(columns={'index': 'date'}, inplace=True)

print('yolo')