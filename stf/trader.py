#!/usr/bin/env python3

import argparse
import logging
import time
from typing import Type, Dict

import schedule

from stf.brokerages.AlpacaBrokerage import AlpacaBrokerage
from stf.brokerages.AlpacaPaperBrokerage import AlpacaPaperBrokerage
from stf.brokerages.Brokerage import Brokerage
from stf.brokerages.DryRunBrokerage import DryRunBrokerage
from stf.strategies.Strategy import Strategy


class Trader:
    def __init__(self) -> None:
        super().__init__()
        self.__setup_logging()
        self.brokerages: Dict[str, Type[Brokerage]] = {
            "dry_run": DryRunBrokerage,
            "alpaca": AlpacaBrokerage,
            "alpaca_paper": AlpacaPaperBrokerage,
        }
        self.strategies: Dict[str, Type[Strategy]] = {}

    def start(self):
        parser = self.__get_parser()
        args = parser.parse_args()
        logging.info(f"Brokerage - {args.brokerage}")
        brokerage = self.brokerages[args.brokerage]()
        logging.info(f"Strategy - {args.strategy}")
        strategy = self.strategies[args.strategy](brokerage)
        if args.send_event:
            logging.info(f"Sending event: {args.send_event}")
            result = getattr(strategy, args.send_event)()
        elif args.start_daemon:
            logging.info(f"Starting daemon")
            scheduler = Scheduler(strategy)
            scheduler.run()

    def register_strategy(self, name: str, strategy: Type[Strategy]):
        self.strategies[name] = strategy

    def register_brokerage(self, name: str, brokerage: Type[Brokerage]):
        self.brokerages[name] = brokerage

    def __get_parser(self):
        parser = argparse.ArgumentParser(description="Algorithmic Stock Trader")
        parser.add_argument("--brokerage", choices=self.brokerages, required=True)
        parser.add_argument("--strategy", choices=self.strategies, required=True)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "--send_event", help="Event to send (for now this is a method name in the chosen strategy)")
        group.add_argument("--start_daemon", action="store_true")
        return parser

    @staticmethod
    def __setup_logging():
        logging.basicConfig(filename='log',
                            format='[%(asctime)s] [%(levelname)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.DEBUG)
        logging.getLogger().addHandler(logging.StreamHandler())


class Scheduler:
    def __init__(self, strategy: Strategy, error_sleep_secs: int = 30):
        self.error_sleep_secs = error_sleep_secs
        strategy.register_events()
        logging.info("Scheduled all jobs")

    def run(self):
        while True:
            try:
                schedule.run_pending()
            except Exception as ex:
                logging.error(f"!!!! Unexpected failure: {ex}")
                logging.error(f"!!!! Sleeping {self.error_sleep_secs} seconds and then trying again")

            time.sleep(self.error_sleep_secs)
