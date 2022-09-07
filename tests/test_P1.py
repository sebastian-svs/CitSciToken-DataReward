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
def test_P1():
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
    print(account, "and", account2, "autorized at deployed contract")
    # start testing the sensor orderbook contract
    # first buy order and testing if it gets accepted
    amount = random.randint(1, 1000)
    print("randomized amount = ", amount)
    price = random.randint(1, 1000)
    print("randomized price = ", price)
    needed_sc_for_scenario = (amount * price) + (amount * price * 3)
    sc_token_contract.increaseSupply(needed_sc_for_scenario, {"from": account})
    balance = sc_token_contract.balanceOf(account.address)
    balance2 = sc_token_contract.balanceOf(account2.address)

    contract_asset.addBuyOrder(amount, price, {"from": account})
    balance -= amount * price
    assert (amount * price) == contract_asset.getBalanceBuyer({"from": account})
    assert sc_token_contract.balanceOf(account.address) == balance
    assert sc_token_contract.balanceOf(contract_asset.address) == (amount * price)
    print("buy oder added from = ", account)
    print(
        "CitScit token of the sum of",
        price * amount,
        "succesfully transfered from the buyer to the contract",
    )

    # first matching sell order
    tx = contract_asset.addSellOrder(
        "url_asset", amount, price, 193162972515784259321009795655, {"from": account2}
    )  # 193162972515784259321009795655 is gps data chile

    assert sc_token_contract.balanceOf(account2.address) == balance2 + (amount * price)
    try:
        print(
            "trade happened and data sent",
            tx.events["sendData"],
        )
    except:
        print("no trade")
    # second contract for seonsor data
    contract_sensortrade = deploy_orderbook_sensor2(account2)
    sc_token_contract.authorizeOperator(
        contract_sensortrade.address, {"from": account}
    )  # account regrister so the contract can request payments and deposits
    sc_token_contract.authorizeOperator(
        contract_sensortrade.address, {"from": account2}
    )  # account regrister so the contract can request payments and deposits
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
"""
