from solcx import compile_standard, install_solc
import json
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


install_solc("0.8.0")
# Compile solidity file

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

# print(compiled_sol)

# Saving compiled code

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# deploy the solidity and test it out
# 1. get bytecode

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# 2. get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# 3. connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chainid = 1337
address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = os.getenv("PRIVATE_KEY")

# print(private_key)

# create contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)

# Get latest transaction
nonce = w3.eth.getTransactionCount(address)
# print(nonce)

# deploy the contract

# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction

transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chainid, "from": address, "nonce": nonce, "gasPrice": w3.eth.gas_price}
)
signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)

tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Working with contract we need contract address and abi

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> simulates the call and get the return value (blue button in remix)
# Trasact -> makes the state change (orange button in remix)

print(simple_storage.functions.retrieve().call())

store_transaction = SimpleStorage.functions.store(15).buildTransaction(
    {
        "chainId": chainid,
        "from": address,
        "nonce": nonce + 1,
        "gasPrice": w3.eth.gas_price,
        "to": tx_receipt.contractAddress,
    }
)
sign_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
store_tx_hash = w3.eth.send_raw_transaction(sign_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)

print(simple_storage.functions.retrieve().call())
