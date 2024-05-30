import ta
import numpy as np
import json
import tablib

from utils.data.getdata import GetData


class SevenLowAndHigh:
    def strategy(self, df, symbol):
        df["7-Day-High"] = df["Close"].rolling(window=7).max()
        df["7-Day-Low"] = df["Close"].rolling(window=7).min()
        df["Signal"] = df.apply(self.condition, axis=1)
        df = df.dropna()
        # print(df)
        return df

    def condition(self, row):
        if row["Close"] <= row["7-Day-Low"]:
            return 1
        elif row["Close"] >= row["7-Day-High"]:
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
            is_days=True, number_of_days=100)
        benchmark_df = stock_price.get_data(
            start_date=start_date, end_date=end_date)
        benchmark_df['Benchmark_Returns'] = benchmark_df['Close'].pct_change()
        benchmark_df = benchmark_df.dropna()
        covariance = df['Asset_Returns'].cov(benchmark_df['Benchmark_Returns'])
        variance = benchmark_df['Benchmark_Returns'].var()
        beta = covariance / variance
        return round(beta, 3)
