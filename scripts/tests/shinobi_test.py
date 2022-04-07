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


eth_to_usd = config["networks"][network.show_active()]["eth_usd_price_feed"]

# --------------- Var-----------
common_box_price = 100000 + Web3.toWei(50, "ether")
epic_box_price = 100000 + Web3.toWei(100, "ether")
legendary_box_price = 100000 + Web3.toWei(150, "ether")
normal_account = get_account()
other_account = get_account(1)
boxIndexing = {"common": 0, "epic": 1, "legendary": 2}
boxPricing = {0: common_box_price, 1: epic_box_price, 2: legendary_box_price}
userChoice = boxIndexing["epic"]


# --------------- Test -----------

# 1 : test if the other player can open othter's boxes = > no
# 2 : test if player can open his box => yes
# 3 : test if player can open the box twice = >no


# --------Deploy -------
def deployShinobi():
    account = get_account()  # get account
    # deploy the contract
    print("Deploying ...")
    shinobi_contract = Shinobi.deploy(eth_to_usd, {"from": account})
    print("Contract deployed ! ")

def test_3():
    addInvestor()
    amount_to_sent = getBoxPrice(boxPricing[userChoice])
    number = random.randint(
        1970986995652941011198306695860511804973345179954581845656239119030691489434,
        9970986995652941011198306695860511804973345179954581845656239119030691489434,
    )
    print(number)
    print("Opening the box")
    shinobi = Shinobi[-1]
    mintingBox(shinobi, userChoice, normal_account, amount_to_sent)
    openTheBox = shinobi.openBox(0, number, {"from": normal_account})
    openTheBox = shinobi.openBox(0, number, {"from": normal_account})
    openTheBox.wait(1)
    id = openTheBox.events["ShinobiBorn"]["id"]
    owner = openTheBox.events["ShinobiBorn"]["owner"]
    rarity = openTheBox.events["ShinobiBorn"]["rarity"]
    print(
        f"Player: {owner} mint a new Shinobi Id {id} rarity : {get_rarity_shinobi(rarity)}"
    )
    print(shinobi.shinobis(id))


def test_2(): #------ Done ! _---
    addInvestor()
    amount_to_sent = getBoxPrice(boxPricing[userChoice])
    number = random.randint(
        1970986995652941011198306695860511804973345179954581845656239119030691489434,
        9970986995652941011198306695860511804973345179954581845656239119030691489434,
    )
    print(number)
    print("Opening the box")
    shinobi = Shinobi[-1]
    mintingBox(shinobi, userChoice, normal_account, amount_to_sent)
    openTheBox = shinobi.openBox(0, number, {"from": normal_account})
    openTheBox.wait(1)
    id = openTheBox.events["ShinobiBorn"]["id"]
    owner = openTheBox.events["ShinobiBorn"]["owner"]
    rarity = openTheBox.events["ShinobiBorn"]["rarity"]
    print(
        f"Player: {owner} mint a new Shinobi Id {id} rarity : {get_rarity_shinobi(rarity)}"
    )
    print(shinobi.shinobis(id))

def test_1(): # ------ Done ! ----
    addInvestor()
    amount_to_sent = getBoxPrice(boxPricing[userChoice])
    number = random.randint(
        1970986995652941011198306695860511804973345179954581845656239119030691489434,
        9970986995652941011198306695860511804973345179954581845656239119030691489434,
    )
    print(number)
    print("Opening the box")
    shinobi = Shinobi[-1]
    mintingBox(shinobi, userChoice, normal_account, amount_to_sent)
    openTheBox = shinobi.openBox(0, number, {"from": other_account})
    openTheBox.wait(1)
    id = openTheBox.events["ShinobiBorn"]["id"]
    owner = openTheBox.events["ShinobiBorn"]["owner"]
    rarity = openTheBox.events["ShinobiBorn"]["rarity"]
    print(
        f"Player: {owner} mint a new Shinobi Id {id} rarity : {get_rarity_shinobi(rarity)}"
    )
    print(shinobi.shinobis(id))


# -------- miting process ----------
def mintingBox(box_contract, userChoice, account, amount_to_sent):
    print("Minting Your Box")
    mint__box = box_contract.mintBox(
        userChoice, {"from": account, "value": amount_to_sent}
    )
    mint__box.wait(1)
    owner = mint__box.events["BoxMinted"]["owner"]
    time = mint__box.events["BoxMinted"]["time"]
    box_id = mint__box.events["BoxMinted"]["box_id"]
    price = mint__box.events["BoxMinted"]["price"]
    rarity = mint__box.events["BoxMinted"]["rarity"]
    converted_time = datetime.fromtimestamp(time).strftime("%B,%d,%I:%M:%S")
    print(
        f"player : {owner} mint a new Box id {box_id} Rarity : {get_rarity_box(rarity)} Price :{Web3.fromWei(price,'ether')} Time : {converted_time} "
    )

# ------- get price in eth ----
def getBoxPrice(box_price):
    shinobi = Shinobi[-1]
    price = shinobi.getBoxPrice(box_price)
    return price

# --------- add investor ----
def addInvestor():
    print("Ading Investor")
    box_contract = Shinobi[-1]
    addInv = box_contract.addInvestor(
        normal_account.address, {"from": normal_account}
    )
    addInv.wait(1)


def main():
    deployShinobi()
    #test_1()
    #test_2()
    test_3()
