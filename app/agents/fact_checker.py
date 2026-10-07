from langchain_openai import ChatOpenAI

from app.config import OPENROUTER_API_KEY
from app.models.fact_check import FactCheckReport
from app.tools.web_search import search_tool
from app.utils.llm_retry import invoke_with_retry


model = ChatOpenAI(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)

structured_model = model.with_structured_output(FactCheckReport)

FACT_CHECK_PROMPT = """
You are a rigorous fact-checking and evidence-quality agent.

Your task is to evaluate the supplied research claims using
the provided web search results.

Claims to verify:
{claims}

Web Search Results:
{search_results}

For EACH claim, evaluate all of the following dimensions.

1. VERIFICATION STATUS

Use exactly one:

* verified
* partially_verified
* unverified
* contradicted

verified:
The available evidence directly supports the main claim,
with sufficiently reliable evidence and no major unresolved
contradiction.

partially_verified:
Some important part of the claim is supported, but the
evidence is incomplete, indirect, conflicting, outdated,
or does not fully support the entire claim.

unverified:
There is insufficient reliable evidence to establish the claim.

contradicted:
Reliable evidence directly conflicts with the claim.

2. EVIDENCE STRENGTH

Use exactly one:

* strong
* moderate
* weak
* insufficient

Strong:
Multiple reliable sources directly support the claim.

Moderate:
Reasonable evidence exists, but there are limitations such as
limited sources, partial evidence, or some uncertainty.

Weak:
Evidence is mostly indirect, low-quality, promotional,
single-source, or otherwise unreliable.

Insufficient:
There is not enough usable evidence to evaluate the claim.

3. SOURCE QUALITY

Use exactly one:

* high
* medium
* low
* mixed

High-quality sources may include:

* Government agencies
* Regulatory bodies
* Official organizations
* Peer-reviewed research
* Major academic institutions
* Established international organizations
* Primary institutional documents

Medium-quality sources may include:

* Established technology publications
* Reputable business publications
* Industry research
* Professional organizations
* Secondary reporting

Low-quality sources may include:

* Marketing pages
* Unsourced blogs
* SEO websites
* Social media posts
* Promotional material
* Aggregator websites
* Sources with unclear methodology

Mixed:
Use this when the evidence contains a meaningful mixture
of high/medium-quality sources and weaker sources.

4. SOURCE QUALITY REASON

Explain WHY the sources received the selected quality.

For example:

"Evidence includes a government report and two established
news publications, although one supporting source is a
company promotional page."

Do not simply repeat "high quality" or "medium quality."

5. INDEPENDENT SOURCES

Estimate how many genuinely independent sources provide
meaningful evidence.

Do NOT count multiple websites that simply repeat the same
underlying report as independent sources.

Example:

Three news articles citing the same market-research report
should generally count as one underlying source.

If the evidence comes from different organizations or
independent research, they may be counted separately.

6. DIRECT EVIDENCE

Set direct_evidence to true only when the evidence directly
supports the actual claim.

Example:

Claim:
"AI is being used for clinical documentation."

Direct evidence:
A healthcare organization or study explicitly documents
AI use for clinical documentation.

Indirect evidence:
A source only describes the capability of AI to summarize
clinical notes.

Do NOT treat general capability evidence as direct evidence.

7. EVIDENCE LIMITATIONS

Provide a list of important limitations.

Consider:

* Geographic limitations
* Time/date limitations
* Small sample sizes
* Conflicting sources
* Forecast uncertainty
* Indirect evidence
* Weak sources
* Promotional sources
* Lack of independent sources
* Missing primary evidence
* Different definitions of the same metric

If there are no meaningful limitations, return an empty list.

8. CONTRADICTIONS

Look carefully for conflicting evidence.

If different credible sources provide significantly different
market sizes or CAGR estimates, identify the disagreement.

Do not automatically select one number as correct.

9. GEOGRAPHIC RELEVANCE

Pay attention to geography.

If the claim concerns India but the evidence only concerns
the United States or global healthcare, do not treat that
evidence as direct India-specific evidence.

The claim may therefore be only partially verified.

10. TEMPORAL RELEVANCE

Pay attention to dates.

Current claims should preferably use recent evidence.

Historical evidence should not automatically be treated as
proof of the current situation.

11. NUMERICAL CLAIMS

Be especially careful with:

* Market size
* CAGR
* Adoption percentages
* Patient numbers
* Revenue
* Funding
* Hospital counts
* Forecasts

If credible sources provide different numbers, identify the
disagreement rather than choosing one number without
explanation.

12. PREDICTIONS AND FORECASTS

Clearly distinguish between:

* Current facts
* Historical facts
* Forecasts
* Predictions
* Expert opinions

A forecast must not be presented as an established fact.

13. SOURCE URLS

Only include URLs that actually appear in the supplied
search results.

Never invent URLs.

Never fabricate sources.

14. EXPLANATION

The explanation should clearly describe:

* Why the claim received its status
* How strong the evidence is
* Whether evidence is direct or indirect
* Important supporting evidence
* Important contradictions
* Important uncertainty

IMPORTANT RULE:

Do not mark a claim as "verified" merely because one search
result says the claim is true.

Evidence quality, independence, directness, geography,
timeliness, and contradictions all matter.

If evidence is insufficient, say so explicitly instead of
guessing.
"""

def fact_check_claims(claims: list[str]) -> FactCheckReport:
    search_results = []

    # Search each claim with Tavily
    for claim in claims:
        print(f"\n[Fact Check Search] {claim}")

        result = search_tool.invoke({
            "query": claim
        })

        search_results.append({
            "claim": claim,
            "results": result,
        })

    # Process claims in smaller LLM batches.
    # This prevents one enormous structured-output request.
    BATCH_SIZE = 10
    all_results = []

    total_claims = len(claims)

    for start in range(0, total_claims, BATCH_SIZE):
        end = min(start + BATCH_SIZE, total_claims)

        batch_claims = claims[start:end]
        batch_search_results = search_results[start:end]

        print(
            f"\n[Fact Check Batch] "
            f"{start + 1}-{end} of {total_claims}"
        )

        prompt = FACT_CHECK_PROMPT.format(
            claims=batch_claims,
            search_results=batch_search_results,
        )

        batch_report = invoke_with_retry(
            structured_model,
            prompt,
        )

        all_results.extend(batch_report.results)

    return FactCheckReport(
        results=all_results
)

