from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):
    objective: str = Field(
        description="The main objective of the research."
    )

    tasks: list[str] = Field(
        description="Specific research tasks that need to be completed."
    )

    subtopics: list[str] = Field(
        description="Important subtopics that should be investigated."
    )

    verification_requirements: list[str] = Field(
        description="Claims or information that require verification."
    )

    source_types: list[str] = Field(
        description="Recommended types of sources for the research."
    )