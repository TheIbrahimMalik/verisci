# VeriSci – On-chain Scientific Verification Agent

VeriSci is an AI-powered scientific verification agent designed to bring transparency, auditability, and trust to scientific information.

## Architecture (High-Level)

- **Agent & Orchestration:** Python-based agent built on SpoonOS
- **LLM Invocation (Baseline Requirement 1):** SpoonOS unified LLM protocol (Agent → SpoonOS → LLM) using `LLMManager`
- **Tooling (Baseline Requirement 2):** Custom SpoonOS tool (`StoreEvaluationTool`, subclass of `BaseTool`) to handle storage/logging of evaluations, demonstrating full tool invocation with basic error handling
- **Blockchain:** Neo, with a `ClaimRegistry` smart contract for on-chain scores
- **Interface:** CLI (for the hackathon demo), with potential UI or web front-end extension

## Current Status

- Implemented `verisci_agent.py`:
  - Hashes scientific claims to deterministic identifiers
  - Invokes an LLM via SpoonOS (`LLMManager.chat(...)`) to generate a credibility score, confidence label, explanation and factors
  - Invokes a SpoonOS tool (`StoreEvaluationTool`) to handle storing/logging evaluation results keyed by claim hash
  - Includes a Neo submission stub (`submit_to_neo_stub`) that clearly indicates how the agent would call the `ClaimRegistry` smart contract

- Created `ClaimRegistry` Neo smart contract skeleton:
  - `submitClaim(claim_hash, score, confidence, explanation)`
  - `getClaim(claim_hash)`

- SpoonOS agent/workflow config scaffolded in `agent/spoonos.yaml`

- Next steps (beyond hackathon prototype):
  - Deploy `ClaimRegistry` to Neo testnet and replace the stub with a real RPC call
  - Introduce persistent storage (database or decentralised storage) behind `StoreEvaluationTool`
  - Build a minimal web or terminal UI for non-technical users
