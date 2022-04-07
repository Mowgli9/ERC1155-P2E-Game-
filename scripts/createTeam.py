
from brownie import Shinobi, network, config, web3
from scripts.deploy import deployShinobi
from scripts.global_helpful_script import get_account
from scripts.tests.box_test import test_8, investor_account
from scripts.Shinobi import openTheBox

eth_to_usd = config["networks"][network.show_active()]["eth_usd_price_feed"]


def createTeam2():
    account =get_account()
    shinobi = Shinobi[-1]
    createTeamFee = shinobi.getBoxPrice(10 * 10 ** 18)
    shinobi_1_struct = shinobi.shinobis(0)
    shinobi_2_struct = shinobi.shinobis(1)
    shinobi_3_struct = shinobi.shinobis(2)
    shinobis = (shinobi_1_struct, shinobi_2_struct, shinobi_3_struct)
    if len(shinobis) < 3 or len(shinobis) > 5:
        print("3 shinobis mini and 5 max")
    else:
        if shinobi.canTeamUp(shinobis) == False:
            print("One of shinobis are already in team or banned")
        else:
            create = shinobi.createTeam(
                "Mowgli",
                shinobis,
                {"from": account, "value": createTeamFee},
            )
            create.wait(1)
            id = create.events["TeamCreated"]["id"]
            owner = create.events["TeamCreated"]["owner"]
            name = create.events["TeamCreated"]["name"]
            createdAt = create.events["TeamCreated"]["createdAt"]
            totalChakra = create.events["TeamCreated"]["totalChakra"]
            totalMembre = create.events["TeamCreated"]["totalMembre"]
            print(
                f"team : {name} id :{id} Chakra :{totalChakra} Members {totalMembre} has been created by {owner} at {createdAt}"
            )
            print(shinobi.TeamMapping(0,0))
            print(shinobi.TeamMapping(0,1))
            print(shinobi.TeamMapping(0,2))


def createTeam():
    shinobi = Shinobi[-1]
    test_8()
    openTheBox(0, investor_account)
    openTheBox(1, investor_account)
    openTheBox(2, investor_account)
    createTeamFee = shinobi.getBoxPrice(10 * 10 ** 18)
    shinobi_1_struct = shinobi.shinobis(0)
    shinobi_2_struct = shinobi.shinobis(1)
    shinobi_3_struct = shinobi.shinobis(2)
    shinobis = (shinobi_1_struct, shinobi_2_struct, shinobi_3_struct)
    if len(shinobis) < 3 or len(shinobis) > 5:
        print("3 shinobis mini and 5 max")
    else:
        if shinobi.canTeamUp(shinobis) == False:
            print("One of shinobis are already in team or banned")
        else:
            create = shinobi.createTeam(
                "Mowgli",
                shinobis,
                {"from": investor_account, "value": createTeamFee},
            )
            create.wait(1)
            id = create.events["TeamCreated"]["id"]
            owner = create.events["TeamCreated"]["owner"]
            name = create.events["TeamCreated"]["name"]
            createdAt = create.events["TeamCreated"]["createdAt"]
            totalChakra = create.events["TeamCreated"]["totalChakra"]
            totalMembre = create.events["TeamCreated"]["totalMembre"]
            print(
                f"team : {name} id :{id} Chakra :{totalChakra} Members {totalMembre} has been created by {owner} at {createdAt}"
            )
            print(shinobi.TeamMapping(0,0))
            print(shinobi.TeamMapping(0,1))
            print(shinobi.TeamMapping(0,2))


def changeCombo():
    shinobi = Shinobi[-1]
    change = shinobi.changeCombo(
                0,
                {"from": investor_account},
            )
    change.wait(1)
    print(shinobi.TeamMapping(0,0))
    print(shinobi.TeamMapping(0,1))
    print(shinobi.TeamMapping(0,2))


def getTotalTeams():
    shinobi = Shinobi[-1]
    total  = shinobi.getTotalTeams()
    print(f"Total Teams : {total}")


def main():
    deployShinobi()
    createTeam()
    getTotalTeams()
    changeCombo()
    getTotalTeams()
