
from scripts.global_helpful_script import (

    get_account

)
from brownie import Shinobi, network, config, web3
from scripts.deploy import deployShinobi
from scripts.tests.box_test import test_8, investor_account

from scripts.createTeam import createTeam, getTotalTeams

eth_to_usd = config["networks"][network.show_active()]["eth_usd_price_feed"]

# ---------------------    Tests ------------------
# 1: test if player can fight with team have chakra less than required=> no
# 2: test if player can fight with team have lastfighttime<24h  =>no
# 3: test if player can fight with team have chakra plus or equial required =>yes
# 4: test if player can fight with team have lastfighttime >= 24h =>yes
# 5 : test if player can fight with another player's team => no




def test_5(): # ----- Done !- ---
    account = get_account()
    print("fighting ...")
    shinobi = Shinobi[-1]
    createTeam()
    fighting = shinobi.fight(
        0, 0, {"from": account}
    )  # change paramters to be exast as tests
    fighting.wait(1)
    print("Fight finished")
    print(
        f"player :{investor_account.address} has now {shinobi.playerBalance(investor_account.address)}"
    )
    print(
        f"player :{investor_account.address} need to pay fees {shinobi.fightDamageFee(investor_account.address)}"
    )

def test_4():  # ---- done
    test_1()


def test_3():  # - ---- Done ----
    test_1()


def test_2():  # ----------- Done !------------
    shinobi = Shinobi[-1]
    test_1()
    fighting = shinobi.fight(0, 0, {"from": investor_account})
    fighting.wait(1)
    print("Fight finished")
    print(
        f"player :{investor_account.address} has now {shinobi.playerBalance(investor_account.address)}"
    )
    print(
        f"player :{investor_account.address} need to pay fees {shinobi.fightDamageFee(investor_account.address)}"
    )


def test_1():  # ------ Done !------
    print("fighting ...")
    shinobi = Shinobi[-1]
    createTeam()
    fighting = shinobi.fight(
        0, 1, {"from": investor_account}
    )  # change paramters to be exast as tests
    fighting.wait(1)
    print("Fight finished")
    print(
        f"player :{investor_account.address} has now {shinobi.playerBalance(investor_account.address)}"
    )
    print(
        f"player :{investor_account.address} need to pay fees {shinobi.fightDamageFee(investor_account.address)}"
    )





def main():
    deployShinobi()
    # test_1()
    # test_2()
    # test_5()
 