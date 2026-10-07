from typing import TypedDict

from app.models.research import ResearchPlan
from app.models.evidence import ResearchEvidence
from app.models.fact_check import FactCheckReport
from app.models.final_report import FinalResearchReport


class ResearchState(TypedDict):

    question: str

    research_plan: ResearchPlan | None

    research_evidence: list[ResearchEvidence]

    fact_check_report: FactCheckReport | None

    final_report: FinalResearchReport | None

    status: str

    error_message: str | None