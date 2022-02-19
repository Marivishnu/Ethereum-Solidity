// SPDX-License-Identifier: MIT

pragma solidity > 0.6.0;

import "./1_SimpleStorage.sol";

contract StorageFactory {

    SimpleStorage[] public simpleStorageArray;

    function createSimpleStorageContract() public {

        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorageArray.push(simpleStorage);
    }

    function sfStore(uint index, uint number) public {

        SimpleStorage simpleStorage = SimpleStorage(address(simpleStorageArray[index]));
        simpleStorage.store(number);
    }

    function sfRetrieve(uint index) public view returns(uint) {

        SimpleStorage simpleStorage = SimpleStorage(address(simpleStorageArray[index]));
        uint result = simpleStorage.retrieve();
        return result;
    }
}
