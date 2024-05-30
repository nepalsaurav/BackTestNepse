import ta
import numpy as np
import json
import tablib
import random

from utils.data.getdata import GetData


def calculate_amplitude_probability(value, weight, custom_value):
    value_array = np.array(value)
    weight_array = np.array(weight)
    multiply_array = value_array * weight_array
    aggregate_value = sum(multiply_array)/sum(weight_array)
    # Calculate the absolute difference between a and b
    absolute_difference = abs(aggregate_value - custom_value)
    rank = 1 - absolute_difference / max(aggregate_value, custom_value)
    # print("ranking of number", rank)
    return rank


def custom_ml_algo(df, buying_agg_value, buying_agg_value_weight, selling_agg_value, selling_agg_value_weight):
    df = df
    df["Signal"] = "No condition"
    df["Buying_Prob"] = 0
    df["Selling_Prob"] = 0
    buying_prob = 0.5
    selling_prob = 0.5
    buying_agg_value_copy = 0
    buy_hold_days = 0
    is_buy_started = False
    percentage_return_we_want = 0.15
    buy_price = 0
    for index, row in df.iterrows():
        if is_buy_started:
            buy_hold_days += 1
        random_number = random.randint(0, 1)
        if len(buying_agg_value) == 0:
            if random_number == 1:
                buying_prob = 1
        if len(buying_agg_value) != 0:
            buying_prob = calculate_amplitude_probability(
                buying_agg_value, buying_agg_value_weight, row["Custom Value"])
        if len(selling_agg_value) == 0:
            if random_number == 0:
                selling_prob = 1
        if len(selling_agg_value) != 0:
            selling_prob = calculate_amplitude_probability(
                selling_agg_value, selling_agg_value_weight, row["Custom Value"])
        df.loc[index, 'Buying_Prob'] = buying_prob
        df.loc[index, 'Selling_Prob'] = selling_prob
        if buying_prob > 0.95 and is_buy_started == False:
            df.loc[index, 'Signal'] = "Buy"
            buy_price = row["Close"]
            buying_agg_value_copy = row["Custom Value"]
            is_buy_started = True
        elif selling_prob > 0.95 and buy_hold_days >= 3:
            df.loc[index, 'Signal'] = "Sell"
            if row["Close"] - buy_price > 0:
                selling_agg_value.append(row["Custom Value"])
                buying_agg_value.append(buying_agg_value_copy)
                b_weight = (
                    ((row["Close"] - buy_price)/buy_price)/percentage_return_we_want) * 100
                buying_agg_value_weight.append(b_weight)
                selling_agg_value_weight.append(b_weight)
            is_buy_started = False
            buy_price = 0
            buy_hold_days = 0
            buying_agg_value_copy = 0
        else:
            '''Noting to do'''
    return df


def find_buy_sell_points(df):
    df["Signal"] = "No condition"
    max_profit = 0
    buy_point = None
    sell_point = None
    min_price = 0
    number_of_holding_days = 0
    is_buy_started = False
    for index, row in df.iterrows():
        if is_buy_started:
            number_of_holding_days += 1
        if not is_buy_started:
            buy_point = index
            min_price = row["Close"]
            is_buy_started = True
            number_of_holding_days = 1
            df.loc[buy_point, 'Signal'] = "Buy"
        potential_profit = (row["Close"] - min_price)/min_price
        # print(potential_profit)
        if potential_profit >= 0.15 and number_of_holding_days >= 3:
            max_profit = potential_profit
            sell_point = index
            is_buy_started = False
            number_of_holding_days = 0
            df.loc[sell_point, 'Signal'] = "Sell"
    # print(df)
    return df


class CustomMl:
    def strategy(self, df):
        # Volatility indicator
        df["ATR14"] = ta.volatility.AverageTrueRange(
            high=df["High"], low=df["Low"],
            close=df["Close"], window=14, fillna=False).average_true_range()

        # trendIndicator
        df["ADX14"] = ta.trend.ADXIndicator(high=df["High"], low=df["Low"],
                                            close=df["Close"], window=14, fillna=False).adx()
        df["macd_signal"] = ta.trend.macd_signal(
            close=df["Close"], window_slow=26, window_fast=12, window_sign=9, fillna=False)
        # Momentum indicator
        df["RSI14"] = ta.momentum.RSIIndicator(
            close=df["Close"], window=14, fillna=False).rsi()
        df["Custom Value"] = (df["ATR14"] + df["ADX14"] +
                              df["RSI14"] + df["macd_signal"])
        df = df.dropna()
        # df = custom_ml_algo(df=df, buying_agg_value=[], buying_agg_value_weight=[],selling_agg_value=[], selling_agg_value_weight=[])
        df = find_buy_sell_points(df)
        signal_price = df["Close"].iloc[-1]
        date = df["Date"].iloc[-1]
        if df["Signal"].iloc[-1] == "Buy":
            return "Buy", date, signal_price
        elif df["Signal"].iloc[-1] == "Sell":
            return "Buy", date, signal_price
        else:
            return "No_signal", df["Date"].iloc[-1], df["Close"].iloc[-1]

    def condition(self, row):
        if row["SMA10"] > row["SMA20"]:
            return "Buy"
        elif row["SMA20"] > row["SMA10"]:
            return "Sell"
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
        buy_date = 0
        is_buy_started = False
        df_data = tablib.Dataset(
            headers=['Date', 'Close', 'Position', 'qtd', 'Invest', 'Number Of Buy Days', 'Custom Value'])
        print_position = ''
        for data in parsed:
            if is_buy_started:
                buy_date += 1
            if data["Signal"] == "Buy":
                if position != 'Buy':
                    is_buy_started = True
                    buy_date = 1
                    qtd = invest_amount/data["Close"]
                    position = 'Buy'
                    print_position = 'Buy'
            if data["Signal"] == "Sell":
                if position == 'Buy' and buy_date >= 3:
                    invest_amount = qtd * data["Close"]
                    position = 'Sell'
                    is_buy_started = False
                    buy_date = 0
                    qtd = 0
                    print_position = 'Sell'
            append_data = (data["Date"], data["Close"],
                           print_position, qtd, invest_amount,  buy_date,  data['Custom Value'])
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
