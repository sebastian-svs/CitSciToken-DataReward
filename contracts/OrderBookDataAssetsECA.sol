// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./InterfaceERC7772.sol";
import "@openzeppelin/contracts/token/ERC777/IERC777.sol";
import "@openzeppelin/contracts/token/ERC777/IERC777Sender.sol";
import "@openzeppelin/contracts/token/ERC777/IERC777Recipient.sol";
import "@openzeppelin/contracts/utils/introspection/IERC1820Registry.sol";
import "@openzeppelin/contracts/utils/introspection/ERC1820Implementer.sol";

contract OrderBookDataAssetsECA is
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

    struct Order {
        uint256 id;
        uint256 limitPrice;
        uint256 amount;
        uint256 entryTime;
        address addressOf;
        string dataAccess;
    }

    Order[] private sellList;
    Order[] private buyList;
    uint256 public id;
    uint256 public current_price;
    mapping(address => address[]) public tradePartners; //stores active dataStreams between buyer and seller, so that no multiple trades of the same dataAccess with the same buyer is not possible
    mapping(address => uint256) public buyerHolding; //stores ScToken of each individual buyer
    mapping(address => uint256) public sellerHolding; //stores ScToken of each individual seller

    event sendData(
        string access_point,
        address seller,
        address buyer,
        uint256 time
    ); //event with hashed information which can be read from outside of the blockchain

    //Sell side of the orderbook
    function getIndexSellList(uint256 _price)
        internal
        view
        returns (uint256 i)
    {
        for (i = 0; i < sellList.length; ) {
            if (sellList[i].limitPrice > _price) {
                i++;
            } else {
                return i;
            }
        }
    }

    function checkSeller(address _check) internal view returns (bool listed) {
        if (sellList.length == 0) {
            return false;
        }
        for (uint256 i = 0; i <= sellList.length - 1; i++) {
            if (sellList[i].addressOf == _check) {
                return true;
            }
        }
        return false;
    }

    function addSellOrder(
        string memory _dataAccess,
        uint256 _amount,
        uint256 _limitPrice,
        uint256 _utmGPS
    ) public {
        require(
            checkSeller(msg.sender) == false,
            "remove old order before you make a new one"
        ); //network members are only allowed to have one active Order
        require(_amount > 0, "amount must be bigger than 0"); //network members are only allowed to have one active Order
        require(
            _utmGPS == 193162972515784259321009795655,
            "GPS data must be from Chile"
        ); //checks gsp
        Order memory newOrder;
        newOrder.id = id;
        newOrder.limitPrice = _limitPrice;
        newOrder.amount = _amount;
        newOrder.dataAccess = _dataAccess;
        newOrder.entryTime = block.timestamp;
        newOrder.addressOf = msg.sender;
        uint256 rest;
        if (buyList.length == 0) {
            //no Buy Orders -> No trade -> New Order goes into the BuyList
            rest = newOrder.amount;
        } else {
            //checks in the SellList for possible trades
            rest = priceMatchingNewSell(
                newOrder.limitPrice,
                newOrder.amount,
                newOrder.dataAccess
            );
        }
        if (rest <= 0) {
            //the requested amount is already fullfilled -> Order wont be stored in the Orderbook
        } else {
            //there was no matching Order in the SellList or the Order was not completly fullfilled the rest amount will be stored in the SellList for future trades
            newOrder.amount = rest;
            if (sellList.length == 0) {
                sellList.push(newOrder);
            } else if (sellList.length == 1) {
                if (sellList[0].limitPrice < newOrder.limitPrice) {
                    sellList.push(sellList[0]);
                    sellList[0] = newOrder;
                } else if (sellList[0].limitPrice >= newOrder.limitPrice) {
                    sellList.push(newOrder);
                }
            } else {
                uint256 position = getIndexSellList(newOrder.limitPrice);
                if (position >= sellList.length) {
                    sellList.push(newOrder);
                } else {
                    uint256 last = sellList.length - 1;
                    sellList.push(sellList[last]);
                    Order memory copyOrder;
                    Order memory copyOrder2;
                    copyOrder = newOrder;

                    for (uint256 i = position; i < sellList.length; i++) {
                        copyOrder2 = sellList[i];
                        sellList[i] = copyOrder;
                        copyOrder = copyOrder2;
                    }
                }
            }
            id++;
        }
    }

    function priceMatchingNewSell(
        uint256 _limitPrice,
        uint256 _amount,
        string memory _dataAccess
    ) internal returns (uint256) {
        uint256 units = 0;
        uint256 accumulated_price = 0;
        for (uint256 i = buyList.length - 1; i >= 0; ) {
            if (
                buyList[i].limitPrice >= _limitPrice &&
                buyList[i].addressOf != msg.sender &&
                checkPartnerBuyer(buyList[i].addressOf) == false
            ) {
                //trade happens if price matches, seller and buyer address no the same, parters didn't trade yet
                if (buyList[i].amount >= _amount) {
                    //update  buyList
                    buyList[i].amount = buyList[i].amount - _amount;

                    //current price calculation
                    units = units + _amount;
                    accumulated_price =
                        accumulated_price +
                        (buyList[i].limitPrice * _amount);
                    current_price = accumulated_price / units;
                    //transfer tokens and data
                    buyerHolding[buyList[i].addressOf] -=
                        buyList[i].limitPrice *
                        _amount;
                    IERC777(token).send(
                        msg.sender,
                        (buyList[i].limitPrice * _amount),
                        ""
                    );
                    //from buyer to seller _amount* buyList[i].limitPrice
                    addPartnerToBuyer(buyList[i].addressOf);
                    emit sendData(
                        _dataAccess,
                        msg.sender,
                        buyList[i].addressOf,
                        block.timestamp
                    );
                    //_amount = 0;
                    //update  buyList
                    if (buyList[i].amount == 0) {
                        internalRemoveBuyOder(i);
                    }
                    return _amount;
                } else if (buyList[i].amount < _amount) {
                    //transfer tokens
                    //from buyer to seller  buyList[i].amount* buyList[i].limitPrice
                    addPartnerToBuyer(buyList[i].addressOf);
                    emit sendData(
                        _dataAccess,
                        msg.sender,
                        buyList[i].addressOf,
                        block.timestamp
                    );
                    buyerHolding[buyList[i].addressOf] -=
                        buyList[i].limitPrice *
                        _amount;
                    IERC777(token).send(
                        msg.sender,
                        (buyList[i].limitPrice * _amount),
                        ""
                    );
                    //current price calculation
                    units = units + buyList[i].amount;
                    accumulated_price =
                        accumulated_price +
                        (buyList[i].limitPrice * buyList[i].amount);
                    //_amount = _amount - buyList[i].amount;
                    buyList[i].amount == 0;
                    internalRemoveBuyOder(i);
                    if (_amount == 0) {
                        current_price = accumulated_price / units;
                        return _amount;
                    }
                    if (buyList.length == 0) {
                        current_price = accumulated_price / units;
                        return _amount;
                    }
                    i--;
                }
            } else if (
                buyList[i].limitPrice >= _limitPrice &&
                buyList[i].addressOf == msg.sender &&
                checkPartnerBuyer(buyList[i].addressOf) == true
            ) {
                if (buyList.length == 1) {
                    return _amount;
                } else {
                    i--;
                }
            } else {
                return _amount;
            }
        }
        return _amount; //NO TRADE with entry -> no price change
    }

    function internalRemoveSellOder(uint256 _index) internal {
        //remove function of the smart contract
        require(_index < sellList.length, "index to high");
        for (uint256 i = _index; i < sellList.length - 1; i++) {
            sellList[i] = sellList[i + 1];
        }
        sellList.pop();
    }

    function removeYourSellOrder() public returns (uint256) {
        require(sellList.length > 0, "no Order places yet");
        require(
            checkSeller(msg.sender) == true,
            "no order from you places yet"
        );
        for (uint256 i = 0; i <= sellList.length - 1; i++) {
            if (sellList[i].addressOf == msg.sender) {
                removeSellOder(i);
                return i;
            }
        }
        return 0;
    }

    function removeSellOder(uint256 _index) internal {
        //manual remove function only the seller is alowed to delete his own order
        Order storage copy = sellList[_index];
        require(_index < sellList.length, "index to high");
        require(
            checkSeller(msg.sender) == true,
            "place an order before you can remove it"
        );
        require(copy.addressOf == msg.sender, "only seller can remove order");
        for (uint256 i = _index; i < sellList.length - 1; i++) {
            sellList[i] = sellList[i + 1];
        }
        sellList.pop();
    }

    function getSellOrder(uint256 _index)
        public
        view
        returns (
            uint256,
            uint256,
            uint256,
            uint256,
            address
        )
    {
        require(sellList.length > 0, "No sell orders in this orderbook");
        require(
            _index <= sellList.length - 1,
            "No entry in the sell side of the orderbook, index too high"
        );
        Order storage i = sellList[_index];
        require(i.addressOf != address(0), "no such order"); // not exists
        return (i.id, i.limitPrice, i.amount, i.entryTime, i.addressOf);
    }

    //Buy side of the orderbook
    function addBuyOrder(uint256 _amount, uint256 _limitPrice) public {
        require(
            checkBuyer(msg.sender) == false,
            "remove old order before you submit a new one"
        ); //network members are only allowed to have one active Order
        require(_amount > 0, "amount must be bigger than 0"); //network members are only allowed to have one active Order
        require(
            IERC777(token).balanceOf(msg.sender) >= _limitPrice * _amount,
            "insufficient funds for the buy oder"
        );
        Order memory newOrder;
        newOrder.id = id;
        newOrder.limitPrice = _limitPrice;
        newOrder.amount = _amount;
        newOrder.entryTime = block.timestamp;
        newOrder.addressOf = msg.sender;
        uint256 required_amount = _limitPrice * _amount;
        //deposit tokens on smart contract
        IERC777(token).operatorSend(
            msg.sender,
            address(this),
            required_amount,
            "",
            ""
        );
        buyerHolding[msg.sender] += required_amount;
        uint256 rest;
        if (sellList.length == 0) {
            //no Sell Orders -> No trade -> New Order goes into the BuyList
            rest = newOrder.amount;
        } else {
            //checks in the SellList for possible trades
            rest = priceMatchingNewBuy(newOrder.limitPrice, newOrder.amount);
        }
        if (rest <= 0) {
            //the requested amount is already fullfilled -> Order wont be stored in the Orderbook
        } else {
            //there was no matching Order in the SellList or the Order was not completly fullfilled the rest amount will be stored in the BuyList for future trades
            newOrder.amount = rest;
            if (buyList.length == 0) {
                buyList.push(newOrder);
            } else if (buyList.length == 1) {
                if (buyList[0].limitPrice <= newOrder.limitPrice) {
                    buyList.push(newOrder);
                } else if (buyList[0].limitPrice > newOrder.limitPrice) {
                    buyList.push(buyList[0]);
                    buyList[0] = newOrder;
                }
            } else {
                uint256 position = getIndexBuyList(newOrder.limitPrice);
                if (position >= buyList.length) {
                    buyList.push(newOrder);
                } else {
                    uint256 last = buyList.length - 1;
                    buyList.push(buyList[last]);
                    Order memory copyOrder;
                    Order memory copyOrder2;
                    copyOrder = newOrder;

                    for (uint256 i = position; i < buyList.length; i++) {
                        copyOrder2 = buyList[i];
                        buyList[i] = copyOrder;
                        copyOrder = copyOrder2;
                    }
                }
            }

            id++;
        }
    }

    function priceMatchingNewBuy(uint256 _limitPrice, uint256 _amount)
        internal
        returns (uint256)
    {
        uint256 units = 0;
        uint256 accumulated_price = 0;
        for (uint256 i = sellList.length - 1; i >= 0; ) {
            if (
                sellList[i].limitPrice <= _limitPrice &&
                sellList[i].addressOf != msg.sender &&
                checkPartner(sellList[i].addressOf) == false
            ) {
                //TRADE HAPPENS if price matches, seller and buyer address no the same, parters didn't trade yet
                if (sellList[i].amount >= _amount) {
                    //update sellList
                    //sellList[i].amount = sellList[i].amount - _amount;
                    //current price calculation
                    units = units + _amount;
                    accumulated_price =
                        accumulated_price +
                        (sellList[i].limitPrice * _amount);
                    current_price = accumulated_price / units;
                    //transfer tokens and data
                    buyerHolding[msg.sender] -=
                        _amount *
                        sellList[i].limitPrice;
                    IERC777(token).send(
                        sellList[i].addressOf,
                        (_amount * sellList[i].limitPrice),
                        ""
                    );
                    //from buyer to seller _amount*sellList[i].limitPrice userHolding[sellList[i].addressOf] to userHolding[msg.sender]
                    addPartner(sellList[i].addressOf);
                    emit sendData(
                        sellList[i].dataAccess,
                        sellList[i].addressOf,
                        msg.sender,
                        block.timestamp
                    );
                    _amount = 0;
                    //update sellList
                    //if(sellList[i].amount == 0){
                    //    internalRemoveSellOder(i);
                    //}
                    return _amount;
                } else if (sellList[i].amount < _amount) {
                    //transfer tokens
                    buyerHolding[msg.sender] -=
                        _amount *
                        sellList[i].limitPrice;
                    IERC777(token).send(
                        sellList[i].addressOf,
                        (_amount * sellList[i].limitPrice),
                        ""
                    );
                    //from buyer to seller sellList[i].amount*sellList[i].limitPrice
                    addPartner(sellList[i].addressOf);
                    //from buyer to seller _amount*sellList[i].limitPrice userHolding[sellList[i].addressOf] to userHolding[msg.sender]
                    emit sendData(
                        sellList[i].dataAccess,
                        sellList[i].addressOf,
                        msg.sender,
                        block.timestamp
                    );
                    //current price calculation
                    units = units + sellList[i].amount;
                    accumulated_price =
                        accumulated_price +
                        (sellList[i].limitPrice * sellList[i].amount);
                    _amount = _amount - sellList[i].amount;
                    //sellList[i].amount == 0;
                    //internalRemoveSellOder(i);
                    if (_amount == 0) {
                        current_price = accumulated_price / units;
                        return _amount;
                    }
                    //if(sellList.length == 0){
                    //    current_price = accumulated_price/units;
                    //    return _amount;
                    //}
                    i--;
                }
            } else if (
                sellList[i].limitPrice <= _limitPrice &&
                sellList[i].addressOf == msg.sender &&
                checkPartner(sellList[i].addressOf) == true
            ) {
                if (sellList.length == 1) {
                    return _amount;
                } else {
                    i--;
                }
            } else {
                return _amount;
            }
        }
        return _amount; //NO TRADE with entry -> no price change
    }

    function getIndexBuyList(uint256 _price) internal view returns (uint256 i) {
        for (i = 0; i < buyList.length; ) {
            if (buyList[i].limitPrice >= _price) {
                i++;
            } else {
                return i;
            }
        }
    }

    function checkBuyer(address _check) internal view returns (bool listed) {
        if (buyList.length == 0) {
            return false;
        }
        for (uint256 i = 0; i <= buyList.length - 1; i++) {
            if (buyList[i].addressOf == _check) {
                return true;
            }
        }
        return false;
    }

    function removeYourBuyOrder() public returns (uint256) {
        require(buyList.length > 0, "no Order places yet");
        require(checkBuyer(msg.sender) == true, "no order from you places yet");
        //withdraw contract holdings to buyer
        IERC777(token).send(msg.sender, buyerHolding[msg.sender], "");
        buyerHolding[msg.sender] = 0;
        for (uint256 i = 0; i <= buyList.length - 1; i++) {
            if (buyList[i].addressOf == msg.sender) {
                removeBuyOder(i);
                return i;
            }
        }
        return 0;
    }

    function removeBuyOder(uint256 _index) internal {
        Order storage copy = buyList[_index];
        require(_index < buyList.length, "index to high");
        require(
            checkBuyer(msg.sender) == true,
            "place an order before you can remove it"
        );
        require(copy.addressOf == msg.sender, "only buyer can remove order");
        //withdraw Buyer UserHoldings to back to buyer safed in userHolding[msg.sender]
        for (uint256 i = _index; i < buyList.length - 1; i++) {
            buyList[i] = buyList[i + 1];
        }
        buyList.pop();
    }

    function internalRemoveBuyOder(uint256 _index) internal {
        require(_index < buyList.length, "index to high");
        IERC777(token).send(
            buyList[_index].addressOf,
            buyerHolding[buyList[_index].addressOf],
            ""
        );
        buyerHolding[buyList[_index].addressOf] = 0;
        for (uint256 i = _index; i < buyList.length - 1; i++) {
            buyList[i] = buyList[i + 1];
        }
        buyList.pop();
    }

    function getBuyOrder(uint256 _index)
        public
        view
        returns (
            uint256,
            uint256,
            uint256,
            uint256,
            address
        )
    {
        require(buyList.length > 0, "No Buy Orders in this Orderbook");
        require(
            _index <= buyList.length - 1,
            "No entry in the buy side of the orderbook, index too high"
        );
        Order storage i = buyList[_index];
        require(i.addressOf != address(0), "no such order"); // not exists
        return (i.id, i.limitPrice, i.amount, i.entryTime, i.addressOf);
    }

    //Regrister past Trades
    function addPartner(address _tradedWith) internal {
        tradePartners[msg.sender].push(_tradedWith);
    }

    function addPartnerToBuyer(address _tradedWith) internal {
        tradePartners[_tradedWith].push(msg.sender);
    }

    function removePartner(address _tradedNoMore) public {
        int256 index = checkPartnerIndex(_tradedNoMore);
        require(index >= 0, "not a recent trading partner");
        if (index >= 0) {
            uint256 indexUint = uint256(index);
            tradePartners[msg.sender][indexUint] = tradePartners[msg.sender][
                tradePartners[msg.sender].length - 1
            ];
            tradePartners[msg.sender].pop();
        }
    }

    function getPartner(uint256 _index) public view returns (address) {
        address trader = tradePartners[msg.sender][_index];
        return trader;
    }

    function checkPartner(address _check) public view returns (bool traded) {
        if (tradePartners[msg.sender].length == 0) {
            return false;
        }
        for (uint256 i = 0; i <= tradePartners[msg.sender].length - 1; i++) {
            if (_check == tradePartners[msg.sender][i]) {
                return true;
            }
        }
        return false;
    }

    function checkPartnerBuyer(address _check)
        public
        view
        returns (bool traded)
    {
        if (tradePartners[_check].length == 0) {
            return false;
        }
        for (uint256 i = 0; i <= tradePartners[_check].length - 1; i++) {
            if (_check == tradePartners[_check][i]) {
                return true;
            }
        }
        return false;
    }

    function checkPartnerIndex(address _check) internal view returns (int256) {
        int256 index = -1;
        for (uint256 i = 0; i <= tradePartners[msg.sender].length - 1; i++) {
            if (_check == tradePartners[msg.sender][i]) {
                index = int256(i);
                return index;
            }
        }
        return index;
    }

    //Additional test functions
    function getBalanceBuyer() public view returns (uint256) {
        return buyerHolding[msg.sender];
    }
}
