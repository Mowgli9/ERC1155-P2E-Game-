from operator import inv
import time
from scripts.deploy import deployShinobi,fund_contract_with_ryo

from brownie import Shinobi, accounts, network, config, web3
from web3 import Web3
from scripts.global_helpful_script import get_account
from scripts.tests.box_test import test_8, investor_account

from scripts.fight import fight
from scripts.tests.claim_test import test_pay_fees,test_pay_fees2

def claim2():
    shinobi = Shinobi[-1]
    test_pay_fees2()
    account = get_account()
    ten_days = 24*60*60*10
    if shinobi.fightDamageFee(account.address) > 0 :
        print("pay fees first ")
    else :
        if shinobi.playerBalance(account.address) <50:
            print("50 dollar mini")
        else :
            if shinobi.LastClaim(account.address) + ten_days >= time.time():
                print("You need to wait more")
            else :
                time.sleep(15)
                claim = shinobi.claim({"from":account})
                claim.wait(1)
                #ClaimSuccefully(address indexed player, uint amountClaimed, uint time);
                player = claim.events["ClaimSuccefully"]["player"]
                amountClaimed = claim.events["ClaimSuccefully"]["amountClaimed"]
                claimTime = claim.events["ClaimSuccefully"]["time"]
                print(f" Player :{player} has claimed {Web3.fromWei(amountClaimed,'ether')} at {claimTime}")



def claim():
    deployShinobi()
    fund_contract_with_ryo()
    shinobi = Shinobi[-1]
    test_pay_fees()
    ten_days = 24*60*60*10
    if shinobi.fightDamageFee(investor_account.address) > 0 :
        print("pay fees first ")
    else :
        if shinobi.playerBalance(investor_account.address) <50:
            print("50 dollar mini")
        else :
            if shinobi.LastClaim(investor_account.address) + ten_days >= time.time():
                print("You need to wait more")
            else :
                time.sleep(15)
                claim = shinobi.claim({"from":investor_account})
                claim.wait(1)
                #ClaimSuccefully(address indexed player, uint amountClaimed, uint time);
                player = claim.events["ClaimSuccefully"]["player"]
                amountClaimed = claim.events["ClaimSuccefully"]["amountClaimed"]
                claimTime = claim.events["ClaimSuccefully"]["time"]
                print(f" Player :{player} has claimed {Web3.fromWei(amountClaimed,'ether')} at {claimTime}")


def main():
    claim()