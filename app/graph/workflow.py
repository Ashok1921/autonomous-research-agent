from langgraph.graph import StateGraph, START, END

from app.graph.state import ResearchState
from app.graph.nodes import (
    planner_node,
    web_research_node,
    resume_research_node,
    fact_checker_node,
    report_synthesizer_node,
)
from app.utils.checkpoint import checkpoint_exists


def route_at_start(state: ResearchState):
    if checkpoint_exists():
        print("\n[Workflow] Research checkpoint found.")
        print("[Workflow] Skipping Planner and Web Research.")
        return "resume_research"

    print("\n[Workflow] No research checkpoint found.")
    print("[Workflow] Starting normal research.")
    return "planner"


def route_after_planner(state: ResearchState):
    if state["status"] == "planner_failed":
        return END

    return "web_researcher"


def route_after_web_research(state: ResearchState):
    if state["status"] == "web_research_failed":
        return END

    return "fact_checker"


def route_after_resume(state: ResearchState):
    if state["status"] == "web_research_failed":
        return END

    return "fact_checker"


def route_after_fact_checker(state: ResearchState):
    if state["status"] == "fact_checker_failed":
        return END

    return "report_synthesizer"


def build_research_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("planner", planner_node)
    graph.add_node("web_researcher", web_research_node)
    graph.add_node("resume_research", resume_research_node)
    graph.add_node("fact_checker", fact_checker_node)
    graph.add_node("report_synthesizer", report_synthesizer_node)

    # Decide whether to start fresh or resume saved research.
    graph.add_conditional_edges(
        START,
        route_at_start,
        {
            "planner": "planner",
            "resume_research": "resume_research",
        },
    )

    graph.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "web_researcher": "web_researcher",
            END: END,
        },
    )

    graph.add_conditional_edges(
        "web_researcher",
        route_after_web_research,
        {
            "fact_checker": "fact_checker",
            END: END,
        },
    )

    graph.add_conditional_edges(
        "resume_research",
        route_after_resume,
        {
            "fact_checker": "fact_checker",
            END: END,
        },
    )

    graph.add_conditional_edges(
        "fact_checker",
        route_after_fact_checker,
        {
            "report_synthesizer": "report_synthesizer",
            END: END,
        },
    )

    graph.add_edge("report_synthesizer", END)

    return graph.compile()