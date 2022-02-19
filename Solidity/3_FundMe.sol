// SPDX-License-Identifier: MIT

pragma solidity >= 0.6.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {

    mapping(address => uint) public addressToAmount;

    address owner;
    address[] funders;
    constructor() public {

        owner = msg.sender;
    }

    function fund() public payable {

        uint min = 50 * 10 ** 18;

        if (getConversionRate(msg.value) < min)
            revert("You need to spend more ETH");

        addressToAmount[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns(uint) {

        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
);
        return priceFeed.version();
    }

    function getPrice() public view returns(uint) {

        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
);
        (
            uint80 roundID, 
            int price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        return uint(price * 10000000000);
    }

    function getConversionRate(uint ethAmount) public view returns(uint) {

        uint ethPrice = getPrice();
        uint USD = (ethPrice * ethAmount)/1000000000000000000;
        return USD;
    }

    modifier onlyOwner {

        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner{
        payable(msg.sender).transfer(address(this).balance);

        for (uint funderIndex = 0; funderIndex < funders.length; funderIndex ++) {

            address funder = funders[funderIndex];
            addressToAmount[funder] = 0;
        }

        funders = new address[](0);
    }
}
