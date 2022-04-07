
import random
from scripts.global_helpful_script import (
    get_account,
listen_for_event,
    get_rarity_shinobi
)
from brownie import Shinobi, network, config, web3
from scripts.deploy import deployShinobi
eth_to_usd = config["networks"][network.show_active()]["eth_usd_price_feed"]
from scripts.Box import addInvestor,mintBox

account = get_account()


def openTheBox(id,account):
    #number = random.randint(1970986995652941011198306695860511804973345179954581845656239119030691489434,9970986995652941011198306695860511804973345179954581845656239119030691489434)
    print("Opening the box")
    shinobi = Shinobi[-1]
    if shinobi.boxes(id)["box_status"] != 0 :
        print("Box empty")
    else :
        if shinobi.boxes(id)["owner"] != account.address:
            print("you're not the owner")
        else :
            openTheBox = shinobi.openBox(id,{"from":account})
            openTheBox.wait(1)
            print(listen_for_event(shinobi,"ShinobiBorn"))
            requestId = openTheBox.events["openBoxRequested"]["requestId"]
            idFromRequestId = shinobi.requestIdToShinobiId(requestId)
            the_shinobi = shinobi.shinobis(idFromRequestId)
            owner = shinobi.shinobis(idFromRequestId)["owner"]
            shinobi_rarity = shinobi.shinobis(idFromRequestId)["shinobi_rarity"]
            chakra = shinobi.shinobis(idFromRequestId)["chakra"]
            print(f"Player: {owner} mint a new Shinobi Id {the_shinobi} rarity : {get_rarity_shinobi(shinobi_rarity)} Chakra : {chakra}")
            

# def boxOverview():
#     shinobiId = 0
#     account = get_account()  # get account
#     shinobi = Shinobi[-1]
#     shinobi_overview = shinobi.boxes(0)
#     print(shinobi_overview)



def interacting():
    account2 = get_account(2)
    addInvestor()
    mintBox()
    openTheBox(0,account)
  





def main():
    deployShinobi()
    interacting()
