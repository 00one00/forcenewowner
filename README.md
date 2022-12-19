# Assume ownership of target contract

Disclaimer: This program is only intended for educational purposes on how to safe-guard your smart contracts from attacks. Hacking with the intent of stealing money is illegal and unethical.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Contract deployment and attack](#contract-deployment-and-attack)
* [How to avoid this kind of attack](#how-to-avoid-this-kind-of-attack)


## General info
The Target contract (We'll call it A) contains a loop-hole vulnerability that allows an adversary to obtain ownership of the contract. The vulnerability lies in the changeOwner() function of contract A, since tx.origin does not have to be msg.sender this function can be exploited. For example, if Bob sends a transaction to contract A (Bob --> A) Bob will be both the origin of the transaction (tx.origin) and msg.sender (the sender that initiated the transaction). However, if Bob sends a transaction to contract B (Bob --> B) and contract B sends a transaction to contract A (Bob --> B --> A), then Bob will still be tx.origin but not msg.sender, msg.sender will be contract B.
Since the changeOwner() function in our Target contracts condition requires the origin to NOT be the sender of the transaction we can merely deploy a simple contract to call on contract A, granting us ownership of contract A, this is where the CompromiseTarget (contract B) comes in. Contract B merely contains a constructor that passes in the contract address of contract A and calls the changeOwner() function of contract A upon deployment.


## Technologies
* Python v.3.11
* Brownie v.1.19.0
* Solidity v.0.8.15
* Web3py library v.5.0
* Infura Node API service


## Setup
To deploy the adversary contract, you will need to deploy on a testnet like goerli. If you are not familiar with deploying on a testnet there are many resourceful articles and guides. 
Within 'helpful_scripts.py' there is a get_accounts() function, this function is utilized several times in 'deploy_n_destroy.py' and is vital to being able to run the scripts. 
* If you do not want to run this function, simply substitute it for account = accounts[0] in the deploy() and deposit() functions and account = accounts[1] in the alpha() and withdraw() functions. 

Else, if you want to proceed with using the get_accounts() function, you will need to create a custom account within brownie accounts following the [Brownie docs](https://eth-brownie.readthedocs.io/en/stable/account-management.html) or you can import your private key within the .env file and then run '$source.env' in your terminal. 
Lastly, ensure you have gotten your Infura API key and pasted it into your .env file. If you are unfamiliar with Infura or Alchemy API keys or more generally nodes to connect to blockchains, find a resource online to brush up on this topic.


## Contract deployment and attack
Once you have all technologies installed, your accounts setup and the Infura API key imported, it's time to run the 'deploy_n_destroy.py' script, you are ready to deploy the contracts.

The first contract we need to deploy is the target contract; this will be the contract containing the vulnerability inside the changeOwner() function. 
To deploy contract A; in your terminal, run:

'$ brownie run scripts/deploy_n_destroy.py --network goerli'

A few things happened here; 
1. the Target contract was deployed and the msg.sender of the transaction is the owner of the contract. 
2. A deposit was made into the contract by the owner of the contract. 
3. The hacker contract was deployed and passed the Target contracts address into the constructor, allowing the creator of the 'CompromiseTarget' contract to be the new owner of 'Target'.  
4. Once the new owner has taken over, a withdraw has taken place, draining the desired amount of liquidity from the contract and into the attackers wallet. 


## How to avoid this kind of attack
This is a simple example and it's pretty likely that you aren't going to see a bug like this live in a production dapp, but stranger things have happened. All you can do is ensure that you do not make this critical mistake when writing your smart contracts. This could have been avoided simply by tacking the onlyOwner modifier onto the changeOwner() function, leaving out the require condition and keeping the statement simple with 'owner = _newOwner;'


I am always open to criticism and improving my code, feel free to reach out on twitter @nonfungible_kid or just give me a follow. Thanks for your support, stay safe out there!
