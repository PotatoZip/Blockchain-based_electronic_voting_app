// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract ElectionManager is Ownable {
    mapping(uint256 => mapping(uint256 => uint256)) public votesCount;
    mapping(bytes32 => bool) public hasVoted;

    event VoteCast(
        uint256 indexed electionId,
        uint256 indexed choiceId,
        bytes32 indexed voterKey
    );

    constructor(address owner_) Ownable(owner_) {}

    function markVotedAndCount(
        uint256 electionId,
        bytes32 voterKey,
        uint256 choiceId
    ) external onlyOwner {
        require(!hasVoted[voterKey], "Already voted");
        hasVoted[voterKey] = true;
        votesCount[electionId][choiceId] += 1;
        emit VoteCast(electionId, choiceId, voterKey);
    }

    function getChoiceCount(
        uint256 electionId,
        uint256 choiceId
    ) external view returns (uint256) {
        return votesCount[electionId][choiceId];
    }
}
