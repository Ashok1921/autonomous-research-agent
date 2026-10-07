
from app.agents.fact_checker import fact_check_claims


claims = [
    """
    Generative AI is being used for clinical documentation
    in healthcare.
    """,

    """
    The Indian healthcare AI market will reach $34.35 billion
    by 2034 with a CAGR of 40.60%.
    """,

    """
    AIIMS New Delhi has deployed Smart Doctor across
    70,000 hospitals in India.
    """,

    """
    Generative AI can help reduce administrative workload
    for healthcare professionals.
    """,
]


result = fact_check_claims(claims)


print("\n======================================")
print("FACT CHECK REPORT")
print("======================================")


for index, item in enumerate(result.results, start=1):

    print(f"\n--- Claim {index} ---")

    print(f"Claim: {item.claim}")

    print(f"\nStatus: {item.status}")

    print(f"Evidence strength: {item.evidence_strength}")

    print(f"Source quality: {item.source_quality}")

    print(f"Independent sources: {item.independent_sources}")

    print(f"Direct evidence: {item.direct_evidence}")

    print(f"\nExplanation:")
    print(item.explanation)

    print("\nSupporting sources:")

    for source in item.supporting_sources:
        print(f"- {source}")

    print("\nContradicting sources:")

    for source in item.contradicting_sources:
        print(f"- {source}")

