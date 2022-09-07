// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface InterfaceERC7772 {
    event TokensReceived(
        address sender,
        address operator,
        address from,
        address to,
        uint256 amount,
        bytes userData,
        bytes operatorData
    );

    event TokensToSend(
        address sender,
        address operator,
        address from,
        address to,
        uint256 amount,
        bytes userData,
        bytes operatorData
    );
}
