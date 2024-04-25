// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;
 
contract HelloWorld {
    function say_hello() external pure returns(string memory) {
        return "Hello World!";
    }

    function add(uint256 a, uint256 b) public pure returns(uint256) {
        return a + b;
    }

    function times2(uint256 a) external pure returns(uint256) {
        return a * 2;
    }

    function echo(string calldata a) external pure returns(string memory) {
        return a;
    }
}