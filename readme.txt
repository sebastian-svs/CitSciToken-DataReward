DEPLOYMENT:

The program was tested on Windows 10 x64 
Python 3.10.1 is used as while developing, deploying and desting this protoype.
Brownie v1.19.0 - Python development framework for Ethereum is used hile developing, deploying and desting this protoype.
To deploy the Smart contracts you need to install brownie
The codes are written in solidity ^0.8.0 this however does not have any effects on your local machine and only has an effect on the Etehreum network.

To install Brownie follow this guide:
https://eth-brownie.readthedocs.io/en/stable/install.html

Makesure that the private addresses have enough Rinkeby ETH in case the amount is not sufficient reload the accounts here
https://rinkebyfaucet.com/

To run the scripts you need to type:
brownie run scripts/name.py --network rinkeby

Example:
brownie run scripts/deploy_OrderBookAssets.py --network rinkeby

Brownie prints the contract address in the console. You can copy it to https://rinkeby.etherscan.io/ and interact with it there
Or interact with it with a script (see /tests)

Rinkeby might shut down in Q3 of 2023 you need to change the network after that for example to the Goerli Testnet all accounts need to be loaded with the new network ETH then as well.
All main networks are already preinstalled to brownie
brownie run scripts/deploy_OrderBookAssets.py --network othernetwork

TESTS:
For testing you need to additionally need to install numpy (random tests) and inject it to brownie

You can find the numpy install guide here:
https://numpy.org/install/

To inject it to brownie use this command:
pipx inject eth-brownie numpy

To run the tets on the rinekby network. Make sure that the accounts have enough RinkebyETH!

Currently all /test scripts are deactivated by comments. Delete the """ """" comments to activate the test.
This is an example how to create logfiles:
brownie test --network rinkeby -s  >A2.log

This is an example how to create gas profiles:
brownie test --network rinkeby --gas   