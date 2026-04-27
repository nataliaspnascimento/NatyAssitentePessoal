// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./NatyStaking.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract NatyDAO is Ownable {
    NatyStaking public stakingContract;

    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
        mapping(address => bool) hasVoted;
    }

    Proposal[] public proposals;

    event ProposalCreated(uint256 proposalId, string description);
    event Voted(uint256 proposalId, address voter, uint256 weight);

    constructor(address _stakingContract, address _initialOwner) Ownable(_initialOwner) {
        stakingContract = NatyStaking(_stakingContract);
    }

    function createProposal(string memory description) external {
        uint256 proposalId = proposals.length;
        Proposal storage newProposal = proposals.push();
        newProposal.description = description;
        newProposal.executed = false;
        
        emit ProposalCreated(proposalId, description);
    }

    function vote(uint256 proposalId) external {
        Proposal storage proposal = proposals[proposalId];
        require(!proposal.hasVoted[msg.sender], "Already voted");
        
        uint256 weight = stakingContract.balanceOf(msg.sender);
        require(weight > 0, "No voting power (stake tokens first)");

        proposal.voteCount += weight;
        proposal.hasVoted[msg.sender] = true;

        emit Voted(proposalId, msg.sender, weight);
    }

    function getProposalCount() external view returns (uint256) {
        return proposals.length;
    }
}
