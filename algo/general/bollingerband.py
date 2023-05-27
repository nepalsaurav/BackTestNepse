import ta
import numpy as np
import json
import tablib

from utils.data.getdata import GetData

is_lowerbound_cross = False
is_higherbound_cross = False
class BollingerBand:
    def strategy(self, df):
        df["SMA10"] = ta.trend.SMAIndicator(close=df["Close"],
                                            window=10,
                                            fillna=False).sma_indicator()
        df["SMA20"] = ta.trend.SMAIndicator(close=df["Close"],
                                            window=20,
                                            fillna=False).sma_indicator()
        BB = ta.volatility.BollingerBands(close=df["Close"], window=20, window_dev=2, fillna=False)
        df["High Band"] = BB.bollinger_hband()
        df["Low Band"] = BB.bollinger_lband()
        df["Signal"] = df.apply(self.condition, axis=1)
        df = df.dropna()
        return df

    def condition(self, row):
        global is_lowerbound_cross
        global is_higherbound_cross
        return_condition = 'No Conditon'
        if row["Low Band"] >= row["Close"]:
           is_lowerbound_cross = True
        #    print(is_lowerbound_cross, "lower bound cross")
           return return_condition
        if row["Low Band"] <= row["Close"] and (is_lowerbound_cross and row["SMA10"] > row["SMA20"]):
            is_lowerbound_cross = False
            return_condition = "Buy"
            # print("Buy Condition full fill")
            return return_condition
        if row["High Band"] <= row["Close"]:
            is_higherbound_cross = True
            # print(is_higherbound_cross, "Upper bound cross")
            return return_condition
        if row["High Band"] >= row["Close"] and (is_higherbound_cross and row["SMA10"] < row["SMA20"]):
            is_higherbound_cross = False
            return_condition = "Sell"
            # print("Sell Condition full fill")
            return return_condition
        return return_condition

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
            if data["Signal"] == 'Buy':
                buy_date += 1
                if position != 'Buy':
                    qtd = invest_amount/data["Close"]
                    position = 'Buy'
                    print_position = 'Buy'
            if data["Signal"] == 'Sell':
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
