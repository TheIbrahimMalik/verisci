import hashlib
import json

# These imports assume you're using SpoonOS Python SDK structure.
# If the exact paths differ, we can tweak later; for now this clearly shows intent.
from spoon_ai.llm import LLM
from spoon_ai.tools.storage import KVStorage


def hash_claim(claim_text: str) -> str:
    return hashlib.sha256(claim_text.encode("utf-8")).hexdigest()


def evaluate_claim_with_spoon(claim: str) -> dict:
    """
    Use SpoonOS unified LLM interface to evaluate a scientific claim.
    Returns structured JSON-like dict.
    """
    llm = LLM(provider="openai", model="gpt-4.1")  # adjust model/provider based on hackathon credits

    prompt = f"""
You are VeriSci, an AI assistant that evaluates the credibility of scientific claims.

Return ONLY valid JSON with the following keys:
- "score": integer 0-100 (0 = not credible at all, 100 = very credible)
- "confidence": one of ["low", "medium", "high"]
- "explanation": string, max 3 sentences, explaining your reasoning
- "factors": array of 3-5 short strings listing key factors you considered

Scientific claim: {claim}
"""

    # Depending on SpoonOS API, this may be llm.run(prompt) or similar.
    # We'll assume it returns an object with a .text attribute containing the model output.
    response = llm.run(prompt)
    raw_text = getattr(response, "text", str(response))

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        # Fallback: wrap raw_text into a dict so we don't crash.
        data = {
            "score": 50,
            "confidence": "low",
            "explanation": "Model returned non-JSON output, using fallback.",
            "factors": [raw_text[:200]],
        }

    return data


def persist_result_with_spoon_tool(claim_hash: str, result: dict):
    """
    Use SpoonOS Storage Tool (KV) to save intermediate agent state and results.
    This satisfies the 'use at least one tool' requirement.
    """
    store = KVStorage(namespace="verisci")
    store.put(claim_hash, result)
    # You could also later read it via store.get(claim_hash)
    return True


def run_agent():
    claim = input("Enter a scientific claim: ")

    claim_hash = hash_claim(claim)
    print(f"\n[VeriSci] Claim hash: {claim_hash}")

    print("\n[VeriSci] Evaluating claim via SpoonOS LLM...")
    result = evaluate_claim_with_spoon(claim)

    print("\n[VeriSci] Evaluation result:")
    print(json.dumps(result, indent=2))

    print("\n[VeriSci] Persisting result using SpoonOS Storage tool...")
    persist_result_with_spoon_tool(claim_hash, result)
    print("[VeriSci] Stored in KVStorage under that hash.")

    print("\n[VeriSci] (Next step) Write this result to Neo smart contract ClaimRegistry.")


if __name__ == "__main__":
    run_agent()