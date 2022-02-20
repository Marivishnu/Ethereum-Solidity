// SPDX-License-Identifier: MIT

pragma solidity >0.6.0;

contract SimpleStorage {
    uint256 myNumber;

    function store(uint256 number) public {
        myNumber = number;
    }

    //view makes that function not to change the state of the ethereum network
    function retrieve() public view returns (uint256) {
        return myNumber;
    }

    //pure function cannot read or modify the state variables
    function pureFunction() public pure returns (uint256 product, uint256 sum) {
        product = 10 * 20;
        sum = 10 + 20;
    }

    struct People {
        uint256 number;
        string name;
    }

    //People public people = People({number: 2, name: "Marivishnu"});
    People[] public people;

    //mapping to map one variable to another
    mapping(string => uint256) public nameToNumber;

    function addPeople(uint256 number, string memory name) public {
        people.push(People({number: number, name: name}));
        //people.push(People(number, name)); since number is defined first in struct it denotes 0th index and name is the 1st index. Passing parameter must also follow the indexing.
        nameToNumber[name] = number;
    }
}
