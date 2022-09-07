from scripts.helpful_scripts import get_account
from scripts.get_deployedContracts import get_scToken
from scripts.deploy_RewardMarket import deploy_rewardMarket_rdm
from scripts.deploy_OrderBookAssets import deploy_orderbook_assets
from scripts.deploy_OrderBookSensor import (
    deploy_orderbook_sensor,
    deploy_orderbook_sensor2,
)

from brownie import accounts, config
from brownie import Contract
from web3 import Web3
import time
import numpy as np
import random

total_accounts = 20
sigma = 0.1
first_order_price = random.randint(20, 100)

sc_address = "0x748D1aC3c7D2140AC4c80bcea7704797C00D4887"


def get_random_number(mean):
    sigma_adapted = mean * sigma
    s = np.random.normal(mean, sigma_adapted)
    s = round(s)
    return s


def authorize_all_accounts(contract, sc_token_contract):
    for i in accounts:
        sc_token_contract.authorizeOperator(contract.address, {"from": i})


def revoke_all_accounts(contract, sc_token_contract):
    for i in accounts:
        sc_token_contract.revokeOperator(contract.address, {"from": i})


def buyOrder(contract, selected_acc, amount, price):
    tx = contract.addBuyOrder(amount, price, {"from": selected_acc})
    print(
        selected_acc, "placed order buy order with amount", amount, "and price", price
    )
    return tx


def sellOrder(contract, selected_acc, amount, price):
    access_point = "Access-Point:URL"
    tx = contract.addSellOrder(access_point, amount, price, {"from": selected_acc})
    print(
        selected_acc, "placed order sell order with amount", amount, "and price", price
    )
    return tx


def addReward(contract, selected_acc, price, amount):
    access_point = "Reward:URL"
    description = "Cool reward"
    tx = contract.addItem(
        access_point, description, price, amount, {"from": selected_acc}
    )
    print(selected_acc, "added new item. amount:", amount, "and price", price)
    return tx


## for this test the paypout intervals are set low in the contract
## uint256 public streamingDuration = 1800; //here the streaming duration defined in seconds = 30 min
## uint256 public streamingInterval = 180; //here the streaming payout Intervall be defined in seconds = 3 min

"""
def test_P3():
    ##Getting accounts and setting up account mamagment
    print("sigma = ", sigma)
    print("first_order_price = ", first_order_price)
    # creating account from private key
    account1 = get_account()
    account2 = accounts.add(config["wallets"]["from_key2"])
    account3 = accounts.add(config["wallets"]["from_key3"])
    account4 = accounts.add(config["wallets"]["from_key4"])
    account5 = accounts.add(config["wallets"]["from_key5"])
    account6 = accounts.add(config["wallets"]["from_key6"])
    account7 = accounts.add(config["wallets"]["from_key7"])
    account8 = accounts.add(config["wallets"]["from_key8"])
    account9 = accounts.add(config["wallets"]["from_key9"])
    account10 = accounts.add(config["wallets"]["from_key10"])
    account11 = accounts.add(config["wallets"]["from_key11"])
    account12 = accounts.add(config["wallets"]["from_key12"])
    account13 = accounts.add(config["wallets"]["from_key13"])
    account14 = accounts.add(config["wallets"]["from_key14"])
    account15 = accounts.add(config["wallets"]["from_key15"])
    account16 = accounts.add(config["wallets"]["from_key16"])
    account17 = accounts.add(config["wallets"]["from_key17"])
    account18 = accounts.add(config["wallets"]["from_key18"])
    account19 = accounts.add(config["wallets"]["from_key19"])
    account20 = accounts.add(config["wallets"]["from_key20"])

    # fetchin CitSciToken
    sc_token_contract = get_scToken()

    # deploy smart contract orderbook for sensors from random account
    value = random.randint(0, total_accounts - 1)
    print("selected account", value)
    orderbookdeloyer1 = accounts[value]
    print(orderbookdeloyer1.address, "deployed the orderbookSSC")
    contract_sensortrade1 = deploy_orderbook_sensor2(orderbookdeloyer1)
    # authorize all accounts to use the deployed smart contracts
    authorize_all_accounts(contract_sensortrade1, sc_token_contract)
    print("All accounts joined the smart contract with access rights")
    # testing random orders for orderbook
    traders = total_accounts
    buyers = random.randint(1, traders - 1)
    sell_or_buy = [0] * buyers + [1] * (traders - buyers)
    random.shuffle(sell_or_buy)
    print("Order of sell and buy orders:", sell_or_buy)
    current_price = first_order_price
    y = 0
    contract_sensor_buyers = []
    contract_sensor_seller = []
    for i in sell_or_buy:
        if contract_sensortrade1.current_price() != 0:
            current_price = contract_sensortrade1.current_price()
            print("The current price for this data is:", current_price)
        random_amount = random.randint(1, 5)
        random_price = get_random_number(current_price)
        if i == 0:
            random_amount = random.randint(
                1, 5
            )  # sellers usually do not have so many sensor acces point to trade
            tx = sellOrder(
                contract_sensortrade1, accounts[y], random_amount, random_price
            )
            contract_sensor_seller.append(accounts[y])
        if i == 1:
            random_amount = random.randint(
                1, 30
            )  # buyers usually do want more sensor data but since orderfullfillments are tested the range is kept low
            sc_token_contract.increaseSupply(
                random_amount * random_price * 1000, {"from": accounts[y]}
            )
            contract_sensor_buyers.append(accounts[y])
            tx = buyOrder(
                contract_sensortrade1, accounts[y], random_amount, random_price
            )
        y += 1
        wait_time = random.randint(0, 10)
        time.sleep(wait_time)
        try:
            print(
                "trade happened and data sent",
                tx.events["sendData"],
            )
        except:
            print("no trade")
    print("buyers:", contract_sensor_buyers)
    print("sellers", contract_sensor_seller)

    for i in contract_sensor_buyers:
        wait_time = random.randint(0, 10)
        time.sleep(wait_time)
        try:
            contract_sensortrade1.removeYourBuyOrder({"from": i})
            print("buy order removed of", i)
        except:
            print("already fullfilled buy order of", i)

    for i in contract_sensor_seller:
        wait_time = random.randint(0, 10)
        time.sleep(wait_time)
        try:
            contract_sensortrade1.removeYourSellOrder({"from": i})
            print("sell order removed of", i)
        except:
            print("already fullfilled sell order of", i)

    revoke_all_accounts(contract_sensortrade1, sc_token_contract)
    print("All accounts revoked access rights of smart contract")
"""
