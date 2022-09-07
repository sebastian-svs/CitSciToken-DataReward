from scripts.helpful_scripts import get_account
from scripts.get_deployedContracts import get_scToken
from scripts.deploy_token import deploy_token
from brownie import accounts, config
from brownie import Contract
from web3 import Web3
import time
import random

sc_address = "0x748D1aC3c7D2140AC4c80bcea7704797C00D4887"

"""
def test_currency():
    account = get_account()  # creating account from private key
    account2 = accounts.add(config["wallets"]["from_key2"])  # creating account2
    # sc_token_contract = get_scToken()  # normal test fetchin CitSciToken
    sc_token_contract = deploy_token()  # deploying new token for gas testing
    print("CitSciToken deployed with with the address", sc_token_contract.address)
    # getting CitSci Balance of both accounts
    balance = sc_token_contract.balanceOf(account.address)
    balance2 = sc_token_contract.balanceOf(account2.address)
    random_amount = random.randint(10, 10000)
    print("Random Amount =", random_amount)
    sc_token_contract.increaseSupply(random_amount, {"from": account})
    assert sc_token_contract.balanceOf(account.address) == balance + random_amount
    sc_token_contract.increaseSupply(random_amount, {"from": account2})
    assert sc_token_contract.balanceOf(account2.address) == balance2 + random_amount
    print(account, "and", account2, "claimed", random_amount, "CitSciTokens")
    random_amount_to_send = random.randint(10, random_amount)
    print("Random Amount to send =", random_amount_to_send)
    sc_token_contract.send(
        account.address, random_amount_to_send, "", {"from": account2}
    )
    assert (
        sc_token_contract.balanceOf(account.address)
        == balance + random_amount + random_amount_to_send
    )
    print(account, "received", random_amount_to_send, "from account", account2)
    total_supply = sc_token_contract.totalSupply({"from": account2})
    print("Total supply of CitSciTokens =", total_supply)
    sc_token_contract.burn(random_amount, "", {"from": account})
    assert (
        sc_token_contract.totalSupply({"from": account2})
        == total_supply - random_amount
    )
    print(
        "Decreased total supply of",
        total_supply,
        "CitSciTokens to",
        total_supply - random_amount,
    )
"""