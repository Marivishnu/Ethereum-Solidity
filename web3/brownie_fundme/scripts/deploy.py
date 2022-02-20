from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import get_account, deploy_mock
from web3 import Web3


def deploy_fundme():
    account = get_account()

    if (
        network.show_active() != "development"
        and network.show_active() != "ganache-local"
    ) or network.show_active() == "mainnet-fork-dev":
        price_feed_address = config["networks"][network.show_active()]["eth_usd"]
    else:
        deploy_mock()
        price_feed_address = MockV3Aggregator[-1].address
    fund_me = FundMe.deploy(price_feed_address, {"from": account})
    print("Contract deployed at", fund_me.address)


def main():
    deploy_fundme()
