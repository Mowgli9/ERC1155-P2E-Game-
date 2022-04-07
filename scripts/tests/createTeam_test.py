import random
import time
from scripts.global_helpful_script import (
    fund_with_link,
    get_account,
    get_rarity_box,
    listen_for_event,
    get_rarity_shinobi,
)
from brownie import Shinobi, network, config, web3
from web3 import Web3
from datetime import datetime
from scripts.tests.box_test import test_8, investor_account
from scripts.Shinobi import openTheBox

# ---------------- TEST ---------------
# 1 : test if can create team with more than 5 shinobis = > no
# 2 : test if can create team with 2 or less shinobis = > no
# 3 : test if can create team with  5 shinobis  => yes
# 4 : test if can create team with 3 shinobis = > yes
# 5 /6 : test if can create team with shinobis already in team or banned = > no

eth_to_usd = config["networks"][network.show_active()]["eth_usd_price_feed"]


def deployShinobi():
    account = get_account()  # get account
    # deploy the contract
    print("Deploying ...")
    shinobi_contract = Shinobi.deploy(eth_to_usd, {"from": account})
    print("Contract deployed ! ")

    # -------- Test 5 need test_6() when you want run the test tun the both------
def test_6():
    shinobi = Shinobi[-1]
    openTheBox(3, investor_account)
    openTheBox(4, investor_account)
    openTheBox(5, investor_account)
    shinobi_3_struct = shinobi.shinobis(1)
    shinobi_4_struct = shinobi.shinobis(4)
    shinobi_5_struct = shinobi.shinobis(5)
    create = shinobi.createTeam("Mowgli",(shinobi_3_struct,shinobi_4_struct,shinobi_5_struct),{"from":investor_account,"value":Web3.toWei(0.2,'ether')})
    create.wait(1)
    id = create.events["TeamCreated"]["id"]
    owner = create.events["TeamCreated"]["owner"]
    name = create.events["TeamCreated"]["name"]
    createdAt = create.events["TeamCreated"]["createdAt"]
    totalChakra = create.events["TeamCreated"]["totalChakra"]
    totalMembre = create.events["TeamCreated"]["totalMembre"]
    print(f"team : {name} id :{id} Chakra :{totalChakra} Members {totalMembre} has been created by {owner} at {createdAt}")

def test_5():
    shinobi = Shinobi[-1]
    test_8()
    openTheBox(0, investor_account)
    openTheBox(1, investor_account)
    openTheBox(2, investor_account)
    shinobi_1_struct = shinobi.shinobis(0)
    shinobi_2_struct = shinobi.shinobis(1)
    shinobi_3_struct = shinobi.shinobis(2)
    create = shinobi.createTeam("Mowgli",(shinobi_1_struct,shinobi_2_struct,shinobi_3_struct),{"from":investor_account,"value":Web3.toWei(0.2,'ether')})
    create.wait(1)
    id = create.events["TeamCreated"]["id"]
    owner = create.events["TeamCreated"]["owner"]
    name = create.events["TeamCreated"]["name"]
    createdAt = create.events["TeamCreated"]["createdAt"]
    totalChakra = create.events["TeamCreated"]["totalChakra"]
    totalMembre = create.events["TeamCreated"]["totalMembre"]
    print(f"team : {name} id :{id} Chakra :{totalChakra} Members {totalMembre} has been created by {owner} at {createdAt}")



def test_4(): # ---- Done ----
   
    shinobi = Shinobi[-1]
    test_8()
    openTheBox(0, investor_account)
    openTheBox(1, investor_account)
    openTheBox(2, investor_account)
    openTheBox(3, investor_account)
    openTheBox(4, investor_account)
    shinobi_1_struct = shinobi.shinobis(0)
    shinobi_2_struct = shinobi.shinobis(1)
    shinobi_3_struct = shinobi.shinobis(2)
    create = shinobi.createTeam("Mowgli",(shinobi_1_struct,shinobi_2_struct,shinobi_3_struct),{"from":investor_account,"value":Web3.toWei(0.2,'ether')})
    create.wait(1)
    id = create.events["TeamCreated"]["id"]
    owner = create.events["TeamCreated"]["owner"]
    name = create.events["TeamCreated"]["name"]
    createdAt = create.events["TeamCreated"]["createdAt"]
    totalChakra = create.events["TeamCreated"]["totalChakra"]
    totalMembre = create.events["TeamCreated"]["totalMembre"]
    print(f"team : {name} id :{id} Chakra :{totalChakra} Members {totalMembre} has been created by {owner} at {createdAt}")


def test_3(): # --------- Done --------
    shinobi = Shinobi[-1]
    test_8()
    openTheBox(0, investor_account)
    openTheBox(1, investor_account)
    openTheBox(2, investor_account)
    openTheBox(3, investor_account)
    openTheBox(4, investor_account)
    shinobi_1_struct = shinobi.shinobis(0)
    shinobi_2_struct = shinobi.shinobis(1)
    shinobi_3_struct = shinobi.shinobis(2)
    shinobi_4_struct = shinobi.shinobis(3)
    shinobi_5_struct = shinobi.shinobis(4)
    create = shinobi.createTeam("Mowgli",(shinobi_1_struct,shinobi_2_struct,shinobi_3_struct,shinobi_4_struct,shinobi_5_struct),{"from":investor_account,"value":Web3.toWei(0.2,'ether')})
    create.wait(1)
    id = create.events["TeamCreated"]["id"]
    owner = create.events["TeamCreated"]["owner"]
    name = create.events["TeamCreated"]["name"]
    createdAt = create.events["TeamCreated"]["createdAt"]
    totalChakra = create.events["TeamCreated"]["totalChakra"]
    totalMembre = create.events["TeamCreated"]["totalMembre"]
    print(f"team : {name} id :{id} Chakra :{totalChakra} Members {totalMembre} has been created by {owner} at {createdAt}")


def test_2(): # ------ Done ! ------
    shinobi = Shinobi[-1]
    test_8()
    openTheBox(0, investor_account)
    openTheBox(1, investor_account)
    shinobi_1_struct = shinobi.shinobis(0)
    shinobi_2_struct = shinobi.shinobis(1)
    create = shinobi.createTeam("Mowgli",(shinobi_1_struct,shinobi_2_struct),{"from":investor_account,"value":Web3.toWei(0.2,'ether')})
    create.wait(1)
    id = create.events["TeamCreated"]["id"]
    owner = create.events["TeamCreated"]["owner"]
    name = create.events["TeamCreated"]["name"]
    createdAt = create.events["TeamCreated"]["createdAt"]
    totalChakra = create.events["TeamCreated"]["totalChakra"]
    totalMembre = create.events["TeamCreated"]["totalMembre"]
    print(f"team : {name} id :{id} Chakra :{totalChakra} Members {totalMembre} has been created by {owner} at {createdAt}")

def test_1(): # ----- Done ----
    shinobi = Shinobi[-1]
    test_8()
    openTheBox(0, investor_account)
    openTheBox(1, investor_account)
    openTheBox(2, investor_account)
    openTheBox(3, investor_account)
    openTheBox(4, investor_account)
    openTheBox(5, investor_account)
    shinobi_1_struct = shinobi.shinobis(0)
    shinobi_2_struct = shinobi.shinobis(1)
    shinobi_3_struct = shinobi.shinobis(2)
    shinobi_4_struct = shinobi.shinobis(3)
    shinobi_5_struct = shinobi.shinobis(4)
    shinobi_6_struct = shinobi.shinobis(5)
    create = shinobi.createTeam("Mowgli",(shinobi_1_struct,shinobi_2_struct,shinobi_3_struct,shinobi_4_struct,shinobi_5_struct,shinobi_6_struct),{"from":investor_account,"value":Web3.toWei(0.2,'ether')})
    create.wait(1)
    id = create.events["TeamCreated"]["id"]
    owner = create.events["TeamCreated"]["owner"]
    name = create.events["TeamCreated"]["name"]
    createdAt = create.events["TeamCreated"]["createdAt"]
    totalChakra = create.events["TeamCreated"]["totalChakra"]
    totalMembre = create.events["TeamCreated"]["totalMembre"]
    print(f"team : {name} id :{id} Chakra :{totalChakra} Members {totalMembre} has been created by {owner} at {createdAt}")

def main():
    deployShinobi()
    #test_1()
    #test_2()
    #test_3()
    #test_4()
    # test_5()
    # test_6()