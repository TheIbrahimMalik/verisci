# 🔬 VeriSci – Scientific Claim Credibility Engine

**Agent → SpoonOS → LLM → Tooling → Neo (stub)**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://verisci.streamlit.app)

---

## 🧠 Overview

**VeriSci** is an **AI-powered scientific verification agent** designed to evaluate the credibility of natural-language scientific claims with transparency and auditability.

Built for the **Scoop AI Hackathon**, VeriSci demonstrates how an AI agent can be constructed using **SpoonOS** to deliver structured reasoning, tool invocation, and an on-chain pathway for long-term trust records.

Given any natural-language scientific claim, VeriSci produces a verifiable output:

* A **credibility score (0–100)**
* A **confidence label** (low, medium, high)
* A **short explanation** of the verdict
* A set of **key contributing factors**
* A **deterministic claim hash** for storage/on-chain indexing

This system satisfies all baseline technical requirements for entry into Hackathon judging.

---

## 🏗️ System Architecture

### 1. Agent Layer (Python)

**Located in:** `agent/verisci_agent.py`

The agent is the central orchestrator, performing the following key actions:

* **Claim hashing** using SHA-256
* **LLM evaluation** through the **SpoonOS LLMManager**
* Intelligent fallback to the OpenAI Chat Completions API if the SpoonOS provider fails
* Structured result normalisation and validation
* **Storage** via a custom SpoonOS Tool (`StoreEvaluationTool`)
* Forwarding of the result to a **Neo blockchain submission stub**

This demonstrates a complete vertical flow from **Agent → LLM → Tools → Blockchain**.

---

### 🔌 LLM Invocation Flow (SpoonOS + Fallback)

The agent prioritizes the use of SpoonOS to satisfy hackathon requirements but ensures reliability with a robust three-tier fallback mechanism:

1.  **Primary Path:** Agent → SpoonOS LLMManager → OpenAI Provider
2.  **Fallback 1 (Reliability):** If the SpoonOS adapter raises a `ProviderError` (due to current instability with missing `role` or `tool_calls` attributes), the agent executes a **direct OpenAI call**.
3.  **Fallback 2 (Deterministic Fail-safe):** If the direct API call fails, the agent produces a **deterministic stub response**.

This guarantees the agent always produces valid JSON, ensuring the pipeline and live demo never break.

---

### 🧰 Custom Spoon Tool: `StoreEvaluationTool`

**Located in:** `agent/verisci_agent.py`

This official SpoonOS Tool implementation satisfies the second baseline requirement for tool usage:

* Implements `BaseTool` from SpoonOS.
* Defines structured, JSON-schema parameters.
* Writes results to a persistent local file: `data/verisci_store.json`.
* Provides basic error handling and logs each action for transparency.

---

### 🔗 Neo Blockchain Integration (Stub)

**Located in:** `contracts/ClaimRegistry.py`

A smart contract skeleton for the Neo blockchain is provided. The contract defines the core functions needed for on-chain trust records:

* `submitClaim(claim_hash, score, confidence, explanation)`
* `getClaim(claim_hash)`

In the agent, the function `submit_to_neo_stub(...)` shows exactly where a **real RPC call** would occur when deployed to the Neo TestNet. This clearly demonstrates the intended **on-chain pathway** without requiring full deployment during the hackathon.

---

## 🌐 Web UI (Streamlit Frontend)

The live web interface is the public face of the project, allowing judges and users to test the system directly without installing anything.

* **Located at:** `ui/app.py`
* **Hosted Live:** **https://verisci.streamlit.app**
* **Features:** Clean text input, live LLM-backed evaluation, display of structured results, and claim hash.
* **Mobile-friendly** layout.

---

## 🧪 Example Output

**Input:** *"All apples are green."*

**Output (JSON Snippet):**

```json
{
  "score": 10,
  "confidence": "high",
  "explanation": "The claim that all apples are green is scientifically inaccurate, as apples can come in a variety of colours including red, yellow, and even bi-coloured varieties.",
  "factors": [
    "Apples exist in multiple colours.",
    "Genetic variation among apple cultivars.",
    "Colour changes during ripening."
  ]
}
```

**Deterministic Hash:**

`dc937665de797b4612608b6c14d5394eb2191f00ca483a0332aee64fb2a6d9b4`

---

## 📊 What the Score Means

VeriSci uses a **0–100 scientific credibility score**:

| Score Range | Meaning |
| :--- | :--- |
| **0** | Contradicts scientific consensus or established facts. |
| **50** | Uncertain, ambiguous, or highly context-dependent. |
| **100** | Strongly supported by scientific evidence and widely accepted. |

Combined with the **confidence value**, this forms a compact trust signal suitable for on-chain storage.

---

## 📁 Repository Structure
It looks like the previous content ended right after the "Deterministic Hash" example and has the subsequent sections partially formatted or as plain text. I'll reformat and combine all the remaining content into the correct README.md structure, starting from the "What the Score Means" section.

Markdown

**Deterministic Hash:**

`dc937665de797b4612608b6c14d5394eb2191f00ca483a0332aee64fb2a6d9b4`

---

## 📊 What the Score Means

VeriSci uses a **0–100 scientific credibility score**:

| Score Range | Meaning |
| :--- | :--- |
| **0** | Contradicts scientific consensus or established facts. |
| **50** | Uncertain, ambiguous, or highly context-dependent. |
| **100** | Strongly supported by scientific evidence and widely accepted. |

Combined with the **confidence value**, this forms a compact trust signal suitable for on-chain storage.

---

## 📁 Repository Structure

```json
verisci/
│
├── agent/
│ └── verisci_agent.py # Main agent, LLM logic, Tool, Neo stub
│
├── contracts/
│ └── ClaimRegistry.py # Neo smart-contract skeleton
│
├── ui/
│ └── app.py # Streamlit front-end
│
├── data/
│ └── verisci_store.json # Created dynamically by the Tool
│
├── docs/ # Additional documentation for judges
│
└── README.md # This file (You are here)
```

---

## 🚀 Future Work

We plan to significantly extend VeriSci's capabilities post-hackathon:

* **Neo Integration:** Full deployment of `ClaimRegistry` to **Neo TestNet** and implementation of **RPC-based contract invocation** from the agent for true on-chain submission.
* **Grounded Claims:** Implementation of **Evidence retrieval** (literature search, RAG pipelines) to provide factual grounding for all claims and explanations.
* **Graph Scoring:** Development of **Cross-claim graph scoring** to detect claim clusters, consensus trends, and identify conflicts across multiple submissions.
* **Accessibility:** Creation of a **Browser extension** for real-time credibility detection as users browse scientific articles.
* **Richer Tooling:** Integration of advanced SpoonOS modules for identity, compliance, and security checks.

---

## 🧾 Licence

Copyright 2025 TheIbrahimMalik.