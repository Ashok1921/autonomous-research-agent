from app.agents.web_researcher import research_task


task = """
Identify current Generative AI applications
in healthcare globally.
"""


result = research_task(task)


print("\n==============================")
print("RESEARCH SUMMARY")
print("==============================")
print(result.summary)


print("\n==============================")
print("EVIDENCE ITEMS")
print("==============================")

for index, item in enumerate(result.findings, start=1):

    print(f"\n--- Evidence {index} ---")

    print(f"Claim: {item.claim}")
    print(f"Source: {item.source_title}")
    print(f"URL: {item.source_url}")
    print(f"Supporting text: {item.supporting_text}")
    print(f"Verification needed: {item.verification_needed}")