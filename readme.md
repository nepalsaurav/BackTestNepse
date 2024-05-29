Got it! Here's the content formatted as a GitHub README:

---

# BackTestNepse

BackTestNepse is a project for backtesting various trading strategies on the NEPSE (Nepal Stock Exchange). The project includes predefined strategies, the ability to define custom strategies, and a web interface to run and view the results.

## How to Use

### Running Strategies

To run a strategy, use the `manager.py` script. You can use either predefined strategies or custom strategies.

#### Example Usage

```python
import sys
from manager import StrategyManager
from create_html import CreateHtml

def main(args):
    # Run strategies
    arg = {}
    try:
        for a in args:
            arg[a.split("=")[0]] = a.split("=")[1]
        strategy_manager = StrategyManager(args=arg)
        strategy_manager.run_startegy()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main(sys.argv[1:])
```

### Running the Web Interface

BackTestNepse includes a FastAPI web interface. You can start the web server and access the interface to run and view strategies.

#### Example FastAPI Application

```python
from typing import Union

from fastapi import FastAPI

from create_html import create_response
from manager import StrategyManager
from fastapi.middleware.cors import CORSMiddleware

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
def run_strategy(strategy: str = "",  from_date: str = "", to_date: str = "", isDay: bool = True):
    strategy_manager = StrategyManager(args={'strategy': strategy, 'isDay': isDay, 'start_date': from_date, 'end_date': to_date})
    result = strategy_manager.run_startegy()
    data = create_response(strategy=strategy, start_date=from_date, end_date=to_date, isDay=isDay)
    return data

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

### Frontend

The frontend of the project is built using SvelteKit and can be found in the `frontend` directory.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

If you have any questions or suggestions, feel free to open an issue or contact me directly.

--- 

This README format should be compatible with GitHub's markdown rendering.