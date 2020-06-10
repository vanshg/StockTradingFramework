import json
import logging

import alpaca_trade_api as tradeapi
from alpaca_trade_api import entity
from alpaca_trade_api.rest import APIError

from stf.brokerages.Brokerage import Brokerage
from stf.models.Position import Position


class AlpacaBrokerage(Brokerage):

    CONFIG_FILENAME = "alpaca.json"

    def __init__(self, key_id=None, secret_key=None, base_url=None):
        logging.info("Initializing AlpacaBrokerage")
        if key_id is None or secret_key is None:
            key_id, secret_key = self.get_credentials_from_file()
        self.api = tradeapi.REST(key_id, secret_key, base_url)
        account = self.api.get_account()
        if account.trading_blocked or account.account_blocked:
            logging.error(f"ERROR: Alpaca account/trading blocked!!")

    @property
    def is_open(self):
        return bool(self.api.get_clock().is_open)

    def is_tradable_stock(self, ticker):
        try:
            logging.info(f"Fetching asset {ticker}")
            result = self.api.get_asset(ticker.upper())
            logging.info(f"Got result for asset {ticker}: {result.__dict__}")
            return result.tradable
        except APIError as ex:
            logging.warning(f"Untradable asset {ticker}. {ex}")
            return False
        except Exception as ex:
            logging.error(f"Unknown error occurred: {ex}")
            return False

    def buy(self, ticker, num_shares):
        if self.is_open:
            logging.info(f"Submitting market order to buy {num_shares} shares of {ticker}")
            self.api.submit_order(ticker.upper(), num_shares, 'buy', 'market', 'day')
        else:
            logging.warning(f"Market is NOT open, so therefore not buying {num_shares} shares of {ticker}")

    def sell(self, ticker, num_shares):
        if self.is_open:
            logging.info(f"Submitting market order to sell {num_shares} shares of {ticker}")
            self.api.submit_order(ticker.upper(), num_shares, 'sell', 'market', 'day')
        else:
            logging.warning(f"Market is NOT open, so therefore not selling {num_shares} shares of {ticker}")

    def sell_all_positions(self):
        if self.is_open:
            logging.info(f"Selling all positions")
            for position in self.api.list_positions():
                self.sell(position.symbol, position.qty)
        else:
            logging.warning(f"Market is NOT open, so therefore not selling all positions")

    @property
    def buying_power(self):
        return float(self.api.get_account().buying_power)

    @property
    def portfolio_value(self):
        return float(self.api.get_account().portfolio_value)

    @property
    def positions(self) -> [Position]:
        return [self.alpaca_to_our_position(position) for position in self.api.list_positions()]

    @staticmethod
    def alpaca_to_our_position(alpaca_position: entity.Position) -> Position:
        """
        Takes a Position object returns by Alpaca and converts it into our model
        :param alpaca_position: an Alpaca position instance
        :return: our Position instance
        """
        position = Position()
        position.num_shares = int(alpaca_position.qty)
        position.ticker = alpaca_position.symbol
        position.day_percent_return = float(alpaca_position.unrealized_intraday_plpc) * 100
        position.total_percent_return = float(alpaca_position.unrealized_plpc) * 100
        return position

    def get_credentials_from_file(self):
        """
        Credentials should be stored in a file called alpaca.json, with keys for "secret_key" and "key_id"
        For example:
        {
            "key_id": "<YOUR KEY HERE>",
            "secret_key": "<YOUR SECRET HERE>"
        }

        :return: key_id, secret_key
        """
        try:
            with open(f"config/{self.CONFIG_FILENAME}") as credentials_file:
                credentials = json.load(credentials_file)
                return credentials['key_id'], credentials['secret_key']
        except Exception as ex:
            logging.error(f"Credentials error: Check that alpaca.json exists and is formatted correctly: {ex}")
