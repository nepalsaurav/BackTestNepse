import tablib
import json
from tqdm import tqdm

from utils.data.getdata import GetData
from algo.signal.seven_low_high import SevenLowAndHigh
from algo.signal.customml import CustomMl


def GetSignal(strategy_param):
    if strategy_param == "seven-low-high":
        strategy = SevenLowAndHigh()
    elif strategy_param == "custom-ml":
        strategy = CustomMl()
    else:
        return
    export_data = tablib.Dataset(
        headers=['Symbol', 'Date', 'Signal', 'Signal Price'])
    with open('symbols.json', 'r') as f:
        data = json.load(f)
    for data in tqdm(data["Sheet1"]):
        try:
            symbol = data['symbol']
            symbol = data['symbol']
            stock_price = GetData(symbol=f"{symbol}_adj")
            start_date, end_date = stock_price.get_start_and_end_date(
                is_days=True, number_of_days=100)
            df = stock_price.get_data(
                start_date=start_date, end_date=end_date)
            signal, date, signal_price = strategy.strategy(df)
            append_data = (symbol, date, signal, signal_price)
            if signal != "No_signal":
                export_data.append(append_data)
        except Exception as e:
            pass
    with open(f"{strategy_param}.xlsx", "wb") as f:
        f.write(export_data.export('xlsx'))


GetSignal("custom-ml")
