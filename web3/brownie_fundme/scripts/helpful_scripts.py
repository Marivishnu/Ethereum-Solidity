from brownie import network, accounts, config, MockV3Aggregator, accounts
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account():
    if (
        network.show_active() == "development"
        or network.show_active() == "ganache-local"
        or network.show_active() == "mainnet-fork-dev"
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mock():
    print("Deploying mock....")
    if len(MockV3Aggregator) <= 0:
        mock = MockV3Aggregator.deploy(
            DECIMALS, STARTING_PRICE, {"from": get_account()}
        )
    else:
        mock = MockV3Aggregator[-1].address
