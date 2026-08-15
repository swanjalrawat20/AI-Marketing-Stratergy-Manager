from app.agents.handoff_agents import marketing_manager_agent


def main():
    print("\n========================================")
    print("STEP 2.5 - HANDOFF SCHEMA TEST")
    print("========================================\n")

    print("Manager:", marketing_manager_agent.name)

    handoffs = marketing_manager_agent.handoffs

    print("Number of handoffs:", len(handoffs))

    for index, h in enumerate(handoffs, start=1):
        target = getattr(h, "agent", h)

        print(f"Handoff {index}:", target.name)

    expected_agents = {
        "Marketing Planner",
        "Market Research",
    }

    actual_agents = {
        getattr(h, "agent", h).name
        for h in handoffs
    }

    assert expected_agents.issubset(actual_agents), (
        f"Missing expected agents. Found: {actual_agents}"
    )

    print("\nExpected specialists found:")
    for name in sorted(expected_agents):
        print("PASS:", name)

    print("\nStep 2.5 schema test: PASS")


if __name__ == "__main__":
    main()