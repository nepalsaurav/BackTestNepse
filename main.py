from typing import Union

from fastapi import FastAPI
import pandas as pd

from create_html import create_response
from manager import StrategyManager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:5173",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/run_strategy")
def run_strategy(strategy: str = "",  from_date: str = "", to_date: str = "",isDay: bool = True):
    strategy_manager = StrategyManager(args={'strategy': strategy, 'isDay': isDay, 'start_date':from_date, 'end_date': to_date})
    result = strategy_manager.run_startegy()
    data = create_response(strategy=strategy, start_date=from_date, end_date=to_date, isDay=isDay)
    return data

@app.get("/single_stock")
def get_single_stock(symbol: str = ""):
    df = pd.read_excel(f"result/{symbol}.xlsx", sheet_name='Sheet1')
    data_json = df.to_json(orient="records")
    return data_json



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}