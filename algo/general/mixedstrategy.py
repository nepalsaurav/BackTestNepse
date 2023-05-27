import ta
import numpy as np
import json
import tablib

from utils.data.getdata import GetData


class MixedStrategy:
    def strategy(self, df):
        df['VWAP20'] = ta.volume.VolumeWeightedAveragePrice(df['High'],df['Low'],df['Close'],df['Volume'],window=20,fillna=False).volume_weighted_average_price() #volume
        df['SMA10'] = ta.trend.SMAIndicator(df['Close'],window=10, fillna=False).sma_indicator() #trend
        df['SMA20'] = ta.trend.SMAIndicator(df['Close'],window=20, fillna=False).sma_indicator()
        df['SMA200'] = ta.trend.SMAIndicator(df['Close'],window=20, fillna=False).sma_indicator() #for 200 days moving average change window to 200
        df['KAMA'] = ta.momentum.KAMAIndicator(df['Close'],window=10,pow1=2,pow2=30,fillna=False).kama() #momentum
        # df['cumalative_return'] = ta.others.CumulativeReturnIndicator(df['Close'], fillna = False).cumulative_return()
        df['SAR'] = ta.trend.PSARIndicator(df['High'],df['Low'],df['Close'],step=0.02,max_step=0.2,fillna=False).psar()
        df = df.dropna()
        df["Signal"] = df.apply(self.condition, axis=1)
        return df

    def condition(self, row):
        if row['SMA10'] > row['SMA20'] and row['Close'] > row['VWAP20'] and row['Close'] > row['KAMA']:
            return 1
        elif row['Close'] < row['VWAP20'] or row['SMA10'] < row['SMA20']:
            return 0
        else:
            return 'No condition'

    def return_calculation(self, df):
        result = df.to_json(orient="table")
        parsed = json.loads(result)['data']
        from_date = parsed[0]['Date']
        to_date = parsed[len(parsed) - 1]['Date']
        position = ''
        invest_amount = 100_000
        qtd = 0
        buy_date = 1
        df_data = tablib.Dataset(
            headers=['Date', 'Close', 'Position', 'qtd', 'Invest', 'Number Of Buy Days'])
        print_position = ''
        for data in parsed:
            if data["Signal"] == 1:
                buy_date += 1
                if position != 'Buy':
                    qtd = invest_amount/data["Close"]
                    position = 'Buy'
                    print_position = 'Buy'
            if data["Signal"] == 0:
                if position == 'Buy' and (buy_date - 1) >= 3:
                    invest_amount = qtd * data["Close"]
                    position = 'Sell'
                    buy_date = 1
                    qtd = 0
                    print_position = 'Sell'
            append_data = (data["Date"], data["Close"],
                           print_position, qtd, invest_amount,  buy_date-1)
            print_position = ''
            df_data.append(append_data)
        return df_data, from_date, to_date, invest_amount, ((invest_amount - 100_000)/100_000) * 100

    def std_deviation(self, df):
        std = df["Close"].std()
        return round(std, 3)

    def beta(self, df):
        df['Asset_Returns'] = df['Close'].pct_change()
        df = df.dropna()
        stock_price = GetData("NEPSE_index")
        start_date, end_date = stock_price.get_start_and_end_date(
            is_days=True, number_of_days=360)
        benchmark_df = stock_price.get_data(
            start_date=start_date, end_date=end_date)
        benchmark_df['Benchmark_Returns'] = benchmark_df['Close'].pct_change()
        benchmark_df = benchmark_df.dropna()
        covariance = df['Asset_Returns'].cov(benchmark_df['Benchmark_Returns'])
        variance = benchmark_df['Benchmark_Returns'].var()
        beta = covariance / variance
        return round(beta, 3)
