// contracts/OurToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

//importing the ERC777 Standard from Openzeppelin burn, balanceOf, totalSupply etc are included
import "@openzeppelin/contracts/token/ERC777/ERC777.sol";

contract CitSciToken is ERC777 {
    constructor(uint256 initialSupply, address[] memory defaultOperators)
        ERC777("SCToken", "SC", defaultOperators)
    {
        //Initial Suppy by deployment of the token
        _mint(msg.sender, initialSupply, "", "");
    }

    //making the mint function public and avaible to interact with it
    function increaseSupply(uint256 _amount) public {
        _mint(msg.sender, _amount, "", "");
    }
}
