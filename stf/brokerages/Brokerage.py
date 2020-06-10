from abc import ABC, abstractmethod

from stf.models import Position


class Brokerage(ABC):
    @abstractmethod
    def is_tradable_stock(self, ticker):
        pass

    @property
    @abstractmethod
    def is_open(self):
        pass

    @abstractmethod
    def buy(self, ticker, num_shares):
        pass

    @abstractmethod
    def sell(self, ticker, num_shares):
        pass

    @abstractmethod
    def sell_all_positions(self):
        pass

    @property
    @abstractmethod
    def buying_power(self):
        pass

    @property
    @abstractmethod
    def portfolio_value(self):
        pass

    @property
    @abstractmethod
    def positions(self) -> [Position]:
        pass

    @abstractmethod
    def get_credentials_from_file(self):
        pass
