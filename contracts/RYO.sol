// contracts/RYO.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Ryo is ERC20 {
    constructor() ERC20("RYO", "RYO") {
        _mint(msg.sender, 100000000 *10**18);
    }
}