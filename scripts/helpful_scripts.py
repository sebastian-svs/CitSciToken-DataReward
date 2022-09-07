from brownie import accounts, network, config

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache",
    "hardhat",
    "local-ganache",
    "mainnet-fork",
]

# helpful for development to switch easily from develepment network (Ganache) to actual Ethereum Network Rinkeby
def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print(accounts[0].balance())
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])
