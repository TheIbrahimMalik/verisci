# VeriSci – On-chain Scientific Verification Agent

VeriSci is an AI-powered scientific verification agent designed to bring transparency, auditability, and trust to scientific information.

## Architecture (High-Level)

- **Agent & Orchestration:** SpoonOS
- **LLM Invocation:** SpoonOS unified LLM protocol (Agent → SpoonOS → LLM)
- **Tooling:** SpoonOS Storage Tool (KV) to persist intermediate results and agent state
- **Blockchain:** Neo, with a `ClaimRegistry` smart contract for on-chain scores
- **Interface:** CLI (for the hackathon demo), with potential UI extension

## Current Status

- Implemented `verisci_agent.py`:
  - Hashes scientific claims
  - Invokes an LLM via SpoonOS to generate a credibility score, confidence label, explanation and factors
  - Uses SpoonOS Storage Tool (KVStorage) to store results by claim hash
- Created `ClaimRegistry` Neo smart contract skeleton:
  - `submitClaim(claim_hash, score, confidence, explanation)`
  - `getClaim(claim_hash)`
- SpoonOS agent/workflow config scaffolded in `agent/spoonos.yaml`
- Next steps:
  - Deploy `ClaimRegistry` to Neo testnet
  - Wire the agent to submit results on-chain
  - Build a minimal web or terminal UI for demo