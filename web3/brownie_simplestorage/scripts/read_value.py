# read from the contract
from brownie import SimpleStorage, accounts, config


def read_contract():
    simple_storage = SimpleStorage[-1]  # recent deployment
    # We need abi and address but brownie already knows it
    print(simple_storage.retrieve())


def main():
    read_contract()
