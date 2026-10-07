from pydantic import BaseModel, Field


class FinalResearchReport(BaseModel):
    title: str = Field(
        description="Clear title for the final research report."
    )

    executive_summary: str = Field(
        description="Concise summary of the most important research conclusions."
    )

    key_findings: list[str] = Field(
        description="Important findings supported by the research evidence."
    )

    verified_facts: list[str] = Field(
        description="Claims that were strongly supported by the fact-checking stage."
    )

    uncertain_or_partial_findings: list[str] = Field(
        description="Claims that were only partially verified or have important limitations."
    )

    contradicted_claims: list[str] = Field(
        description="Claims that were contradicted by reliable evidence."
    )

    opportunities: list[str] = Field(
        description="Important opportunities identified by the research."
    )

    challenges: list[str] = Field(
        description="Important challenges, risks, or barriers identified by the research."
    )

    future_outlook: str = Field(
        description="Balanced discussion of the likely future direction based on the available evidence."
    )

    conclusion: str = Field(
        description="Final evidence-based conclusion."
    )

    sources: list[str] = Field(
        description="Important source URLs used in the final report."
    )