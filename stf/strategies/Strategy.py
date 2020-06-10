from abc import ABC, abstractmethod

from stf.brokerages.Brokerage import Brokerage


class Strategy(ABC):

    def __init__(self, brokerage: Brokerage):
        self.brokerage = brokerage
        self.blacklist = []  # List of symbols to never trade (tickers should be in All Caps!)

    @abstractmethod
    def register_events(self):
        """
        Register any/all methods you want the framework to call on a regular basis using the schedule module
        See https://github.com/dbader/schedule for further details
        NOTE: Schedule times are in 24 hour format!
        """
        pass
