from langchain_openai import ChatOpenAI

from app.config import OPENROUTER_API_KEY
from app.models.research import ResearchPlan


model = ChatOpenAI(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)


structured_model = model.with_structured_output(ResearchPlan)


PLANNER_PROMPT = """
You are an expert research planning agent.

Create a structured research plan for the user's research question.

Your plan must contain:

1. A clear research objective.
2. 5-8 specific research tasks.
3. Important subtopics.
4. Information or claims that require verification.
5. Recommended source types.

Do NOT answer the research question.

Create only the research plan.

Research Question:
{question}
"""


def create_research_plan(question: str) -> ResearchPlan:
    prompt = PLANNER_PROMPT.format(question=question)

    response = structured_model.invoke(prompt)

    return response