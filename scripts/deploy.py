from scripts.global_helpful_script import (
    get_account,
  
)
from brownie import Shinobi, accounts, network, config, web3, Ryo,interface

eth_to_usd = config["networks"][network.show_active()]["eth_usd_price_feed"]
# matic_to_usd = config["networks"][network.show_active()]["matic_usd_price_feed"]
keyhash = config["networks"][network.show_active()]["key_hash"]
vrf = config["networks"][network.show_active()]["vrf_coordinator"]
link_address = config["networks"][network.show_active()]["link_address"]

def deployShinobi():
    account = get_account()
    # deploy the contract
    print("Deploying ...")
    _contract = Shinobi.deploy(eth_to_usd,deployRyo(),keyhash,vrf,link_address, {"from": account})
    print("Contract deployed ! ")


def deployRyo():
    print("deploying RYO ...")
    account = get_account()
    _contract = Ryo.deploy({"from":account})
    print("Deployed !")
    return _contract.address

# send ryo to contract

def fund_contract_with_ryo():
    print("Sending Token ...")
    account = get_account()
    ryo_contract = Ryo[-1]
    shinobi_contract = Shinobi[-1]
    total = ryo_contract.balanceOf(account.address)
    transfer = ryo_contract.transfer(shinobi_contract.address,total,{"from":account})
    transfer.wait(1)
    sender = transfer.events["Transfer"]["from"]
    to = transfer.events["Transfer"]["to"]
    amount = transfer.events["Transfer"]["value"]
    print(f"contract : {to} recieved from {sender} amount : {amount}")




def main():
    deployShinobi()
    