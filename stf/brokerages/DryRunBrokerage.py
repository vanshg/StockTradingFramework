import logging

from stf.brokerages.Brokerage import Brokerage
from stf.models import Position


class DryRunBrokerage(Brokerage):
    def __init__(self, mock_buying_power=100_000):
        self.mock_buying_power = mock_buying_power

    def is_open(self):
        return True

    def is_tradable_stock(self, ticker):
        logging.info(f"DRY RUN: is_tradable_stock: {ticker} - True")
        return True

    def buy(self, ticker, num_shares):
        logging.info(f"DRY RUN: Would have bought {num_shares} shares of {ticker}")

    def sell(self, ticker, num_shares):
        logging.info(f"DRY RUN: Would have sold {num_shares} shares of {ticker}")

    @property
    def buying_power(self):
        logging.info(f"DRY RUN: Assuming buying power of {self.mock_buying_power}")
        return self.mock_buying_power

    @property
    def portfolio_value(self):
        return self.mock_buying_power

    def sell_all_positions(self):
        logging.info(f"DRY RUN: Sell all positions")

    @property
    def positions(self) -> [Position]:
        logging.info(f"DRY RUN: Get all positions")
        return []

    def get_credentials_from_file(self):
        pass
