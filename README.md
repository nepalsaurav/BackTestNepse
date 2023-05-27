# BackTestNepse

BackTestNepse is a repository on GitHub that allows you to backtest different strategies for stocks listed on the Nepal Stock Exchange (NEPSE). This tool provides a convenient way to evaluate the performance of various trading strategies using historical stock market data.

## Installation

To install the required dependencies for BackTestNepse, follow these steps:

1. Make sure you have Python installed on your system.
2. Open a command prompt or terminal.
3. Run the following command:

```bash
$ py -m pip install -r requirements.txt
```

This command will install all the necessary Python packages specified in the requirements file.

## Usage

You can run BackTestNepse using the following command and output will generated in output folder as output.html:

```bash
$ py main.py strategy=strategy_name
```


Replace `strategy_name` with the name of the desired strategy. The available strategies are:

- General:
  - Bollinger Band: `bollingerband`
  - Mixed Strategy: `mixedstrategy`
  - System One Turtle: `systemoneturtle`
  - Ten and Twenty SMA Strategy: `tenandtwentysma`
  - Three and Six EMA Strategy: `threeandsixema`

- Reddit Category:
  - Five SMA and Five RSI Strategy: `fivexfive`

Choose the strategy you want to test by specifying the corresponding `strategy_name` parameter in the command.

## Creating a Custom Strategy

You can also create your own custom strategy by following these steps:

1. Navigate to the `algo/general` folder in the repository.
2. Create a new Python file for your custom strategy class.
3. Copy the structure of one of the existing strategy classes and edit the `condition` method to implement your specific strategy logic.
4. Import the new strategy file into `manage.py`.
5. Create a new `elif` statement under the `run_strategy_method` function in `manage.py`, mapping your custom strategy name to the corresponding class.

With these steps, you can add and test your own trading strategies using BackTestNepse.

## Contributions

Contributions to BackTestNepse are welcome! If you have any ideas for improvements or new features, feel free to submit a pull request. Please make sure to follow the existing code structure and style guidelines.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code according to the terms of the license.

## Disclaimer

BackTestNepse is a tool for backtesting trading strategies and is provided for educational and informational purposes only. The results obtained from backtesting should not be considered as financial advice or indicative of future performance. Always exercise caution and conduct your own research before making any investment decisions.

For any further questions or inquiries, please refer to the documentation or reach out to the project maintainers.

