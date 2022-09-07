from scripts.helpful_scripts import get_account
from scripts.get_deployedContracts import get_scToken
from scripts.deploy_RewardMarket import deploy_rewardMarket
from brownie import accounts, config
from brownie import Contract
from web3 import Web3
import time
from brownie.network.gas.strategies import GasNowStrategy

sc_address = "0x748D1aC3c7D2140AC4c80bcea7704797C00D4887"

"""
def test_R1():
    ##Getting accounts and deploying contract
    account = get_account()  # creating account from private key
    account2 = accounts.add(config["wallets"]["from_key2"])  # creating account2
    account3 = accounts.add(config["wallets"]["from_key3"])  # creating account2
    contract = deploy_rewardMarket()
    print("Reward smart contract deployed with with the address", contract.address)
    ##including token contract and regrister acccounts regrister the orderbook smart contract at the token contract
    sc_token_contract = get_scToken()
    sc_token_contract.authorizeOperator(
        contract.address, {"from": account}
    )  # account regrister so the contract can request payments and deposits
    sc_token_contract.authorizeOperator(
        contract.address, {"from": account2}
    )  # account regrister so the contract can request payments and deposits
    sc_token_contract.authorizeOperator(
        contract.address, {"from": account3}
    )  # account regrister so the contract can request payments and deposits
    # start testing the Marketplace contract

    # first buy order and testing if it gets accepted
    sc_token_contract.increaseSupply(
        10000, {"from": account2}
    )  # account regrister so the contract can request payments and deposits
    balance_account = sc_token_contract.balanceOf(account.address)
    balance_account2 = sc_token_contract.balanceOf(account2.address)

    contract.addItem(
        "url", "premium Account", 100, 5, {"from": account}
    )  # add reward with acces point, description of the reward, and price
    print("reward added with amount =", 5, "and price", 100, "from account", account)

    contract.addItem(
        "url2", "different premium Account", 30, 50, {"from": account3}
    )  # add another reward with acces point, description of the reward, and price
    print("reward added with amount =", 50, "and price", 30, "from account", account)
    contract.buyItem(0, {"from": account2})
    reward = contract.getBoughtItem(0, {"from": account2})
    assert reward == ("url", account.address)
    print("reward1 bought by =", account, "and has now access to", reward)
    assert sc_token_contract.balanceOf(account.address) == balance_account + 100
    assert sc_token_contract.balanceOf(account2.address) == balance_account2 - 100
    print("balances of", account, account2, "changed correctly")
    # the reward with the higher demand rises in price the reward with the lower demand gets cheaper
    assert contract.getDemandItem(0, {"from": account2}) == 1
    assert contract.getDemandItem(1, {"from": account2}) == 0
    assert contract.getPriceItem(0, {"from": account2}) == 101
    assert contract.getPriceItem(1, {"from": account2}) == 29
    print("demand and prices of both rewards changed like expected")
    contract.buyItem(1, {"from": account2})
    reward = contract.getBoughtItem(1, {"from": account2})
    assert reward == ("url2", account3.address)
    print("reward2 bought by =", account, "and has now access to", reward)
"""
