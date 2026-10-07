from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    claim: str = Field(
        description="A specific factual claim supported by a source."
    )

    source_title: str = Field(
        description="Title of the source."
    )

    source_url: str = Field(
        description="URL of the source."
    )

    supporting_text: str = Field(
        description="Relevant text from the search result supporting the claim."
    )

    verification_needed: bool = Field(
        description="Whether this claim requires additional verification."
    )


class ResearchEvidence(BaseModel):
    summary: str = Field(
        description="Concise summary of the research findings."
    )

    findings: list[EvidenceItem] = Field(
        description="Individual evidence items supporting the research."
    )