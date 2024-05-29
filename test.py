import unittest
from algo.general.tenandtwenty import TenAndTwentySma
from algo.general.strategy import RSIOversoldBounce, VolumeDiscrepancy, BreakoutConfirmation, ATRStopLossMAC
import pandas as pd


import unittest
from HtmlTestRunner import HTMLTestRunner


class TestTenAndTwentySma(unittest.TestCase):
    def setUp(self):
        self.strategy = TenAndTwentySma()
        self.dummy_data = pd.DataFrame({
            'Close': [100, 110, 120, 115, 130, 125, 135, 140, 145, 150],
        })

    def test_buy_signal(self):
        self.dummy_data['SMA10'] = [100, 105, 110, 112.5, 115, 120, 125, 130, 135, 140]
        self.dummy_data['SMA20'] = [100, 105, 110, 112.5, 115, 117.5, 120, 122.5, 125, 127.5]
        df = self.strategy.strategy(self.dummy_data, symbol='TEST', test=True)
        self.assertTrue((df['Signal'] == 1).any())

    def test_sell_signal(self):
        self.dummy_data['SMA10'] = [100, 105, 110, 112.5, 115, 110, 105, 100, 95, 90]
        self.dummy_data['SMA20'] = [100, 105, 110, 112.5, 115, 120, 125, 130, 135, 140]
        df = self.strategy.strategy(self.dummy_data, symbol='TEST', test=True)
        self.assertTrue((df['Signal'] == 0).any())

    def test_no_signal(self):
        self.dummy_data['SMA10'] = [100, 105, 110, 112.5, 115, 110, 105, 100, 95, 90]
        self.dummy_data['SMA20'] = [100, 105, 110, 112.5, 115, 117.5, 120, 122.5, 125, 127.5]
        df = self.strategy.strategy(self.dummy_data, symbol='TEST', test=True)
        print(df)
        self.assertTrue(df['Signal'].isnull().all())

class TestRsiOversoldBounce(unittest.TestCase):
    def setUp(self):
        self.strategy = RSIOversoldBounce()
        self.dummy_data = pd.DataFrame({
            'Close': [100, 110, 120, 115, 130, 125, 135, 140, 145, 150],
            'RSI': [20, 25, 28, 32, 29, 35, 31, 40, 42, 45]
        })

    def test_buy_signal(self):
        # RSI falls below the predefined oversold threshold
        df = self.strategy.strategy(self.dummy_data, symbol='TEST')
        self.assertTrue((df['Signal'] == 1).all())

    def test_sell_signal(self):
        # RSI rises above the predefined threshold
        self.dummy_data['RSI'] = [80, 75, 72, 68, 71, 65, 69, 60, 58, 55]
        df = self.strategy.strategy(self.dummy_data, symbol='TEST')
        self.assertTrue((df['Signal'] == 0).all())

    def test_no_signal(self):
        # RSI conditions are not met
        self.dummy_data['RSI'] = [40, 45, 48, 52, 49, 55, 51, 60, 62, 65]
        df = self.strategy.strategy(self.dummy_data, symbol='TEST')
        self.assertTrue(df['Signal'].isnull().all())


class TestBreakoutConfirmation(unittest.TestCase):
    def setUp(self):
        self.strategy = BreakoutConfirmation()
        self.dummy_data = pd.DataFrame({
            'Close': [100, 105, 110, 115, 120, 125, 130, 135, 140, 145],
            'Volume': [10000, 12000, 15000, 8000, 20000, 7000, 18000, 25000, 9000, 30000]
        })

    def test_buy_signal(self):
        # Price breaks above a resistance level with increased volume
        df = self.strategy.strategy(self.dummy_data, symbol='TEST')
        self.assertTrue((df['Signal'] == 1).all())

    def test_sell_signal(self):
        # RSI rises above the predefined threshold
        self.dummy_data['Close'] = [145, 140, 135, 130, 125, 120, 115, 110, 105, 100]
        df = self.strategy.strategy(self.dummy_data, symbol='TEST')
        self.assertTrue((df['Signal'] == 0).all())

    def test_no_signal(self):
        # Breakout conditions are not met
        self.dummy_data['Close'] = [100, 105, 110, 115, 120, 125, 130, 135, 140, 135]
        df = self.strategy.strategy(self.dummy_data, symbol='TEST')
        self.assertTrue(df['Signal'].isnull().all())

class TestAtrStopLoss(unittest.TestCase):
    def setUp(self):
        self.strategy = ATRStopLossMAC()
        self.dummy_data = pd.DataFrame({
            'Close': [100, 105, 110, 115, 120, 125, 130, 135, 140, 135],
            'High': [105, 110, 115, 120, 125, 130, 135, 140, 145, 140],
            'Low': [95, 100, 105, 110, 115, 120, 125, 130, 135, 130]
        })

    def test_stop_loss_order(self):
        # Verify that the strategy sets appropriate stop-loss orders based on the current ATR value
        df = self.strategy.strategy(self.dummy_data, symbol='TEST')
        self.assertTrue((df['Signal'] == 1).all())

    def test_no_signal_above_stop_loss(self):
        # Validate that no signals are generated when the price is above the stop-loss level
        self.dummy_data['Close'] = [150, 155, 160, 165, 170, 175, 180, 185, 190, 195]
        df = self.strategy.strategy(self.dummy_data, symbol='TEST')
        self.assertTrue((df['Signal'].isnull()).all())

    def test_sell_signal_below_stop_loss(self):
        # Ensure that sell signals are generated when the price falls below the stop-loss level
        self.dummy_data['Close'] = [90, 85, 80, 75, 70, 65, 60, 55, 50, 55]
        df = self.strategy.strategy(self.dummy_data, symbol='TEST')
        self.assertTrue((df['Signal'] == 0).all())


class TestVolumeDiscrepancy(unittest.TestCase):
    def setUp(self):
        self.strategy = VolumeDiscrepancy()
        self.dummy_data = pd.DataFrame({
            'Close': [100, 110, 120, 115, 130, 125, 135, 140, 145, 150],
            'Volume': [10000, 12000, 15000, 8000, 20000, 7000, 18000, 25000, 9000, 30000]
        })

    def test_buy_signal(self):
        # Significant price increase with low volume
        df = self.strategy.strategy(self.dummy_data, symbol='TEST')
        self.assertTrue((df['Signal'] == 1).all())

    def test_sell_signal(self):
        # Significant price decrease with low volume
        self.dummy_data['Close'] = [150, 145, 140, 135, 130, 125, 120, 115, 110, 100]
        df = self.strategy.strategy(self.dummy_data, symbol='TEST')
        self.assertTrue((df['Signal'] == 0).all())

    def test_no_signal(self):
        # Volume conditions are not met
        self.dummy_data['Volume'] = [5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000]
        df = self.strategy.strategy(self.dummy_data, symbol='TEST')
        self.assertTrue(df['Signal'].isnull().all())



if __name__ == '__main__':
    # Create a test suite
    test_suite = unittest.TestSuite()

    # Add test cases to the suite
    test_suite.addTest(unittest.makeSuite(TestTenAndTwentySma))
    test_suite.addTest(unittest.makeSuite(TestRsiOversoldBounce))
    test_suite.addTest(unittest.makeSuite(TestBreakoutConfirmation))
    test_suite.addTest(unittest.makeSuite(TestAtrStopLoss))
    test_suite.addTest(unittest.makeSuite(TestVolumeDiscrepancy))

    # Define a TextTestRunner
    runner = unittest.TextTestRunner()

    # Run the test suite using TextTestRunner
    result = runner.run(test_suite)

    # Get the test results
    num_failures = len(result.failures)
    num_errors = len(result.errors)
    num_tests_run = result.testsRun

    # Display test results summary
    print("Tests run:", num_tests_run)
    print("Failures:", num_failures)
    print("Errors:", num_errors)

    if num_failures == 0 and num_errors == 0:
        print("All tests passed!")



