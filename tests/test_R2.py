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
def test_R2():
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

    # deploy reward smart contract from random account
    value = random.randint(0, total_accounts - 1)
    print("selected account", value)
    contract_reward1 = deploy_rewardMarket_rdm(accounts[value])
    print(accounts[value], "deployed the rewardSC")

    # authorize all accounts to use the deployed smart contracts
    authorize_all_accounts(contract_reward1, sc_token_contract)

    number_of_rewards = 0
    for i in accounts:
        reward_price = random.randint(200, 1000)
        reward_amount = random.randint(
            100, 500
        )  # vlt vom Guthaben abhängig machen wenn guthaben niedrig dann mehr rewards benötigt
        addReward(contract_reward1, i, reward_price, reward_amount)
        number_of_rewards += 1
        wait_time = random.randint(0, 60)
        time.sleep(wait_time)

    reward_counter = 0
    while reward_counter <= number_of_rewards - 1:
        price = contract_reward1.getPriceItem(reward_counter, {"from": account2})
        print("reward", reward_counter, " has the price ", price)
        reward_counter = reward_counter + 1

    # buy rewards
    reward_selection = random.randint(0, reward_counter - 1)
    print("only reward", reward_selection, "gets bought")
    for i in accounts:
        sc_token_contract.increaseSupply(100000, {"from": i})
        if sc_token_contract.balanceOf(i) >= contract_reward1.getPriceItem(
            reward_selection, {"from": i}
        ):
            ##check if reward exists
            contract_reward1.buyItem(
                reward_selection, {"from": i, "gas_limit": 1000000}
            )
            print(i, "bought reward", reward_selection)
        else:
            print(i, "has not enough CitSciToken to buy the reward")
        reward_counter = 0
        while reward_counter <= number_of_rewards - 1:
            price = contract_reward1.getPriceItem(reward_counter, {"from": account2})
            demand = contract_reward1.getDemandItem(reward_counter, {"from": account2})
            print(
                "reward",
                reward_counter,
                " has the price of",
                price,
                "and demand of ",
                demand,
            )
            reward_counter = reward_counter + 1
"""
