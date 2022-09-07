from scripts.helpful_scripts import get_account
from scripts.get_deployedContracts import get_scToken
from scripts.deploy_OrderBookSensor import (
    deploy_orderbook,
    deploy_orderbook_sensor,
    deploy_orderbook_sensor2,
)
from scripts.deploy_OrderBookAssets import (
    deploy_orderbook_assets,
    deploy_orderbook_assetsECA,
)
from scripts.deploy_RewardMarket import deploy_rewardMarket
from brownie import accounts, config
from brownie import Contract
from web3 import Web3
import time
import random
from brownie.network.gas.strategies import GasNowStrategy

sc_address = "0x748D1aC3c7D2140AC4c80bcea7704797C00D4887"

## for this test the paypout intervals are set very low in the contract
## uint256 public streamingDuration = 180; //here the streaming duration can be defined in seconds
## uint256 public streamingInterval = 60; //here the streaming payout Intervall can be defined in seconds

"""
def test_A1():
    ##Getting accounts and deploying contract
    account = get_account()  # creating account from private key
    account2 = accounts.add(config["wallets"]["from_key2"])  # creating account2
    contract_asset = deploy_orderbook_assetsECA()
    print("Deployed data asset contract address =", contract_asset.address)
    ##including token contract and regrister acccounts regrister the orderbook smart contract at the token contract
    sc_token_contract = get_scToken()
    sc_token_contract.authorizeOperator(
        contract_asset.address, {"from": account}
    )  # account regrister so the contract can request payments and deposits
    sc_token_contract.authorizeOperator(
        contract_asset.address, {"from": account2}
    )  # account regrister so the contract can request payments and deposits
    print(account, "and", account2, "autorized at data asset contract")

    ##deploy reward market
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

    for i in accounts:
        amount = sc_token_contract.balanceOf(i)
        print("reset", amount, "to 0. of", i)
        sc_token_contract.burn(amount, "", {"from": i})
    print("CitSci Token of all accounts reset to 0")

    # first buy order and testing if it gets accepted
    amount = 1
    print("amount = ", amount)
    price = 30
    print("price = ", price)
    needed_sc_for_scenario = amount * price * 3
    sc_token_contract.increaseSupply(needed_sc_for_scenario, {"from": account})
    balance = sc_token_contract.balanceOf(account.address)
    balance2 = sc_token_contract.balanceOf(account2.address)
    print("account1 has a balance of", balance)
    print("account2 has a balance of", balance2)

    contract_asset.addBuyOrder(amount, price * 3, {"from": account})
    balance -= amount * price * 3
    assert (amount * price * 3) == contract_asset.getBalanceBuyer({"from": account})
    assert sc_token_contract.balanceOf(account.address) == balance
    assert sc_token_contract.balanceOf(contract_asset.address) == (amount * price * 3)
    print("buy oder added from = ", account)
    print(
        "CitScit token of the sum of",
        price * amount * 3,
        "succesfully transfered from the buyer to the contract",
    )

    # first matching sell order
    tx = contract_asset.addSellOrder(
        "url_asset",
        amount,
        price * 3,
        193162972515784259321009795655,
        {"from": account2},
    )  # 193162972515784259321009795655 is gps data chile

    assert sc_token_contract.balanceOf(account2.address) == balance2 + (
        amount * price * 3
    )
    try:
        print(
            "trade happened and data sent",
            tx.events["sendData"],
        )
    except:
        print("no trade")
    balance = sc_token_contract.balanceOf(account.address)
    balance2 = sc_token_contract.balanceOf(account2.address)
    print("AFTER DATA ASSET TRADE")
    print("account1 has a balance of", balance)
    print("account2 has a balance of", balance2)
    # reward trade
    contract.addItem(
        "url", "premium Account", 90, 10, {"from": account}
    )  # add reward with acces point, description of the reward, and price
    contract.buyItem(0, {"from": account2})
    balance = sc_token_contract.balanceOf(account.address)
    balance2 = sc_token_contract.balanceOf(account2.address)
    print("AFTER REWARD TRADE")
    print("account1 has a balance of", balance)
    print("account2 has a balance of", balance2)

    # second contract for seonsor data
    contract_sensortrade = deploy_orderbook_sensor2(account2)
    sc_token_contract.authorizeOperator(
        contract_sensortrade.address, {"from": account}
    )  # account regrister so the contract can request payments and deposits
    sc_token_contract.authorizeOperator(
        contract_sensortrade.address, {"from": account2}
    )  # account regrister so the contract can request payments and deposits
    current_balance = sc_token_contract.balanceOf(account.address)
    print("current amount=", current_balance)
    contract_sensortrade.addBuyOrder(amount, price, {"from": account})
    balance -= amount * price * 3
    assert (amount * price * 3) == contract_sensortrade.getBalanceBuyer(
        {"from": account}
    )
    assert sc_token_contract.balanceOf(account.address) == balance
    assert (
        sc_token_contract.balanceOf(contract_sensortrade.address)
        == (amount * price) * 3
    )
    print("buy oder added from = ", account)
    print(
        "CitScit token of the sum of",
        price * amount * 3,
        "succesfully transfered from the buyer to the contract",
    )

    # first matching sell order
    tx = contract_sensortrade.addSellOrder(
        "url_sensor", amount, price, {"from": account2}
    )
    try:
        print(
            "trade happened and data sent",
            tx.events["sendData"],
        )
    except:
        print("no trade")
    balance2 = sc_token_contract.balanceOf(account2.address)
    contract_sensortrade.withdrawEarningSeller({"from": account2, "gas_limit": 1000000})
    widraw = sc_token_contract.balanceOf(account2.address) - balance2
    print("first withdraw of", widraw, "CitSciTokens")
    time.sleep(80)
    contract_sensortrade.withdrawEarningSeller({"from": account2, "gas_limit": 1000000})
    widraw = sc_token_contract.balanceOf(account2.address) - balance2
    print("second withdraw of", widraw, "CitSciTokens")
    time.sleep(180)
    contract_sensortrade.withdrawEarningSeller({"from": account2, "gas_limit": 1000000})
    widraw = sc_token_contract.balanceOf(account2.address) - balance2
    print("complete withdraw of", widraw)
    assert balance2 + (amount * price) * 3 == sc_token_contract.balanceOf(
        account2.address
    )
    print(
        "complete witdraw after min. 180 sec of",
        price * amount * 3,
        "CitSciTokens of",
        account2,
    )

    balance = sc_token_contract.balanceOf(account.address)
    balance2 = sc_token_contract.balanceOf(account2.address)
    print("AFTER WITHDRAW")
    print("account1 has a balance of", balance)
    print("account2 has a balance of", balance2)
    contract.addItem(
        "url", "premium Account", 90, 10, {"from": account}
    )  # add reward with acces point, description of the reward, and price
    contract.buyItem(1, {"from": account2})
    balance = sc_token_contract.balanceOf(account.address)
    balance2 = sc_token_contract.balanceOf(account2.address)
    print("AFTER PURCHASE OF SECOND REWARD")
    print("account1 has a balance of", balance)
    print("account2 has a balance of", balance2)
"""
