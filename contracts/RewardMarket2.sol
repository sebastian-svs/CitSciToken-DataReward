// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./InterfaceERC7772.sol";
import "@openzeppelin/contracts/token/ERC777/IERC777.sol";
import "@openzeppelin/contracts/token/ERC777/IERC777Sender.sol";
import "@openzeppelin/contracts/token/ERC777/IERC777Recipient.sol";
import "@openzeppelin/contracts/utils/introspection/IERC1820Registry.sol";
import "@openzeppelin/contracts/utils/introspection/ERC1820Implementer.sol";

contract RewardMarket2 is
    InterfaceERC7772,
    IERC777Sender,
    IERC777Recipient,
    ERC1820Implementer
{
    IERC1820Registry private _erc1820 =
        IERC1820Registry(0x1820a4B7618BdE71Dce8cdc73aAB6C95905faD24);
    bytes32 public constant TOKENS_RECIPIENT_INTERFACE_HASH =
        keccak256("ERC777TokensRecipient");
    bytes32 public constant TOKENS_SENDER_INTERFACE_HASH =
        keccak256("ERC777TokensSender");

    address public token;
    mapping(address => uint256) public userToHolding;

    constructor(address this_token) {
        _erc1820.setInterfaceImplementer(
            address(this),
            TOKENS_RECIPIENT_INTERFACE_HASH,
            address(this)
        );

        token = this_token;
    }

    function tokensReceived(
        address _operator,
        address _from,
        address _to,
        uint256 _amount,
        bytes calldata _userData,
        bytes calldata _operatorData
    ) external override {
        require(
            msg.sender == token,
            "the calling ERC777 token must match supported token"
        );
        // like approve + transferFrom, but only one tx
        userToHolding[_from] += _amount;

        emit TokensReceived(
            msg.sender,
            _operator,
            _from,
            _to,
            _amount,
            _userData,
            _operatorData
        );
    }

    function tokensToSend(
        address _operator,
        address _from,
        address _to,
        uint256 _amount,
        bytes calldata _userData,
        bytes calldata _operatorData
    ) external override {
        require(_amount > 0, "zero amount");
        emit TokensToSend(
            msg.sender,
            _operator,
            _from,
            _to,
            _amount,
            _userData,
            _operatorData
        );
    }

    function withdrawAccidental(uint256 _amount) external {
        require(_amount > 0, "zero amount");
        require(userToHolding[msg.sender] >= _amount, "insufficient funds");
        require(
            IERC777(token).balanceOf(address(this)) >= _amount,
            "contract insufficient funds"
        );

        userToHolding[msg.sender] -= _amount;
        IERC777(token).send(msg.sender, _amount, "");
    }

    struct Item {
        string reward_access;
        string description;
        address seller;
        uint256 price;
        uint256 amount;
        uint256 demand;
    }

    struct boughtItem {
        string reward_access;
        address seller;
    }

    mapping(address => boughtItem[]) private itemToHolding;
    Item[] private arr;
    uint256 public itemCount;
    uint256 pricePercantageChange = 100; //1%

    function addItem(
        string memory _reward_access,
        string memory _description,
        uint256 _price,
        uint256 _amount
    ) public returns (uint256) {
        itemCount++;
        Item memory newitem;
        newitem.reward_access = _reward_access;
        newitem.description = _description;
        newitem.seller = msg.sender;
        newitem.price = _price;
        newitem.amount = _amount;
        newitem.demand = 0;
        arr.push(newitem);
        return itemCount;
    }

    function checkItemExisting(uint256 _index) public view returns (bool) {
        require(_index < arr.length, "index to high");
        Item storage i = arr[_index];
        return (i.seller != address(0));
    }

    function removeItem(uint256 _index) public returns (uint256) {
        Item storage i = arr[_index];
        require(_index < arr.length, "index to high");
        require(i.seller != address(0), "no such item"); // not exists
        require(i.seller == msg.sender, "only seller can remove item");
        arr[_index] = arr[arr.length - 1];
        arr.pop();
        itemCount--;
        return itemCount;
    }

    function buyItem(uint256 _index) public {
        require(arr[_index].seller != address(0), "no such item"); // not exists
        require(
            arr[_index].price <= IERC777(token).balanceOf(msg.sender),
            "not enough tokens to buy the reward"
        );
        require(arr[_index].amount >= 0, "currenty sold out");
        IERC777(token).operatorSend(
            msg.sender,
            arr[_index].seller,
            arr[_index].price,
            "",
            ""
        );
        arr[_index].amount -= 1;
        boughtItem memory newItem;
        newItem.reward_access = arr[_index].reward_access;
        newItem.seller = arr[_index].seller;
        itemToHolding[msg.sender].push(newItem);
        arr[_index].demand += 1;
        priceBalance(arr[_index].demand);
    }

    function update_amount(uint256 _index, uint256 _amount) public {
        require(arr[_index].seller != address(0), "no such item"); // not exists
        require(
            arr[_index].seller == msg.sender,
            "only seller can change amount"
        ); // not exists
        arr[_index].amount = _amount;
    }

    function priceBalance(uint256 _demand) public {
        for (uint256 i = 0; i <= arr.length - 1; i++) {
            if (arr[i].demand >= _demand) {
                if (arr[i].price < pricePercantageChange) {
                    arr[i].price += 1;
                } else if (arr[i].price >= pricePercantageChange) {
                    uint256 price = arr[i].price;
                    uint256 modulo = price % pricePercantageChange;
                    price = price - modulo;
                    price = price / pricePercantageChange;
                    arr[i].price += price;
                }
            } else if (arr[i].demand < _demand) {
                if (arr[i].price < pricePercantageChange) {
                    if (arr[i].price > 0) {
                        arr[i].price -= 1;
                    }
                } else if (arr[i].price >= pricePercantageChange) {
                    uint256 price = arr[i].price;
                    uint256 modulo = price % pricePercantageChange;
                    price = price - modulo;
                    price = price / pricePercantageChange;
                    arr[i].price -= price;
                }
            }
        }
    }

    function getListedItem(uint256 _index)
        public
        view
        returns (
            string memory,
            uint256,
            uint256
        )
    {
        Item storage i = arr[_index];
        require(i.seller != address(0), "no such item"); // not exists
        return (i.description, i.price, i.demand);
    }

    function getBoughtItem(uint256 _index)
        public
        view
        returns (string memory, address)
    {
        require(itemToHolding[msg.sender].length > 0, "no items bought yet");
        return (
            itemToHolding[msg.sender][_index].reward_access,
            itemToHolding[msg.sender][_index].seller
        );
    }

    function getDemandItem(uint256 _index) public view returns (uint256) {
        return arr[_index].demand;
    }

    function getPriceItem(uint256 _index) public view returns (uint256) {
        return arr[_index].price;
    }
}
