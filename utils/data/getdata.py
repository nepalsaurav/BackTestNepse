import requests
import tablib
from datetime import datetime, timedelta
import json
import os


def dump_json_file(data, symbol, start_date, end_date):
    with open(f"cachedata/{symbol}_{start_date}_{end_date}.json", "w+") as f:
        json.dump(data, f)


def get_json_data(symbol, start_date, end_date):
    data = None
    if os.path.exists(f"cachedata/{symbol}_{start_date}_{end_date}.json"):
        with open(f"cachedata/{symbol}_{start_date}_{end_date}.json", "r") as f:
            data = json.load(f)
        return True, data
    else:
        return False, data


class GetData:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_data(self, start_date, end_date):
        isFileExist, data = get_json_data(self.symbol, start_date, end_date)
        # print(isFileExist)
        if isFileExist == False:
            r = requests.get(
                f"https://backendtradingview.systemxlite.com/tradingViewSystemxLite/history?symbol={self.symbol}&resolution=1D&from={start_date}&to={end_date}&countback=80")
            data = r.json()
            dump_json_file(data, self.symbol, start_date, end_date)
        time = data['t']
        df_data = tablib.Dataset(
            headers=['Date', 'Open', 'Low', 'High', 'Close', 'Volume'])
        for i in range(0, len(time)):
            date = str(datetime.fromtimestamp(time[i])).split(" ")[0]
            open = float(data['o'][i])
            low = float(data['l'][i])
            high = float(data['h'][i])
            close = float(data['c'][i])
            volume = float(data['v'][i])
            append_data = (date, open, low, high, close, volume)
            df_data.append(append_data)

        return df_data.export('df')

    def get_start_and_end_date(self, number_of_days, is_days):
        if is_days == True:
            day = datetime.today()
            day = day.strftime("%d/%m/%Y")
            end_date = datetime(int(day.split("/")[2]), int(day.split("/")[1]),
                                int(day.split("/")[0]), 5, 45, 0)
            end_date = str(datetime.timestamp(end_date)).split(".")[0]
            day = datetime.today() - timedelta(days=number_of_days)
            day = day.strftime("%d/%m/%Y")
            start_date = datetime(int(day.split("/")[2]), int(day.split("/")[1]),
                                  int(day.split("/")[0]), 5, 45, 0)
            start_date = str(datetime.timestamp(start_date)).split(".")[0]
            return start_date, end_date
        else:
            return None, None
