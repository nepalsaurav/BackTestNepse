import ta
import numpy as np
import json
import tablib
import pandas as pd

from utils.data.getdata import GetData

class ThreeAndSixEma:
    def strategy(self, df, symbol):
        df["EMA6"] = ta.trend.EMAIndicator(close=df["Close"], window=6, fillna=False).ema_indicator()
        df["EMA3"] = ta.trend.EMAIndicator(close=df["Close"], window=3, fillna=False).ema_indicator()
        df["Signal"] = df.apply(self.condition, axis=1)
        return df

    def condition(self, row):
        if row["EMA3"] > row["EMA6"]:
            return 1
        elif row["EMA6"] > row["EMA3"]:
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
        df_data = tablib.Dataset(headers=['Date', 'Close', 'Position', 'qtd', 'Invest', 'Number Of Buy Days'])
        print_position = ''
        for data in parsed:
            if data["Signal"] == 1:
                buy_date += 1
                if position != 'Buy':
                    qtd = invest_amount / data["Close"]
                    position = 'Buy'
                    print_position = 'Buy'
            if data["Signal"] == 0:
                if position == 'Buy' and (buy_date - 1) >= 3:
                    invest_amount = qtd * data["Close"]
                    position = 'Sell'
                    buy_date = 1
                    qtd = 0
                    print_position = 'Sell'
            append_data = (data["Date"], data["Close"], print_position, qtd, invest_amount, buy_date - 1)
            print_position = ''
            df_data.append(append_data)
        
        # Convert df_data back to DataFrame for easier manipulation
        df_result = pd.DataFrame(df_data.dict, columns=df_data.headers)

        # Calculate performance metrics
        sharpe_ratio = self.sharpe_ratio(df_result['Close'])
        sortino_ratio = self.sortino_ratio(df_result['Close'])
        max_drawdown = self.max_drawdown(df_result['Close'])

        return df_data, from_date, to_date, invest_amount, ((invest_amount - 100_000) / 100_000) * 100, sharpe_ratio, sortino_ratio, max_drawdown

    def std_deviation(self, df):
        std = df["Close"].std()
        return round(std, 3)

    def beta(self, df, start_date="", end_date=""):
        df['Asset_Returns'] = df['Close'].pct_change()
        df = df.dropna()
        stock_price = GetData("NEPSE_index")
        benchmark_df = stock_price.get_data(start_date=start_date, end_date=end_date)
        benchmark_df['Benchmark_Returns'] = benchmark_df['Close'].pct_change()
        benchmark_df = benchmark_df.dropna()
        covariance = df['Asset_Returns'].cov(benchmark_df['Benchmark_Returns'])
        variance = benchmark_df['Benchmark_Returns'].var()
        beta = covariance / variance
        return round(beta, 3)

    def sharpe_ratio(self, returns):
        risk_free_rate = 0.01
        excess_returns = returns.pct_change() - risk_free_rate / 252
        avg_excess_return = excess_returns.mean()
        std_excess_return = excess_returns.std()
        sharpe_ratio = avg_excess_return / std_excess_return
        return round(sharpe_ratio * np.sqrt(252), 3)  # Annualize Sharpe Ratio

    def sortino_ratio(self, returns):
        risk_free_rate = 0.01
        excess_returns = returns.pct_change() - risk_free_rate / 252
        avg_excess_return = excess_returns.mean()
        downside_deviation = excess_returns[excess_returns < 0].std()
        sortino_ratio = avg_excess_return / downside_deviation
        return round(sortino_ratio * np.sqrt(252), 3)  # Annualize Sortino Ratio

    def max_drawdown(self, returns):
        cumulative_returns = (1 + returns.pct_change()).cumprod()
        peak = cumulative_returns.cummax()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()
        return round(max_drawdown, 3)
