
from algo.reddit.fivexfive import FiveXFive
from algo.general.threeandsixema import ThreeAndSixEma
from algo.general.tenandtwenty import TenAndTwentySma
from algo.general.systemoneturtle import SystemOneTurtle
from algo.general.customml import CustomMl
from algo.general.seven_low_high import SevenLowAndHigh

from algo.general.strategy import RSIDivMACrossover
from algo.general.strategy import ATRStopLossMAC
from algo.general.strategy import RSIOversoldBounce
from algo.general.strategy import BreakoutConfirmation
from algo.general.strategy import VolumeDiscrepancy

from utils.data.getdata import GetData, get_json_data
import json
import tablib
from tqdm import tqdm
from msim import MonteCarloSimulation
from create_html import CreateHtml
import pandas as pd

import warnings
warnings.filterwarnings("ignore")


class StrategyManager:
    def __init__(self, args):
        print(args)
        self.args = args

    def run_startegy(self):
        if self.args['isDay']:
            start_date, end_date = GetData.get_start_and_end_date(is_days=True, number_of_days=100)
        else:
            start_date, end_date = GetData.get_start_and_end_date(is_days=False, start_date=self.args['start_date'], end_date=self.args['end_date'])
    
        isFileExist, data = get_json_data(f'{self.args["strategy"]}', start_date=start_date, end_date=end_date)
        if isFileExist:
            return data
        if self.args["strategy"] == "fivexfive":
            print(f"Running {self.args['strategy']} startegy")
            strategy = FiveXFive()
        elif self.args["strategy"] == "threeandsixema":
            print(f"Running {self.args['strategy']} startegy")
            strategy = ThreeAndSixEma()
        elif self.args["strategy"] == "tenandtwentysma":
            print(f"Running {self.args['strategy']} startegy")
            strategy = TenAndTwentySma()
        elif self.args["strategy"] == "systemoneturtle":
            print(f"Running {self.args['strategy']} startegy")
            strategy = SystemOneTurtle()
        elif self.args["strategy"] == "customml":
            print(f"Running {self.args['strategy']} startegy")
            strategy = CustomMl()
        elif self.args["strategy"] == "seven-low-high":
            print(f"Running {self.args['strategy']} startegy")
            strategy = SevenLowAndHigh()
        elif self.args["strategy"] == "rsiandmac":
            print(f"Running {self.args['strategy']} startegy")
            strategy = RSIDivMACrossover()

        elif self.args["strategy"] == "atrandmaccrossover":
            print(f"Running {self.args['strategy']} startegy")
            strategy = ATRStopLossMAC()
        elif self.args["strategy"] == "rsioversoldbounce":
            print(f"Running {self.args['strategy']} startegy")
            strategy = RSIOversoldBounce()
        
        elif self.args["strategy"] == "breakoutwithvolumeandrsi":
            print(f"Running {self.args['strategy']} startegy")
            strategy = BreakoutConfirmation()
        
        elif self.args["strategy"] == "volumediscrepancy":
            print(f"Running {self.args['strategy']} startegy")
            strategy = VolumeDiscrepancy()

        else:
            print("Error occur during running startegy")
            return 1
        with open('symbols.json', 'r') as f:
            data = json.load(f)
        export_data = tablib.Dataset(headers=['Symbol', 'From Date', 'To Date', 'Invest Amount', 'Return Amount', 'Return Percent', 'Standard Deviation', 'Beta', 'Sharpe Ratio', 'Sortino Ratio', 'Max Drawdown'])
        for data in data["Sheet1"]:
            try:
                symbol = data['symbol']
                stock_price = GetData(symbol=f"{symbol}_adj")
                df = stock_price.get_data(start_date=start_date, end_date=end_date)
                df = strategy.strategy(df=df, symbol=symbol)
                df_data, from_date, to_date, invest_amount, return_p, sharpe_ratio, sortino_ratio, max_drawdown = strategy.return_calculation(df)
                df_data = df_data.export('df')
                df_data.to_excel(f"result/{symbol}.xlsx", index=False)
                std = strategy.std_deviation(df)
                beta = strategy.beta(df, start_date, end_date)
                append_data = (symbol, from_date, to_date, 100000, invest_amount, return_p, std, beta, sharpe_ratio, sortino_ratio, max_drawdown)
                export_data.append(append_data)
            except Exception as e:
                print(e)
                pass
        with open("result.xlsx", "wb") as f:
            f.write(export_data.export('xlsx'))
        MonteCarloSimulation("result.xlsx")
        return "success"
        # print("Creating Html output")
        # CreateHtml(strategy=self.args["strategy"])
        # print("completed Html output")