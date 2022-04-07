
from scripts.deploy import deployShinobi

from brownie import Shinobi, network, config, web3
from scripts.global_helpful_script import get_account

from scripts.tests.box_test import test_8, investor_account

from scripts.fight import fight
eth_to_usd = config["networks"][network.show_active()]["eth_usd_price_feed"]

# ---------------------    Tests ------------------
# 1: test if player can claim less than 50dollar=> no
# 2: test if player can claim before 10 days of last claim  =>no
# 3: test if player can claim without pay fees =>no
# 4: test if player balance change after claim  >=yes

def test_3(): # --- done ---
    shinobi = Shinobi[-1]
    test_pay_fees()
    claim = shinobi.claim({"from":investor_account})
    claim.wait(1)


def test_3(): # ---- Done ---
    shinobi = Shinobi[-1]
    fight()
    claim = shinobi.claim({"from":investor_account})
    claim.wait(1)
    
def test_2():#- ---- Done ----
    shinobi = Shinobi[-1]
    test_pay_fees()
    claim = shinobi.claim({"from":investor_account})
    claim.wait(1)

def test_1(): # ---- Done ---
    shinobi = Shinobi[-1]
    fight()
    claim = shinobi.claim({"from":investor_account})
    claim.wait(1)

def test_pay_fees():
    print("paying fees ..")
    shinobi = Shinobi[-1]
    fight()
    balanceBefore =  shinobi.playerBalance(investor_account.address)
    feesBefore = shinobi.fightDamageFee(investor_account.address)
    print("balance before ",balanceBefore)
    print("fees before ", feesBefore)
    payFees = shinobi.payeFees({"from":investor_account})
    payFees.wait(1)
    balanceAfter =  shinobi.playerBalance(investor_account.address)
    feesAfter = shinobi.fightDamageFee(investor_account.address)
    print("balance after ",balanceAfter)
    print("fees after ", feesAfter)
    
def test_pay_fees2():
    print("paying fees ..")
    shinobi = Shinobi[-1]
    account = get_account()
    balanceBefore =  shinobi.playerBalance(account.address)
    feesBefore = shinobi.fightDamageFee(account.address)
    print("balance before ",balanceBefore)
    print("fees before ", feesBefore)
    payFees = shinobi.payeFees({"from":account})
    payFees.wait(1)
    balanceAfter =  shinobi.playerBalance(account.address)
    feesAfter = shinobi.fightDamageFee(account.address)
    print("balance after ",balanceAfter)
    print("fees after ", feesAfter)

def main():
    deployShinobi()
    #test_1()
    #test_pay_fees()
    test_2()


    
