// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Target {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function changeOwner(address _newOwner) public {
        if (tx.origin != msg.sender) {
            owner = _newOwner;
        }
    }

    function deposit() external payable {}

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw(uint256 _amount) external payable onlyOwner {
        require(_amount <= address(this).balance);
        payable(owner).transfer(_amount);
    }

    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
