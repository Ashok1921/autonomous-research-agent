from langchain_openai import ChatOpenAI

from app.config import OPENROUTER_API_KEY
from app.tools.web_search import search_tool
from app.models.evidence import ResearchEvidence
from app.utils.llm_retry import invoke_with_retry


model = ChatOpenAI(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)

structured_model = model.with_structured_output(ResearchEvidence)


WEB_RESEARCH_PROMPT = """
You are an expert web research agent.

You have been given search results collected from the web.

Research Task:
{task}

Web Search Results:
{search_results}

Create structured research evidence.

Rules:

1. Extract only claims supported by the supplied search results.
2. Include the exact source title when available.
3. Include the source URL.
4. Include relevant supporting text from the search results.
5. Mark verification_needed=True when a claim should be independently
   verified, especially statistics, medical claims, market projections,
   regulatory claims, or claims based on weak sources.
6. Do not invent sources.
7. Do not invent URLs.
8. Do not add information that is not supported by the search results.
9. Provide a concise overall summary.
"""


def research_task(task: str) -> ResearchEvidence:

    search_results = search_tool.invoke({
        "query": task
    })

    prompt = WEB_RESEARCH_PROMPT.format(
        task=task,
        search_results=search_results,
    )

    response = invoke_with_retry(structured_model, prompt)

    return response