
from scripts.deploy import deployShinobi,fund_contract_with_ryo
from scripts.global_helpful_script import fund_with_link, get_account
from scripts.Box import addInvestor,mintBox
from scripts.Shinobi import openTheBox
from scripts.createTeam import createTeam2
from scripts.fight import fight2
from scripts.claim import claim2
from brownie import Shinobi,config,network



link_address = config["networks"][network.show_active()]["link_address"]

# def game():
#     account = get_account()
#     deployShinobi()
#     fund_with_link(shinobi.address,link_address,account)
#     fund_contract_with_ryo()
#     addInvestor()
#     mintBox()

#     openTheBox(0,account)
#     openTheBox(1,account)
#     openTheBox(2,account)
#     createTeam2()
#     fight2()
#     claim2()


def withdraw():
    account = get_account()
    shinobi = Shinobi[-1]
    get =shinobi.getEthBack({"from":account})
    get.wait(1)


def getLink():
    account = get_account()
    shinobi = Shinobi[-1]
    get =shinobi.getLinkBack({"from":account})
    get.wait(1)



def get():
    shinobi = Shinobi[-1]
    print( shinobi.boxes(1))

def interacting():
    account = get_account()
    shinobi = Shinobi[-1]
    fight2()
    
    






def main():
    # interacting()
   interacting()