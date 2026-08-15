from app.agents.handoff_agents import marketing_manager_agent


def main():
    print()
    print("=" * 50)
    print("HANDOFF SCHEMA TEST")
    print("=" * 50)

    print("Manager:", marketing_manager_agent.name)

    handoffs = marketing_manager_agent.handoffs

    print("Number of handoffs:", len(handoffs))

    # We expect exactly two direct handoffs:
    #
    # Marketing Manager
    #       ├── Marketing Planner
    #       └── Market Research

    if len(handoffs) != 2:
        raise AssertionError(
            f"Expected exactly 2 handoffs, found {len(handoffs)}."
        )

    target_names = []

    for handoff_item in handoffs:

        # Direct Agent handoff
        target_agent = getattr(handoff_item, "agent", None)

        if target_agent is None:
            target_agent = handoff_item

        target_name = getattr(target_agent, "name", None)

        if not target_name:
            raise AssertionError(
                "Could not determine the target agent for a handoff."
            )

        target_names.append(target_name)

        print("Target:", target_name)

    # Required agents
    required_agents = {
        "Marketing Planner",
        "Market Research",
    }

    actual_agents = set(target_names)

    missing = required_agents - actual_agents

    if missing:
        raise AssertionError(
            f"Missing required handoff(s): {sorted(missing)}"
        )

    print()
    print("Handoff schema test: PASS")
    print("=" * 50)


if __name__ == "__main__":
    main()