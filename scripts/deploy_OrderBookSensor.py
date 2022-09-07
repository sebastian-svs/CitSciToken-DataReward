from brownie import OrderBookSensor2, OrderBookSensor3
from scripts.helpful_scripts import get_account
from web3 import Web3
from brownie import Contract
from web3 import Web3


def get_scToken():
    sc_token_contract = Contract.from_explorer(
        "0x748D1aC3c7D2140AC4c80bcea7704797C00D4887"
    )  # load contract from rinkeby.etherscan
    return sc_token_contract


def deploy_orderbook():
    account = get_account()  # creating account from private key
    contract = OrderBookSensor2.deploy(
        "0x748D1aC3c7D2140AC4c80bcea7704797C00D4887",
        {"from": account},
        publish_source=True,
    )  # deployment of the contract
    return contract


def deploy_orderbook_sensor(account):
    contract = OrderBookSensor2.deploy(
        "0x748D1aC3c7D2140AC4c80bcea7704797C00D4887",
        {"from": account},
        publish_source=True,
    )  # deployment of the contract
    return contract


def deploy_orderbook_sensor2(account):
    contract = OrderBookSensor3.deploy(
        "0x748D1aC3c7D2140AC4c80bcea7704797C00D4887",
        {"from": account},
        publish_source=True,
    )  # deployment of the contract
    return contract


def main():
    deploy_orderbook()
