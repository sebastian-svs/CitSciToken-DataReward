from brownie import CitSciToken
from scripts.helpful_scripts import get_account
from web3 import Web3

# varaible to determine the initial suppy
initial_supply = Web3.toWei(1000, "ether")


def deploy_token():
    # private key from .env oder local testnet see helpful_scripts.py
    account = get_account()
    sc_token = CitSciToken.deploy(
        initial_supply, [], {"from": account}, publish_source=True
    )  # publish_sorce=True to automatically flatten the code for varification on Etherscan
    return sc_token


def main():
    deploy_token()
