function priceMatchingNewSellOrder(
    uint256 _limitPrice,
    uint256 _amount,
    string memory _dataAccess
) internal returns (uint256) {
    uint256 units = 0;
    uint256 accumulated_price = 0;
    for (uint256 i = buyList.length - 1; i >= 0; i--) {
        //trade happens if price matches, seller and buyer address no the same, parters didn't trade yet
        if (
            buyList[i].limitPrice >= _limitPrice &&
            buyList[i].addressOf != msg.sender &&
            checkPartnerBuyer(buyList[i].addressOf) == false
        ) {
            if (buyList[i].amount >= _amount) {
                //last or single trade
                update amont of buyList[i]
                //current price calculation
                units = units + _amount;
                accumulated_price =
                    accumulated_price +
                    (buyList[i].limitPrice * _amount);
                current_price = accumulated_price / units;
                //transfer tokens
                reduce deposit of the buyer
                send tokens from deposit to the seller via IERC777(CitSciToken).send
                send data via event emition
                regrister trade so no multiple trades can happen multiple times between the same parties
                remove Buy order from list if amount = 0
                retrun //trade end
            } else if (buyList[i].amount < _amount) {
                //multiiple trades
                
                regrister trade so no multiple trades can happen multiple times between the same parties
                send data via event emition
                reduce deposit of the buyer
                send tokens from deposit to the seller via IERC777(CitSciToken).send
                //current price calculation
                current price calculation
                remove buy Order from the list
            }
        } else {
            no more matching parter found
            return //trade end 
        }
    }
    return //trade end
}

    function withdrawEarningSeller() public {
        uint256 currentTime = block.timestamp;
        uint256 totalAmount = 0;
        uint256 remainingTime;
        uint256 remaingIntervalls;
        uint256 timeToPayout;
        uint256 payoutIntervals;
        for (uint256 i = 0; i <= tradePartners[msg.sender].length - 1; i++) {
            uint256 endStream = tradePartners[msg.sender][i].endDataOfStream;
            uint256 startStream = tradePartners[msg.sender][i]
                .startDataOfStream;
            uint256 agreedPrice = tradePartners[msg.sender][i].agreedPrice;
            uint256 agreedAmount = tradePartners[msg.sender][i].agreedAmount;
            remainingTime = endStream - startStream;
            remaingIntervalls = remainingTime / streamingInterval;
            if (currentTime >= endStream) {
                totalAmount = remaingIntervalls * agreedPrice * agreedAmount;
                buyerHolding[
                    tradePartners[msg.sender][i].streamingTo
                ] -= totalAmount;
                sellerHolding[msg.sender] += totalAmount;
                removePartner(i);
                if (tradePartners[msg.sender].length == 0) {
                    break;
                }
            } else {
                timeToPayout = currentTime - startStream;
                if (timeToPayout < streamingInterval) {} else {
                    uint256 modulo = timeToPayout % streamingInterval;
                    timeToPayout = timeToPayout - modulo;
                    tradePartners[msg.sender][i]
                        .startDataOfStream += timeToPayout;
                    payoutIntervals = timeToPayout / streamingInterval;
                    totalAmount = payoutIntervals * agreedPrice * agreedAmount;
                    buyerHolding[
                        tradePartners[msg.sender][i].streamingTo
                    ] -= totalAmount;
                    sellerHolding[msg.sender] += totalAmount;
                    if (
                        tradePartners[msg.sender][i].startDataOfStream >=
                        endStream
                    ) {
                        removePartner(i);
                        if (tradePartners[msg.sender].length == 0) {
                            break;
                        }
                    }
                }
            }
        }
        uint256 amoutToSend = sellerHolding[msg.sender];
        IERC777(token).send(msg.sender, amoutToSend, "");
        sellerHolding[msg.sender] = 0;
    }