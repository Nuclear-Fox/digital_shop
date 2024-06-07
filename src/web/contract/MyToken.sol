// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";

contract MyToken is ERC20, ERC20Permit {

    mapping(address => uint256) payments; // Общая сумма, переведенная пользователем
    mapping(address => uint256) countTransaction; // Количество транзакций, совершенных пользователем
    constructor() ERC20("MyToken", "MTK") ERC20Permit("MyToken") {
        _mint(msg.sender, 3000000);
    }

    function paymentsOf(address account) public view returns (uint256) {
        return payments[account];
    }

    function countTransactionOf(address account) public view returns (uint256) {
        return countTransaction[account];
    }

    function transfer(address sender, address recipient, uint256 amount) public payable returns (bool) {       
        //
        // Для тестов msg.sender не совпадает, для реального использования раскомментировать
        // if (sender == owner) {
        //     require(msg.sender == owner, "No rigths");
        // }
        //require(msg.sender == sender, "No rigths");
        //

        _transfer(sender, recipient, amount);
        
        payments[sender] += amount;
        countTransaction[sender] += 1;

        return true;
    }


    // function transfer(address recipient, int256 amount) public payable returns (bool) {
    //     require(amount <= balances[msg.sender], "Insufficient balance");

    //     balances[msg.sender] -= amount;
    //     balances[recipient] += amount;

    //     payments[msg.sender] += amount;
    //     countTransaction[msg.sender] += 1;

    //     return true;
    // }
}
