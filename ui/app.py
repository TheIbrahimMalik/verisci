import os
import sys

# Ensure project root is on the Python path so 'agent' can be imported
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from agent.verisci_agent import evaluate_claim_with_spoon, hash_claim


import asyncio
import streamlit as st

from agent.verisci_agent import evaluate_claim_with_spoon, hash_claim


st.title("VeriSci – Scientific Claim Credibility Checker")

st.write(
    "Enter a scientific claim below. VeriSci will evaluate it using the "
    "SpoonOS LLM layer and return a structured credibility assessment."
)

claim = st.text_area("Scientific claim", height=100)

if st.button("Evaluate claim"):
    if not claim.strip():
        st.warning("Please enter a claim first.")
    else:
        with st.spinner("Evaluating via SpoonOS..."):
            result = asyncio.run(evaluate_claim_with_spoon(claim))
        st.subheader("Result")
        st.json(result)

        chash = hash_claim(claim)
        st.write(f"**Claim hash:** `{chash}`")
        st.caption(
            "This hash is used for storage and as the key for the planned on-chain "
            "ClaimRegistry contract on Neo."
        )