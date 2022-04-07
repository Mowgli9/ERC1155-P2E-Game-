from scripts.global_helpful_script import (
    get_account,
    get_rarity_box,
)
from brownie import Shinobi, network, config, web3
from web3 import Web3
from datetime import datetime
from scripts.deploy import deployShinobi
common_box_price = 100000 + Web3.toWei(50, "ether")
epic_box_price = 100000 + Web3.toWei(100, "ether")
legendary_box_price = 100000 + Web3.toWei(150, "ether")
eth_to_usd = config["networks"][network.show_active()]["eth_usd_price_feed"]
# matic_to_usd = config["networks"][network.show_active()]["matic_usd_price_feed"]




def intercating():
    addInvestor()
    mintBox()
   


# get BoxPrice using oracle system


def getBoxPrice(box_price):
    account = get_account()
    box_contract = Shinobi[-1]
    price = box_contract.getBoxPrice(box_price)
    # print(f"the Price is {Web3.fromWei(price,'ether')} etheruem")
    return price


# mint a Box with a lot of requires see the smart contract


def mintBox():
    account = get_account()
    box_contract = Shinobi[-1]
    boxIndexing = {"common": 0, "epic": 1, "legendary": 2}
    boxPricing = {0: common_box_price, 1: epic_box_price, 2: legendary_box_price}
    userChoice = boxIndexing["epic"]
    amount_to_sent = getBoxPrice(boxPricing[userChoice])
    if box_contract.who_can_buy_now() == 0:
        if box_contract.isInvestor(account.address) == False:
            print("wait public sale your're not investor")
        else:
            if box_contract.InvestorHolds(account.address) >= 10:
                print("You can't hold more")
            else:
                mintingBox(box_contract, userChoice, account, amount_to_sent)
    elif box_contract.who_can_buy_now() == 1:
        if box_contract.isWhiteListed(account.address) == False:
            print("wait public sale your're not whiteliste")
        else:
            if box_contract.whiteListedHolds(account.address) >= 10:
                print("You can't hold more")
            else:
                mintingBox(box_contract, userChoice, account, amount_to_sent)

    elif box_contract.who_can_buy_now() == 2:
        mintingBox(box_contract, userChoice, account, amount_to_sent)

    else:
        print("Something wrong here ! please contact developers")


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


def addInvestor():
    print("Ading Investor")
    account = get_account()
    box_contract = Shinobi[-1]
    addInv = box_contract.addInvestor(account.address, {"from": account})
    addInv.wait(1)
    print("Added")


def addWhitelist():
    print("Ading Whitelisted")
    account = get_account()
    box_contract = Shinobi[-1]
    addInv = box_contract.addWhiteliste(account.address, {"from": account})
    addInv.wait(1)


def main():
    deployShinobi()
    intercating()
