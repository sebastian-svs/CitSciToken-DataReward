from web3 import Web3
from brownie import Contract
from web3 import Web3

# get CitSci Token
def get_scToken():
    sc_token_contract = Contract.from_explorer(
        "0x748D1aC3c7D2140AC4c80bcea7704797C00D4887"
    )  # load contract from rinkeby.etherscan
    return sc_token_contract
