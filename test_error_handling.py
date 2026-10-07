from app.graph.workflow import build_research_graph


def main():
    graph = build_research_graph()

    # Start with an intentionally invalid state.
    # Planner will be replaced with a local failure simulation below.
    initial_state = {
        "question": "Offline error handling test",
        "research_plan": None,
        "research_evidence": [],
        "fact_check_report": None,
        "final_report": None,
        "status": "planner_failed",
        "error_message": "Simulated offline failure.",
    }

    print("\n======================================")
    print("OFFLINE ERROR HANDLING TEST")
    print("======================================")

    print(f"\nInitial status: {initial_state['status']}")
    print(f"Initial error: {initial_state['error_message']}")

    # Test the routing logic directly.
    from app.graph.workflow import route_after_planner

    next_node = route_after_planner(initial_state)

    print(f"\nNext graph step: {next_node}")

    if next_node == "__end__":
        print("\nSUCCESS: Workflow correctly stops after a planner failure.")
    else:
        print("\nERROR: Workflow did not stop correctly.")

    print("\n======================================")
    print("OFFLINE TEST COMPLETED")
    print("======================================")


if __name__ == "__main__":
    main()