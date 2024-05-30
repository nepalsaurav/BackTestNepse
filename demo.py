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