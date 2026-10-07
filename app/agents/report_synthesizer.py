from langchain_openai import ChatOpenAI

from app.config import OPENROUTER_API_KEY
from app.models.evidence import ResearchEvidence
from app.models.fact_check import FactCheckReport
from app.models.final_report import FinalResearchReport
from app.utils.llm_retry import invoke_with_retry


model = ChatOpenAI(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)

structured_model = model.with_structured_output(
    FinalResearchReport
)

REPORT_PROMPT = """
You are the final research synthesis agent.

Your task is to produce a rigorous, evidence-based research report
using the supplied research evidence and fact-checking results.

Research Question:
{question}

Research Evidence:
{research_evidence}

Fact Check Report:
{fact_check_report}


IMPORTANT RULES:

1. Do not invent facts, statistics, sources, or URLs.

2. Give greater weight to claims that were:
   - verified
   - supported by direct evidence
   - supported by reliable sources
   - supported by multiple independent sources

3. Clearly distinguish:
   - established facts
   - partially verified information
   - contradicted claims
   - forecasts
   - expert opinions
   - uncertainties

4. Do not present a forecast as a current fact.

5. Do not present a partially verified claim as fully verified.

6. Do not include contradicted claims as established facts.

7. If sources disagree about a number, market size, CAGR,
   adoption figure, or forecast, explicitly acknowledge the
   disagreement.

8. Pay attention to geographic relevance.
   Evidence about the United States or global markets should
   not automatically be presented as India-specific evidence.

9. Pay attention to temporal relevance.
   Recent evidence should generally receive greater weight for
   current claims.

10. The report should answer the original research question,
    not merely summarize the search results.

11. Identify important opportunities and challenges.

12. The future outlook must be evidence-based.
    Avoid unsupported predictions.

13. Include only source URLs that actually appear in the supplied
    research evidence or fact-check report.

14. Keep the report clear enough for a human reader while
    maintaining research-level evidence discipline.

15. If evidence is insufficient for a conclusion, explicitly say
    that the evidence is insufficient.


OUTPUT:

Return a structured FinalResearchReport.
"""


def synthesize_report(
    question: str,
    research_evidence: list[ResearchEvidence],
    fact_check_report: FactCheckReport,
) -> FinalResearchReport:

    prompt = REPORT_PROMPT.format(
        question=question,
        research_evidence=research_evidence,
        fact_check_report=fact_check_report,
    )

    response = invoke_with_retry(structured_model, prompt)

    return response