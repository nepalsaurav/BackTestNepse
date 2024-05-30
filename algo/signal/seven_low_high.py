class SevenLowAndHigh:
    def strategy(self, df):
        df["7-Day-High"] = df["Close"].rolling(window=7).max()
        df["7-Day-Low"] = df["Close"].rolling(window=7).min()
        if df["Close"].iloc[-1] <= df["7-Day-Low"].iloc[-1]:
            return "Buy", df["Date"].iloc[-1], df["Close"].iloc[-1]
        elif df["Close"].iloc[-1] >= df["7-Day-High"].iloc[-1]:
            return "Sell", df["Date"].iloc[-1]
        else:
            return "No_signal", df["Date"].iloc[-1], df["Close"].iloc[-1]
