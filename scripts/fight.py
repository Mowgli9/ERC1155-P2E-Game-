
from scripts.global_helpful_script import (
 
    get_account

)
from brownie import Shinobi, network, config, web3

from scripts.tests.box_test import  investor_account
from scripts.deploy import deployShinobi
from scripts.createTeam import createTeam

eth_to_usd = config["networks"][network.show_active()]["eth_usd_price_feed"]

def fight2():
    account = get_account()
    shinobi = Shinobi[-1]
    enmies = {"Sasori": 0, "Kakuzu": 1, "Deidara": 2, "Hidan": 3, "Konan": 4, "Pain": 5}
    enemy_choice = enmies["Sasori"]
    team_id = 0  # must exist otehrwsise returns revert
    # requirement =  no fight last 24h, be the owner , team di must exist,enemy index must be less or equal 5
    fighting = shinobi.fight(
        team_id, enemy_choice, {"from": account}
    )  # change paramters to be exast as tests
    fighting.wait(1)
    print("Fight finished")
    print(
        f"player :{account.address} has now {shinobi.playerBalance(account.address)}"
    )
    print(
        f"player :{account.address} need to pay fees {shinobi.fightDamageFee(account.address)}"
    )
    owner = fighting.events["FightFinished"]["player"]
    teamId=fighting.events["FightFinished"]["teamId"]
    win=fighting.events["FightFinished"]["isWin"]
    time=fighting.events["FightFinished"]["time"]
    phrase = ""
    if win == True:
        phrase = "Win the fight "
    else :
        phrase = "loose the fight"
    print(f"Player : {owner} with team Id :{teamId} {phrase}  at {time}")



def fight():
    shinobi = Shinobi[-1]
    createTeam()
    enmies = {"Sasori": 0, "Kakuzu": 1, "Deidara": 2, "Hidan": 3, "Konan": 4, "Pain": 5}
    enemy_choice = enmies["Sasori"]
    team_id = 0  # must exist otehrwsise returns revert
    # requirement =  no fight last 24h, be the owner , team di must exist,enemy index must be less or equal 5
    fighting = shinobi.fight(
        team_id, enemy_choice, {"from": investor_account}
    )  # change paramters to be exast as tests
    fighting.wait(1)
    print("Fight finished")
    print(
        f"player :{investor_account.address} has now {shinobi.playerBalance(investor_account.address)}"
    )
    print(
        f"player :{investor_account.address} need to pay fees {shinobi.fightDamageFee(investor_account.address)}"
    )
    owner = fighting.events["FightFinished"]["player"]
    teamId=fighting.events["FightFinished"]["teamId"]
    win=fighting.events["FightFinished"]["isWin"]
    time=fighting.events["FightFinished"]["time"]
    phrase = ""
    if win == True:
        phrase = "Win the fight "
    else :
        phrase = "loose the fight"
    print(f"Player : {owner} with team Id :{teamId} {phrase}  at {time}")


def main():
    deployShinobi()
    fight()