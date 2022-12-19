from brownie import accounts, config, network


DEVELOPMENT_NETWORKS = ["development"]
FORKED_ENVIRONMENTS = ["mainnet-fork-dev", "ganache-local"]


def get_account(index=None, id=None):
    """
    Get desired account to deploy contracts and run functions from.
    This function is used in most of the functions inside 'deploy_n_destroy.py'.

        Params:
            index:
                Takes in an integer of the desired account index you want to pull from.
                Use index when you are running on a development or local network.
                index=<desired account index>
            id:
                Takes in a string of a custom account you have created in brownie.
                This method is more secure than pulling from config["wallets"]["from_key"]
                and requires a password every time you run your scripts.
                id=<"test_acct_2">
    """
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])
