from boa3.builtin import public
from boa3.builtin.interop.storage import get, put

# VeriSci Claim Registry
# Stores: claimHash (string) -> "score|confidence|explanation"

@public
def submitClaim(claim_hash: str, score: int, confidence: str, explanation: str) -> bool:
    """
    Stores the credibility score (0-100), confidence label, and explanation
    for a scientific claim identified by claim_hash.
    """
    if len(claim_hash) == 0:
        return False

    # Very simple serialisation: "score|confidence|explanation"
    payload = str(score) + "|" + confidence + "|" + explanation
    put(claim_hash, payload)
    return True


@public
def getClaim(claim_hash: str) -> str:
    """
    Returns "score|confidence|explanation" for a given claim hash,
    or an empty string if not found.
    """
    result = get(claim_hash).to_str()
    return result