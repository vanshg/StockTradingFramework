from stf.brokerages.AlpacaBrokerage import AlpacaBrokerage


class AlpacaPaperBrokerage(AlpacaBrokerage):
    CONFIG_FILENAME = "alpaca_paper.json"

    def __init__(self, key_id=None, secret_key=None):
        super().__init__(key_id, secret_key, "https://paper-api.alpaca.markets")
