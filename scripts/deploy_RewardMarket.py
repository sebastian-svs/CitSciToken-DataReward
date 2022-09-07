from brownie import RewardMarket, RewardMarket2
from scripts.helpful_scripts import get_account
from web3 import Web3
from brownie import Contract
from web3 import Web3


def deploy_rewardMarket():
    account = get_account()  # creating account from private key
    contract = RewardMarket2.deploy(
        "0x748D1aC3c7D2140AC4c80bcea7704797C00D4887",
        {"from": account},
        publish_source=True,
    )  # deployment of the contract
    return contract


def deploy_rewardMarket_rdm(account):
    contract = RewardMarket2.deploy(
        "0x748D1aC3c7D2140AC4c80bcea7704797C00D4887",
        {"from": account},
        publish_source=True,
    )  # deployment of the contract
    return contract


def main():
    deploy_rewardMarket()
