# Stock Trading Framework

## Python
- Use Python 3.7 or above
- Add any credentials to the `config` directory
- Create an instance of `Trader`
- Register any brokerages or strategies
- Invoke `trader.start()`. This will read command line arguments and begin running the code
- Use the `--help` flag for CLI format

### Setting up Alpaca Brokerage

To use the Alpaca brokerage (paper money or real money), follow these steps:

1) Go to https://alpaca.markets/
2) Create a new account
3) Generate the Key ID and Secret Key
4) Go to the `/config` directory and run `touch alpaca.json`
5) Paste your key id and secret in the following format:

``` JSON
{
    "key_id": "<YOUR KEY HERE>",
    "secret_key": "<YOUR SECRET HERE>"
}
```