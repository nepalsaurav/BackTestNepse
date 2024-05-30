import pandas as pd
import json
import random
import tablib
from tqdm import tqdm


def MonteCarloSimulation(filepath):
    print("Monte Carlo Simulation Started")
    df = pd.read_excel(filepath)
    result = df.to_json(orient="table")
    parsed = json.loads(result)['data']

    total_len = len(parsed)

    monte_carlo_simulation = 10

    export_data = tablib.Dataset(
        headers=['Stock Group', 'Invest Amount', 'Return Amount', 'Return Percent'])

    for i in tqdm(range(0, 50001)):
        random_data = random.sample(parsed, 5)
        stock_pile = ''
        return_amount = 0
        for data in random_data:
            stock_pile += f"{data['Symbol']}|"
            return_amount += data["Return Amount"]
        return_percent = ((return_amount - 500000)/return_amount) * 100
        append_item = stock_pile, 500_000, return_amount, return_percent
        export_data.append(append_item)

    with open("msim.xlsx", "wb") as f:
        f.write(export_data.export('xlsx'))

    print("Monte Carlo Simulation Finished and save file in msim.xlsx")
