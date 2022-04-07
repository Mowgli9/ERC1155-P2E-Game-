// contracts/Shinobi.sol
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

// you might see I use -- box -- or --- shinobi --- because it's two nft so I want to be more organized

contract Shinobi is ERC1155, Ownable,VRFConsumerBase {
    // ------------BOX Var ----
    uint256 public currentBoxMinted; // number of minted boxes
    uint256 public investorsTime;
    uint256 public deployedAt;
    uint256 investorFee;
    address[] public investors;
    address[] public whiteListed;
    mapping(uint256 => BOX_RARITY) public BoxRarity;
    mapping(address => uint256) public InvestorHolds;
    mapping(address => uint256) public whiteListedHolds;
    mapping(address => uint256) public playerHolds;
    mapping(uint256 => BOX_RARITY) public BoxRarityIndex;
    mapping(bytes32 => BOX_RARITY) public BoxRarityOfRequestId;
    mapping(bytes32 => uint) public requestIdToShinobiId;
    mapping(bytes32 => address) public RequestIdToOwner;
    mapping(BOX_RARITY => uint256) public BoxPrice;
    mapping(uint256 => BOX_STATUS) public BoxStatus;
    mapping(address => uint256) public InvestorsBalance;
    mapping(bytes32 => uint) public requestIdToBoxId;
    AggregatorV3Interface internal priceFeed; // price Feed see oracle Chainlink

    // ----------- Shinobi -------

    uint256 public currentShinobiMinted;
    uint256 public createTeamfee;
    uint256 currentTeamCreated;
    mapping(uint256 => mapping(uint256 => SHINOBI)) public TeamMapping; // first uint team id second uint structArray Id wiche is shinobi id will give you shinobi struct

    // --------------- Player ---------
    mapping(address => uint256) public LastClaim; // last claim
    mapping(address => uint256) public playerBalance; // user balance
    mapping(address => uint256) public fightDamageFee; // fees
    IERC20 public ryo;

    // ----- VRF ---
    uint256 internal fee;
    bytes32 internal keyHash;

    event BoxMinted(
        address indexed owner,
        uint256 box_id,
        uint256 time,
        uint256 price,
        BOX_RARITY rarity
    );
    event ShinobiBorn(
        address indexed owner,
        uint256 id,
        SHINOBI_RARITY rarity,
        uint256 time,
        uint256 chakra
    );
    event FeesPaid(address indexed player, uint256 amountPaied, uint256 time);
    event ClaimSuccefully(
        address indexed player,
        uint256 amountClaimed,
        uint256 time
    );
    event openBoxRequested(bytes32 requestId);
    event investorAdded(address indexed investor, uint256 time);
    event FightFinished(
        address indexed player,
        uint256 teamId,
        bool isWin,
        uint256 time
    );
    // main Charat of Shinobi NFt

    struct SHINOBI {
        uint256 id;
        address owner;
        uint256 bornDate;
        bool ban;
        SHINOBI_RARITY shinobi_rarity;
        uint256 chakra;
        uint256 lvl;
        uint256 lastFight;
        bool isInTeam;
    }

    SHINOBI[] public shinobis;

    // shinovbi rarity

    enum SHINOBI_RARITY {
        academy_Student,
        genin,
        chunin,
        tokubetsu_jonin,
        jonin,
        kage
    }

    // ------------------- Team ----------

    // team struct
    struct TEAM {
        uint256 id;
        string name;
        uint256 totalChakra;
        uint256 createdAt;
        address owner;
        uint256 mappingId;
        uint256 totalMembre;
        uint256 lastFightTime;
    }
    TEAM[] public teams;
    event TeamCreated(
        uint256 indexed id,
        address owner,
        string name,
        uint256 createdAt,
        uint256 totalChakra,
        uint256 totalMembre
    );

    // --------------------   Boxes ------------

    // struct of a Box

    struct BOX {
        uint256 id;
        address owner;
        uint256 mintedTime;
        bool ban;
        BOX_STATUS box_status;
        BOX_RARITY box_rarity;
    }

    BOX[] public boxes;

    // rarity
    enum BOX_RARITY {
        common,
        epic,
        legendary
    }

    // Open / Closed

    enum BOX_STATUS {
        not_used,
        used
    }

    // Who can buy now Investor / Whiteliste / Public

    enum WHO_CAN_BUY_NOW {
        investor,
        whiteliste,
        public_sale
    }
    WHO_CAN_BUY_NOW public who_can_buy_now;

    constructor(
        address _priceFeed,
        address ryoAddress,
        bytes32 _keyhash,
        address _vrf_coordinator,
        address _linkToken
    ) ERC1155("") VRFConsumerBase(_vrf_coordinator, _linkToken){
        keyHash = _keyhash;
        fee = 0.1 * 10**18;
        ryo = IERC20(ryoAddress);
        createTeamfee = 10 * 10**18;
        investorFee = 250 * 10**18;
        priceFeed = AggregatorV3Interface(_priceFeed);
        BoxPrice[BOX_RARITY.common] = 50;
        BoxPrice[BOX_RARITY.epic] = 100;
        BoxPrice[BOX_RARITY.legendary] = 150;
        deployedAt = block.timestamp; // now date
        // we will have the access to rarity using this mapping
        BoxRarityIndex[0] = BOX_RARITY.common;
        BoxRarityIndex[1] = BOX_RARITY.epic;
        BoxRarityIndex[2] = BOX_RARITY.legendary;
    }

    // return wich groups can buy now investors / whitelisted / public

    function whoCanBuyNow() public {
        if (block.timestamp <= deployedAt + 5 days) {
            who_can_buy_now = WHO_CAN_BUY_NOW.investor;
        } else if (
            block.timestamp >= deployedAt + 15 days &&
            block.timestamp < deployedAt + 25 days
        ) {
            who_can_buy_now = WHO_CAN_BUY_NOW.whiteliste;
        } else {
            who_can_buy_now = WHO_CAN_BUY_NOW.public_sale;
        }
    }

    // is investor => return true if the player is an investor

    function isInvestor(address _player) public view returns (bool) {
        for (uint256 i = 0; i < investors.length; i++) {
            if (investors[i] == _player) {
                return true;
            }
        }
        return false;
    }

    // isWhiteListed => returns true if the player whitelisted

    function isWhiteListed(address _player) public view returns (bool) {
        for (uint256 i = 0; i < whiteListed.length; i++) {
            if (whiteListed[i] == _player) {
                return true;
            }
        }
        return false;
    }

    // public sale

    function isAnyOneCanBuy() public view returns (bool) {
        if (block.timestamp > deployedAt + 25 days) {
            return true;
        } else {
            return false;
        }
    }

    // using chainlink node t get price in Eth in Etheruem and matic on polygon and bnb Binance
    // take 1 parametre  price and it's returns price in network tokens.

    function getBoxPrice(uint256 _price) public view returns (uint256) {
        (, int256 price, , , ) = priceFeed.latestRoundData();

        uint256 newPrice = uint256(price * 10**10);
        return ((_price * 10**18) / newPrice);
    }

    // buy common box buy intering index of wiche rarity
    function mintBox(uint256 _boxRarityIndex) public payable {
        whoCanBuyNow();
        BOX_RARITY boxrarity = BoxRarityIndex[_boxRarityIndex]; // get rarity
        if (who_can_buy_now == WHO_CAN_BUY_NOW.investor) {
            // investor time
            uint256 box_price = BoxPrice[boxrarity] - 15; // new price for investor
            uint256 boxPriceEth = getBoxPrice(box_price); // get this price in eth
            require(currentBoxMinted < 3332, "only 3333 for investors"); // only 3333 box for investor
            require(
                isInvestor(msg.sender) == true, // must be investor
                "wait public sale your're not investor"
            );
            require(msg.value >= boxPriceEth, "Not enough"); // value must be great or equal price
            require(
                InvestorHolds[msg.sender] < 9, // max hold for each investor is 10
                "You can't hold more than 10"
            );
            // Box overview
            boxes.push(
                BOX({
                    id: currentBoxMinted,
                    ban: false,
                    owner: msg.sender,
                    box_status: BOX_STATUS.not_used,
                    box_rarity: boxrarity,
                    mintedTime: block.timestamp
                })
            );
            _mint(msg.sender, currentBoxMinted, 1, ""); // minting 1 NFT erc 1155
            InvestorHolds[msg.sender] += 1; // increment
            currentBoxMinted += 1; // increment
            emit BoxMinted( // event
                msg.sender,
                currentBoxMinted - 1, // current box minted
                block.timestamp,
                msg.value,
                boxrarity
            );

            // same info but this time for whitelist
        } else if (who_can_buy_now == WHO_CAN_BUY_NOW.whiteliste) {
            uint256 box_price = BoxPrice[boxrarity] - 10;
            uint256 boxPriceEth = getBoxPrice(box_price);
            require(currentBoxMinted < 7776, "only 7777 for whiteliste");
            require(
                isWhiteListed(msg.sender) == true,
                "wait public sale your're not whitelisted"
            );
            require(msg.value >= boxPriceEth, "Not enough");
            require(
                whiteListedHolds[msg.sender] < 9,
                "You can't hold more than 10"
            );
            _mint(msg.sender, currentBoxMinted, 1, "");
            boxes.push(
                BOX({
                    id: currentBoxMinted,
                    ban: false,
                    owner: msg.sender,
                    box_status: BOX_STATUS.not_used,
                    box_rarity: boxrarity,
                    mintedTime: block.timestamp
                })
            );
            whiteListedHolds[msg.sender] += 1;
            currentBoxMinted += 1;
            emit BoxMinted(
                msg.sender,
                currentBoxMinted - 1,
                block.timestamp,
                msg.value,
                boxrarity
            );

            // Pre-sale end
        } else if (who_can_buy_now == WHO_CAN_BUY_NOW.public_sale) {
            uint256 box_price = BoxPrice[boxrarity];
            uint256 boxPriceEth = getBoxPrice(box_price);
            require(msg.value >= boxPriceEth, "Not enough");
            _mint(msg.sender, currentBoxMinted, 1, "");
            boxes.push(
                BOX({
                    id: currentBoxMinted,
                    ban: false,
                    owner: msg.sender,
                    box_status: BOX_STATUS.not_used,
                    box_rarity: boxrarity,
                    mintedTime: block.timestamp
                })
            );
            playerHolds[msg.sender] += 1;
            currentBoxMinted += 1;
            emit BoxMinted(
                msg.sender,
                currentBoxMinted - 1,
                block.timestamp,
                msg.value,
                boxrarity
            );
        }
    }

    //                  Shinobi -------

    // open a  box and see the rarity
    // you need to have one box mini
    // you need to be the owner of th box
    // the box must be never used.


    function openBox(uint _boxId) public {
        BOX memory box = boxes[_boxId];
        require(box.box_status == BOX_STATUS.not_used, "Box empty"); // change it
        require(box.owner == msg.sender, "You are not the owner");
        bytes32 requestId = requestRandomness(keyHash, fee); // you can see chainlink documentation
        BoxRarityOfRequestId[requestId] = box.box_rarity;
        RequestIdToOwner[requestId] = msg.sender;
        requestIdToShinobiId[requestId] = _boxId;
        requestIdToBoxId[requestId] = _boxId;
        emit openBoxRequested(requestId);
    }


    // this function require focus and auto-mind complete hhhh ...



    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
        {
        address owner = RequestIdToOwner[requestId];
        uint _boxId = requestIdToBoxId[requestId];
        BOX storage box = boxes[_boxId];
        uint256 chancePercentage = randomness % 100;
        SHINOBI_RARITY shinobiRarity;
        uint256 _chakra;
        if (box.box_rarity == BOX_RARITY.common) {
            if (chancePercentage > 41) {
                shinobiRarity = SHINOBI_RARITY.academy_Student;
            } else if (chancePercentage > 21 && chancePercentage <= 41) {
                shinobiRarity = SHINOBI_RARITY.genin;
            } else if (chancePercentage > 11 && chancePercentage <= 21) {
                shinobiRarity = SHINOBI_RARITY.chunin;
            } else if (chancePercentage > 4 && chancePercentage <= 11) {
                shinobiRarity = SHINOBI_RARITY.tokubetsu_jonin;
            } else if (chancePercentage > 1 && chancePercentage <= 4) {
                shinobiRarity = SHINOBI_RARITY.jonin;
            } else if (chancePercentage == 1) {
                shinobiRarity = SHINOBI_RARITY.kage;
            }
        } else if (box.box_rarity == BOX_RARITY.epic) {
            if (chancePercentage > 64) {
                shinobiRarity = SHINOBI_RARITY.academy_Student;
            } else if (chancePercentage > 39 && chancePercentage <= 64) {
                shinobiRarity = SHINOBI_RARITY.genin;
            } else if (chancePercentage > 19 && chancePercentage <= 39) {
                shinobiRarity = SHINOBI_RARITY.chunin;
            } else if (chancePercentage > 4 && chancePercentage <= 19) {
                shinobiRarity = SHINOBI_RARITY.tokubetsu_jonin;
            } else if (chancePercentage > 1 && chancePercentage <= 4) {
                shinobiRarity = SHINOBI_RARITY.jonin;
            } else if (chancePercentage == 1) {
                shinobiRarity = SHINOBI_RARITY.kage;
            }
        } else if (box.box_rarity == BOX_RARITY.legendary) {
            if (chancePercentage > 83) {
                shinobiRarity = SHINOBI_RARITY.genin;
            } else if (chancePercentage > 43 && chancePercentage <= 83) {
                shinobiRarity = SHINOBI_RARITY.chunin;
            } else if (chancePercentage > 13 && chancePercentage <= 43) {
                shinobiRarity = SHINOBI_RARITY.tokubetsu_jonin;
            } else if (chancePercentage > 5 && chancePercentage <= 13) {
                shinobiRarity = SHINOBI_RARITY.jonin;
            } else if (chancePercentage == 1 && chancePercentage <= 5) {
                shinobiRarity = SHINOBI_RARITY.kage;
            }
        }
        if (shinobiRarity == SHINOBI_RARITY.academy_Student) {
            _chakra = (randomness % 30) + 30;
        } else if (shinobiRarity == SHINOBI_RARITY.genin) {
            _chakra = (randomness % 40) + 61;
        } else if (shinobiRarity == SHINOBI_RARITY.chunin) {
            _chakra = (randomness % 100) + 81;
        } else if (shinobiRarity == SHINOBI_RARITY.tokubetsu_jonin) {
            _chakra = (randomness % 119) + 181;
        } else if (shinobiRarity == SHINOBI_RARITY.jonin) {
            _chakra = (randomness % 200) + 301;
        } else if (shinobiRarity == SHINOBI_RARITY.kage) {
            _chakra = (randomness % 200) + 801;
        }

        box.box_status = BOX_STATUS.used; // delete it
        _mint(owner, box.id, 1, "");
        shinobis.push(
            SHINOBI({
                id: box.id,
                owner: owner,
                bornDate: block.timestamp,
                ban: false,
                shinobi_rarity: shinobiRarity,
                chakra: _chakra,
                lvl: 1,
                lastFight: 0,
                isInTeam: false
            })
        );
        emit ShinobiBorn(
            owner,
            box.id,
            shinobiRarity,
            block.timestamp,
            _chakra
        );
    }

    //           - ----- get shinobi stats -----
    function shinobiOverview(uint256 _id)
        public
        view
        returns (
            uint256,
            address,
            uint256,
            bool,
            SHINOBI_RARITY,
            uint256,
            uint256,
            uint256,
            bool
        )
    {
        SHINOBI memory shinobi = shinobis[_id];
        return (
            shinobi.id,
            shinobi.owner,
            shinobi.bornDate,
            shinobi.ban,
            shinobi.shinobi_rarity,
            shinobi.chakra,
            shinobi.lvl,
            shinobi.lastFight,
            shinobi.isInTeam
        );
    }

    // ----------- can create team -----
    // require no shinobi is already on team and no one is banned

    function canTeamUp(SHINOBI[] memory _shinobis) public view returns (bool) {
        for (uint256 i = 0; i < _shinobis.length; i++) {
            SHINOBI memory _shinobi = _shinobis[i];
            if (_shinobi.isInTeam == true || _shinobi.ban == true) {
                return false;
            }
        }
        return true;
    }

    //              ------------- Team --------

    function createTeam(string memory _name, SHINOBI[] memory _shinobis)
        public
        payable
    {
        require(_shinobis.length >= 3, "3 mini required"); //3 is the minx
        require(_shinobis.length <= 5, "5 max "); // 5 is the max
        require(
            canTeamUp(_shinobis) == true,
            "Already in team or banned Sinobi"
        ); // not already in team no is banned
        require(
            msg.value >= getBoxPrice(createTeamfee),
            "10 dollar for create a team"
        );

        uint256 _totalChakra = 0;

        for (uint256 i = 0; i < _shinobis.length; i++) {
            SHINOBI memory _shinobi = _shinobis[i];
            _shinobi.isInTeam = true;
            _totalChakra += _shinobi.chakra; // get chakra of each shinobi
            TeamMapping[currentTeamCreated][_shinobi.id] = _shinobi;
            shinobis[i] = _shinobi;
        }
        // add a team

        teams.push(
            TEAM({
                id: currentTeamCreated,
                createdAt: block.timestamp,
                name: _name,
                owner: msg.sender,
                totalChakra: _totalChakra,
                mappingId: currentTeamCreated,
                totalMembre: _shinobis.length,
                lastFightTime: 0
            })
        );

        currentTeamCreated += 1;

        emit TeamCreated(
            currentTeamCreated - 1,
            msg.sender,
            _name,
            block.timestamp,
            _totalChakra,
            _shinobis.length
        );
    }

    // remove Team wihtout loosing NFTs just in case player want to change Combo
    // if player want to change combo he need to pay again when he want to create team again

    function changeCombo(uint256 teamId) public {
        TEAM memory team = teams[teamId];
        require(team.id == teamId, "team doesn't exist");
        require(team.owner == msg.sender, "you're not the owner");
        require(
            team.lastFightTime + 24 hours <= block.timestamp,
            "you can change team only after 24h after fight"
        );

        for (uint256 i = 0; i < team.totalMembre; i++) {
            SHINOBI storage member;
            member = TeamMapping[teamId][i];
            member.isInTeam = false;
            TeamMapping[teamId][i] = member;
        }
        require(team.id < teams.length, "index out of bound");

        for (uint256 i = team.id; i < teams.length - 1; i++) {
            teams[i] = teams[i + 1];
        }
        teams.pop();
    }

    function fight(uint256 teamId, uint256 enemyIdex) public {
        TEAM storage team = teams[teamId];
        require(enemyIdex <= 5, "index out of bound");
        require(team.id == teamId, "team doesn't exist");
        require(team.owner == msg.sender, "you're not the owner");
        require(
            team.lastFightTime + 24 hours <= block.timestamp,
            "you can fight only once every 24h"
        );
        if (LastClaim[msg.sender] == 0) {
            LastClaim[msg.sender] = block.timestamp;
        }
        if (enemyIdex == 0) {
            fightWithSasori(msg.sender, team);
        } else if (enemyIdex == 1) {
            fightWithKakuzu(msg.sender, team);
        } else if (enemyIdex == 2) {
            fightWithDeidara(msg.sender, team);
        } else if (enemyIdex == 3) {
            fightWithHidan(msg.sender, team);
        } else if (enemyIdex == 4) {
            fightWithKonan(msg.sender, team);
        } else if (enemyIdex == 5) {
            fightWithPain(msg.sender, team);
        }
    }

    // how to calculte win chance teamChakra / EnmyChakra * 100

    // low lvl random avoid paying link fees
    function _createRandomNum() internal view returns (uint256) {
        uint256 randomNum = uint256(
            keccak256(
                abi.encodePacked(block.timestamp, msg.sender, block.gaslimit)
            )
        );
        return randomNum % 100;
    }

    //                  -----fights-----
    function fightWithSasori(address owner, TEAM storage team) private {
        require(team.totalChakra >= 200, "200 chakra mini");
        // low lvl random but it's enough
        uint256 winChance = (team.totalChakra / 250) * 100;
        if (_createRandomNum() <= winChance) {
            playerBalance[owner] += 10;
            emit FightFinished(owner, team.id, true, block.timestamp);
        }
        fightDamageFee[owner] += 1;
        team.lastFightTime = block.timestamp;
        emit FightFinished(owner, team.id, false, block.timestamp);
    }

    function fightWithKakuzu(address owner, TEAM storage team) private {
        require(team.totalChakra >= 420, "420 chakra mini");
        // low lvl random but it's enough
        uint256 winChance = (team.totalChakra / 500) * 100;
        if (_createRandomNum() <= winChance) {
            playerBalance[owner] += 20;
            emit FightFinished(owner, team.id, true, block.timestamp);
        }
        fightDamageFee[owner] += 2;
        team.lastFightTime = block.timestamp;
        emit FightFinished(owner, team.id, false, block.timestamp);
    }

    function fightWithDeidara(address owner, TEAM storage team) private {
        require(team.totalChakra >= 680, "680 chakra mini");
        // low lvl random but it's enough
        uint256 winChance = (team.totalChakra / 750) * 100;
        if (_createRandomNum() <= winChance) {
            playerBalance[owner] += 30;
            emit FightFinished(owner, team.id, true, block.timestamp);
        }
        fightDamageFee[owner] += 3;
        team.lastFightTime = block.timestamp;
        emit FightFinished(owner, team.id, false, block.timestamp);
    }

    function fightWithHidan(address owner, TEAM storage team) private {
        require(team.totalChakra >= 900, "900 chakra mini");
        // low lvl random but it's enough
        uint256 winChance = (team.totalChakra / 1000) * 100;
        if (_createRandomNum() <= winChance) {
            playerBalance[owner] += 40;
            emit FightFinished(owner, team.id, true, block.timestamp);
        }
        fightDamageFee[owner] += 4;
        team.lastFightTime = block.timestamp;
        emit FightFinished(owner, team.id, false, block.timestamp);
    }

    function fightWithKonan(address owner, TEAM storage team) private {
        require(team.totalChakra >= 1100, "1100 chakra mini");
        // low lvl random but it's enough
        uint256 winChance = (team.totalChakra / 1250) * 100;
        if (_createRandomNum() <= winChance) {
            playerBalance[owner] += 50;
            emit FightFinished(owner, team.id, true, block.timestamp);
        }
        fightDamageFee[owner] += 5;
        team.lastFightTime = block.timestamp;
        emit FightFinished(owner, team.id, false, block.timestamp);
    }

    function fightWithPain(address owner, TEAM storage team) private {
        require(team.totalChakra >= 1300, "1300 chakra mini");
        // low lvl random but it's enough
        uint256 winChance = (team.totalChakra / 1500) * 100;
        if (_createRandomNum() <= winChance) {
            playerBalance[owner] += 60;
            emit FightFinished(owner, team.id, true, block.timestamp);
        }
        fightDamageFee[owner] += 6;
        team.lastFightTime = block.timestamp;
        emit FightFinished(owner, team.id, false, block.timestamp);
    }

    // get total Box minted
    function getTotalBoxes() public view returns (uint256) {
        return boxes.length;
    }

    // get total shinobi
    function getTotalShinobi() public view returns (uint256) {
        return shinobis.length;
    }

    // get total team
    function getTotalTeams() public view returns (uint256) {
        return teams.length;
    }

    // -------------- Claim----------
    // before claim player must have no fees
    // player last claim must great than 10 days
    // require 50  dollar minimum to withdraw
    // - 5 % every claim
    // for claim will give the player for every dollar 1 ryo

    function claim() public {
        require(fightDamageFee[msg.sender] == 0, "pay fees before claim");
        require(
            LastClaim[msg.sender] + 10 days <= block.timestamp,
            "You can't claim now"
        );
        require(playerBalance[msg.sender] >= 50, "50 dollar mini required");
        uint256 newplayerBalance = playerBalance[msg.sender];
        uint256 taxe = (newplayerBalance * 5) / 100;
        playerBalance[msg.sender] = 0;
        LastClaim[msg.sender] = block.timestamp;
        ryo.transfer(msg.sender, (newplayerBalance * 10**18) - taxe);
        emit ClaimSuccefully(
            msg.sender,
            (newplayerBalance * 10**18) - taxe,
            block.timestamp
        );
    }

    // -----------  Paye Feess (fight Damage) --------
    // player need to paye it from his balance;

    function payeFees() public {
        uint256 playerNewBalance = playerBalance[msg.sender];
        uint256 feesToPay = fightDamageFee[msg.sender];
        require(playerNewBalance > feesToPay, "not enough");
        playerBalance[msg.sender] -= feesToPay;
        fightDamageFee[msg.sender] = 0;
    }

    // add investor : # need to fix

    function addInvestor(address _address) public onlyOwner {
        require(investors.length < 550, "only 550 investor");
        investors.push(_address);
    }

    // add whiteliste # need to fix

    function addWhitelisted(address _address) public onlyOwner {
        whiteListed.push(_address);
    }

    // be an ivestor
    function beInvestor() public payable {
        require(InvestorsBalance[msg.sender] == 0, "you're already investor");
        require(investors.length < 550, "only 550 investor");
        require(getBoxPrice(investorFee) <= msg.value, "250 dollar minimum");
        investors.push(msg.sender);
        InvestorsBalance[msg.sender] += 250;
        emit investorAdded(msg.sender, block.timestamp);
    }

    // investor can claim his funds after 5 days

    function getInvestementBack() public {
        require(InvestorsBalance[msg.sender] >= 250, "you're not investor");
        require(
            deployedAt + 5 days <= block.timestamp,
            "You need to wait more"
        );
        uint256 amount = InvestorsBalance[msg.sender];
        InvestorsBalance[msg.sender] -= 250;
        ryo.transfer(msg.sender, (amount * 10**18));
    }


    // get eth from contract 

    function getEthBack() public onlyOwner {
        address owner = payable(owner());
        uint balance = address(this).balance;
        (bool sent,) = owner.call{value:balance}("");
        require (sent ,"failed to send eth ");
    }

    function getLinkBack() public onlyOwner{
        address owner = payable(owner());
        uint balance = LINK.balanceOf(address(this));
        LINK.transfer(owner,balance);
        
    }
}
