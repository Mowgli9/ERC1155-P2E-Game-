import time
from scripts.global_helpful_script import (
    fund_with_link,
    get_account,
    get_rarity_box,
    listen_for_event,
)
from brownie import Shinobi, network, config, web3
from web3 import Web3
from datetime import datetime
from scripts.deploy import deployShinobi

eth_to_usd = config["networks"][network.show_active()]["eth_usd_price_feed"]

# --------------- Var-----------
common_box_price = 100000 + Web3.toWei(50, "ether")
epic_box_price = 100000 + Web3.toWei(100, "ether")
legendary_box_price = 100000 + Web3.toWei(150, "ether")
normal_account = get_account()
investor_account = get_account() 
whitelist_account = get_account()
boxIndexing = {"common": 0, "epic": 1, "legendary": 2}
boxPricing = {0: common_box_price, 1: epic_box_price, 2: legendary_box_price}
userChoice = boxIndexing["epic"]

# in the contract replace 10 days by 1 min and 20 days by 2 mini

# 1 test if a normal person can mint box after deploy + 20 days = > No
# 2 test if an investor can mint box after deployement => yes
# 3 test if a whiteliste can mint box after deployement => no
# 4 test if a whiteliste can mint box between 10-20 after deployement => yes replace 10 days by 1mini and 20 days by 2min
# 5 test if normal person can buy after 20 days = > yes
# 6 test if investor can buy more than 10 = > no  ## change it to 3 just for testing
# 7 test if whiteliste can buy more than 10 =>no
# 8 test if investors can buy more than 3333 = > no ## change it to 3 just for testing
# 9 test if whitelist can buy more than 7777 = > no ## change it to 7 just for testing
# 10  test if investor can hold more than 10 after pre-sale

# -------------- Deploy -------------

def test_test():
    addInvestor()
    amount_to_sent = getBoxPrice(boxPricing[userChoice])
    shinobi = Shinobi[-1]
    for i in range(0,2):
        mintingBox(shinobi, userChoice, investor_account, amount_to_sent)
        print(shinobi.boxes(i)["owner"])
        print(shinobi.boxes(i)["id"])
        print(shinobi.boxes(i)["box_status"])

def test_10(): # -----  !-----
    addInvestor()
    amount_to_sent = getBoxPrice(boxPricing[userChoice])
    shinobi = Shinobi[-1]
    time.sleep(130)
    for i in range(0,15):
     mintingBox(shinobi, userChoice, investor_account, amount_to_sent)

def test_9(): #  ---- Done! ----
    addWhitelist()
    amount_to_sent = getBoxPrice(boxPricing[userChoice])
    shinobi = Shinobi[-1]
    time.sleep(66)
    for i in range(0,6):
     mintingBox(shinobi, userChoice, whitelist_account, amount_to_sent)

def test_8(): # ----- Done !-----
    addInvestor()
    amount_to_sent = getBoxPrice(boxPricing[userChoice])
    shinobi = Shinobi[-1]
    for i in range(0,3):
     mintingBox(shinobi, userChoice, investor_account, amount_to_sent)

def test_7(): #  ---- Done! ----
    addWhitelist()
    amount_to_sent = getBoxPrice(boxPricing[userChoice])
    shinobi = Shinobi[-1]
    time.sleep(66)
    for i in range(0,3):
     mintingBox(shinobi, userChoice, whitelist_account, amount_to_sent)

def test_6(): # ----- Done !-----
    addInvestor()
    amount_to_sent = getBoxPrice(boxPricing[userChoice])
    shinobi = Shinobi[-1]
    for i in range(0,3):
     mintingBox(shinobi, userChoice, investor_account, amount_to_sent)


def test_5(): # ----- Done !-----
    amount_to_sent = getBoxPrice(boxPricing[userChoice])
    shinobi = Shinobi[-1]
    time.sleep(130)
    mintingBox(shinobi, userChoice, normal_account, amount_to_sent)

# we need to add a whiteliet
def test_4():  # ------ Done ! -----
    addWhitelist()
    amount_to_sent = getBoxPrice(boxPricing[userChoice])
    shinobi = Shinobi[-1]
    time.sleep(66)
    mintingBox(shinobi, userChoice, whitelist_account, amount_to_sent)


def test_3():  # ----- Done ! -----
    addWhitelist()
    amount_to_sent = getBoxPrice(boxPricing[userChoice])
    shinobi = Shinobi[-1]
    mintingBox(shinobi, userChoice, whitelist_account, amount_to_sent)


# before do this test we need to add investor
def test_2():  # ------- done ! ---------
    addInvestor()
    amount_to_sent = getBoxPrice(boxPricing[userChoice])
    shinobi = Shinobi[-1]
    mintingBox(shinobi, userChoice, investor_account, amount_to_sent)


def test_1():  # ----- -Done ------

    amount_to_sent = getBoxPrice(boxPricing[userChoice])
    shinobi = Shinobi[-1]
    mintingBox(shinobi, userChoice, normal_account, amount_to_sent)


# ------------ get box price in eth --------


def getBoxPrice(box_price):
    shinobi = Shinobi[-1]
    price = shinobi.getBoxPrice(box_price)
    return price


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


# -------------- Add Investor----------
def addInvestor():
    print("Ading Investor")
    box_contract = Shinobi[-1]
    addInv = box_contract.addInvestor(
        investor_account.address, {"from": normal_account}
    )
    addInv.wait(1)


# ------ add whitelisted ---------
def addWhitelist():
    print("Ading Whitelisted")
    box_contract = Shinobi[-1]
    addInv = box_contract.addWhiteliste(
        whitelist_account.address, {"from": normal_account}
    )
    addInv.wait(1)


def main():
    deployShinobi()
    # test_1()
    # test_2()
    #test_3()
    #test_4()
    #test_5()
    #test_6()
    #test_7()
    #test_8()
    #test_9()
    #test_10()
    test_test()