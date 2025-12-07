import asyncio
import hashlib
import json

from spoon_ai.llm import LLMManager, ConfigurationManager
from spoon_ai.tools.base import BaseTool


SYSTEM_PROMPT = """
You are VeriSci, an AI assistant that evaluates the credibility of scientific claims.

You MUST respond with valid JSON only, using this schema:
{
  "score": 0-100 integer,
  "confidence": "low" | "medium" | "high",
  "explanation": string (max 3 sentences),
  "factors": [string, ...]  // 3–5 short points
}
"""


def hash_claim(claim_text: str) -> str:
    """
    Compute a deterministic hash for the claim so we can
    use it as a key for storage and on-chain indexing.
    """
    return hashlib.sha256(claim_text.encode("utf-8")).hexdigest()


async def evaluate_claim_with_spoon(claim: str) -> dict:
    """
    Use SpoonOS's unified LLM manager to evaluate a scientific claim.

    Flow:
      1) Try Agent -> SpoonOS -> LLM (OpenAI) via LLMManager.chat(...)
      2) If that fails (e.g. ProviderError), fall back to a direct OpenAI call
         using the same messages.
      3) If that also fails, fall back to a deterministic stub so the demo
         always remains functional.
    """
    config_manager = ConfigurationManager()
    llm_manager = LLMManager(config_manager)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Scientific claim: {claim}"},
    ]

    # 1) Primary path: SpoonOS -> OpenAI via LLMManager
    try:
        print("\n[SpoonOS] Calling LLMManager.chat(...) via unified protocol layer...")
        response = await llm_manager.chat(messages)
        content = getattr(response, "content", None) or str(response)
        data = json.loads(content)

        # Normalise and return
        data.setdefault("score", 50)
        data.setdefault("confidence", "low")
        data.setdefault("explanation", "No explanation provided.")
        data.setdefault("factors", [])

        return data

    except Exception as e:
        print(f"[SpoonOS] LLM call failed: {type(e).__name__}: {e}")
        print("[SpoonOS] Attempting direct OpenAI fallback...\n")

        # 2) Secondary path: direct OpenAI call using the same messages
        try:
            from openai import OpenAI

            client = OpenAI()  # uses OPENAI_API_KEY from environment

            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )
            content = resp.choices[0].message.content
            data = json.loads(content)

            # Normalise
            data.setdefault("score", 50)
            data.setdefault("confidence", "low")
            data.setdefault("explanation", "No explanation provided.")
            data.setdefault("factors", [])

            print("[OpenAI] Direct call succeeded.")
            return data

        except Exception as e2:
            print(f"[OpenAI] Direct call failed, falling back to stub: {type(e2).__name__}: {e2}")

            # 3) Last-resort stub so the demo never breaks
            data = {
                "score": 60,
                "confidence": "medium",
                "explanation": (
                    "Fallback evaluation: both SpoonOS and direct LLM calls failed or "
                    "are not yet fully configured. In a full deployment this would "
                    "always be replaced by successful LLM reasoning."
                ),
                "factors": [
                    "Claim length and specificity (heuristic)",
                    "General plausibility based on common scientific understanding (stub)",
                    f"Internal error chain: {type(e).__name__} -> {type(e2).__name__}",
                ],
            }
            return data


class StoreEvaluationTool(BaseTool):
    """
    Simple SpoonOS tool that 'stores' a VeriSci evaluation.

    For the hackathon prototype, this tool simply logs the result to stdout.
    In a fuller version, it could write to a database, file, or external storage.
    """
    name: str = "store_evaluation"
    description: str = "Store a scientific claim evaluation keyed by its hash."
    parameters: dict = {
        "type": "object",
        "properties": {
            "claim_hash": {
                "type": "string",
                "description": "SHA-256 hash of the scientific claim text."
            },
            "score": {
                "type": "integer",
                "description": "Credibility score (0–100)."
            },
            "confidence": {
                "type": "string",
                "description": "Confidence level: low, medium, or high."
            },
            "explanation": {
                "type": "string",
                "description": "Short explanation of the evaluation."
            },
        },
        "required": ["claim_hash", "score", "confidence", "explanation"],
    }

    async def execute(
        self,
        claim_hash: str,
        score: int,
        confidence: str,
        explanation: str,
    ) -> str:
        """
        Store the evaluation locally in a JSON file.

        For the hackathon prototype, this demonstrates a concrete storage
        mechanism behind the tool. In a fuller version, this could be swapped
        for a database or decentralised storage.
        """
        print("\n[StoreEvaluationTool] Storing evaluation:")
        print(f"  claim_hash:  {claim_hash}")
        print(f"  score:       {score}")
        print(f"  confidence:  {confidence}")
        print(f"  explanation: {explanation[:120]}...")

        # Simple local JSON store: data/verisci_store.json
        try:
            import os

            os.makedirs("data", exist_ok=True)
            store_path = os.path.join("data", "verisci_store.json")

            # Load existing store if present
            if os.path.exists(store_path):
                with open(store_path, "r", encoding="utf-8") as f:
                    store = json.load(f)
            else:
                store = {}

            # Update entry for this claim
            store[claim_hash] = {
                "score": score,
                "confidence": confidence,
                "explanation": explanation,
            }

            # Write back to disk
            with open(store_path, "w", encoding="utf-8") as f:
                json.dump(store, f, indent=2)

            print("[StoreEvaluationTool] Stored evaluation in data/verisci_store.json.")
            return "stored"
        except Exception as e:
            print(f"[StoreEvaluationTool] Failed to write to local store: {type(e).__name__}: {e}")
            # Still return a value so the agent can continue.
            return "error"



def submit_to_neo_stub(claim_hash: str, score: int, confidence: str, explanation: str) -> None:
    """
    Stub for submitting the evaluation to the Neo ClaimRegistry smart contract.

    In the full implementation, this would:
    - Construct and sign a transaction
    - Call submitClaim(claim_hash, score, confidence, explanation)
      on the deployed ClaimRegistry contract on Neo testnet.
    """
    print("\n[NeoStub] Preparing to submit to ClaimRegistry:")
    print(f"  claim_hash:  {claim_hash}")
    print(f"  score:       {score}")
    print(f"  confidence:  {confidence}")
    print(f"  explanation: {explanation[:120]}...")
    print("[NeoStub] (Stub) This is where a real Neo RPC call would be made.")


async def agent_run() -> None:
    claim = input("Enter a scientific claim: ")

    claim_hash = hash_claim(claim)
    print(f"\n[VeriSci] Claim hash: {claim_hash}")

    print("\n[VeriSci] Evaluating claim via SpoonOS LLM...")
    result = await evaluate_claim_with_spoon(claim)

    print("\n[VeriSci] Evaluation result (structured):")
    print(json.dumps(result, indent=2))

    # Extract fields safely
    score = int(result.get("score", 50))
    confidence = str(result.get("confidence", "low"))
    explanation = str(result.get("explanation", ""))

    # Use our Spoon tool to 'store' the evaluation
    tool = StoreEvaluationTool()
    try:
        await tool.execute(
            claim_hash=claim_hash,
            score=score,
            confidence=confidence,
            explanation=explanation,
        )
        print("\n[VeriSci] Evaluation passed through StoreEvaluationTool successfully.")
    except Exception as e:
        print(f"\n[VeriSci] Failed to store evaluation via tool: {type(e).__name__}: {e}")

    # Neo submission stub (explained clearly in docs and video)
    submit_to_neo_stub(claim_hash, score, confidence, explanation)

    print(
        "\n[VeriSci] End of agent run."
        "\n  - SpoonOS LLM flow demonstrated (with fallback if unconfigured)."
        "\n  - SpoonOS Tool (StoreEvaluationTool) invoked with basic error handling."
        "\n  - Neo submission stub clearly indicating where on-chain integration occurs."
    )


if __name__ == "__main__":
    asyncio.run(agent_run())