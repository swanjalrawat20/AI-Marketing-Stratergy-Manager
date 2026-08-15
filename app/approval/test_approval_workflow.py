"""
STEP 3.2 - HUMAN APPROVAL + AGENT WORKFLOW INTEGRATION TEST

This test does NOT call Groq.

It validates:

    Agent Strategy
          ↓
    Approval Workflow
          ↓
    Human Revision Request
          ↓
    Revised Strategy
          ↓
    Human Re-approval
          ↓
    Final Approved Strategy
"""

from app.approval.human_approval import ApprovalStatus
from app.approval.workflow_integration import ApprovalWorkflow


# ============================================================
# TEST STRATEGY
# ============================================================

INITIAL_STRATEGY = """
AI Study Assistant Campaign Strategy

Campaign Goal:
Acquire 1,000 college student signups.

Target Audience:
College students aged 18-25.

Total Budget:
₹50,000

Initial Channel Allocation:

Instagram:
₹20,000

Influencer Marketing:
₹15,000

Content Marketing:
₹10,000

Other:
₹5,000
""".strip()


REVISED_STRATEGY = """
AI Study Assistant Campaign Strategy - Revised

Campaign Goal:
Acquire 1,000 college student signups.

Target Audience:
College students aged 18-25.

Total Budget:
₹50,000

Revised Channel Allocation:

Instagram:
₹25,000

Influencer Marketing:
₹10,000

Content Marketing:
₹10,000

Other:
₹5,000
""".strip()


# ============================================================
# MAIN TEST
# ============================================================

def main():

    print()
    print("=" * 60)
    print("STEP 3.2 - HUMAN APPROVAL + AGENT WORKFLOW INTEGRATION")
    print("=" * 60)

    print()
    print("This test does NOT call Groq.")

    print()
    print("Testing:")
    print("Agent strategy → Human approval → Revision → Re-approval")

    # ========================================================
    # TEST 1
    # ========================================================

    print()
    print("=" * 60)
    print("TEST 1 - CREATE APPROVAL WORKFLOW")
    print("=" * 60)

    workflow = ApprovalWorkflow(
        strategy=INITIAL_STRATEGY,
        metadata={
            "source": "agent",
            "agent": "Marketing Planner",
            "test_workflow": True,
        },
        reviewer="project_owner",
    )

    print()
    print("Initial status:")
    print(workflow.status)

    print()
    print("Initial revision number:")
    print(workflow.revision_number)

    test1_status = (
        workflow.status == ApprovalStatus.PENDING
    )

    test1_revision = (
        workflow.revision_number == 0
    )

    print(
        "Initial pending status:",
        "PASS" if test1_status else "FAIL",
    )

    print(
        "Initial revision number:",
        "PASS" if test1_revision else "FAIL",
    )

    if not (test1_status and test1_revision):
        raise SystemExit(
            "TEST 1 FAILED"
        )

    # ========================================================
    # TEST 2
    # ========================================================

    print()
    print("=" * 60)
    print("TEST 2 - AGENT STRATEGY ENTERS APPROVAL")
    print("=" * 60)

    print()
    print("Current strategy:")
    print("-" * 60)
    print(workflow.current_strategy)
    print("-" * 60)

    strategy_loaded = (
        workflow.current_strategy == INITIAL_STRATEGY
    )

    print()
    print(
        "Agent strategy loaded:",
        "PASS" if strategy_loaded else "FAIL",
    )

    if not strategy_loaded:
        raise SystemExit(
            "TEST 2 FAILED"
        )

    # ========================================================
    # TEST 3
    # ========================================================

    print()
    print("=" * 60)
    print("TEST 3 - HUMAN REQUESTS REVISION")
    print("=" * 60)

    revision_feedback = (
        "Reduce influencer spending and increase "
        "Instagram advertising."
    )

    workflow.request_revision(
        feedback=revision_feedback,
        reviewer="project_owner",
    )

    print()
    print("Status after human review:")
    print(workflow.status)

    print()
    print("Revision number:")
    print(workflow.revision_number)

    print()
    print("Revision feedback:")
    print(workflow.get_revision_feedback())

    revision_status_pass = (
        workflow.status
        == ApprovalStatus.REVISION_REQUESTED
    )

    revision_number_pass = (
        workflow.revision_number == 1
    )

    feedback_pass = (
        workflow.get_revision_feedback()
        == revision_feedback
    )

    print(
        "Revision requested:",
        "PASS" if revision_status_pass else "FAIL",
    )

    print(
        "Revision number:",
        "PASS" if revision_number_pass else "FAIL",
    )

    print(
        "Feedback stored:",
        "PASS" if feedback_pass else "FAIL",
    )

    if not (
        revision_status_pass
        and revision_number_pass
        and feedback_pass
    ):
        raise SystemExit(
            "TEST 3 FAILED"
        )

    # ========================================================
    # TEST 4
    # ========================================================

    print()
    print("=" * 60)
    print("TEST 4 - APPLY REVISED AGENT STRATEGY")
    print("=" * 60)

    workflow.apply_revision(
        revised_strategy=REVISED_STRATEGY
    )

    print()
    print("Status after revision:")
    print(workflow.status)

    print()
    print("Revision number:")
    print(workflow.revision_number)

    print()
    print("Revised strategy:")
    print("-" * 60)
    print(workflow.current_strategy)
    print("-" * 60)

    returned_to_pending = (
        workflow.status == ApprovalStatus.PENDING
    )

    revision_preserved = (
        workflow.revision_number == 1
    )

    revised_strategy_stored = (
        workflow.current_strategy
        == REVISED_STRATEGY
    )

    print(
        "Returned to approval:",
        "PASS" if returned_to_pending else "FAIL",
    )

    print(
        "Revision number preserved:",
        "PASS" if revision_preserved else "FAIL",
    )

    print(
        "Revised strategy stored:",
        "PASS" if revised_strategy_stored else "FAIL",
    )

    if not (
        returned_to_pending
        and revision_preserved
        and revised_strategy_stored
    ):
        raise SystemExit(
            "TEST 4 FAILED"
        )

    # ========================================================
    # TEST 5
    # ========================================================

    print()
    print("=" * 60)
    print("TEST 5 - APPROVE REVISED STRATEGY")
    print("=" * 60)

    workflow.approve(
        feedback="Approved after revision.",
        reviewer="project_owner",
    )

    print()
    print("Final status:")
    print(workflow.status)

    print()
    print("Revision number:")
    print(workflow.revision_number)

    final_approval = workflow.is_approved()

    final_status_pass = (
        workflow.status
        == ApprovalStatus.APPROVED
    )

    revision_number_final = (
        workflow.revision_number == 1
    )

    print(
        "Final approval:",
        "PASS" if final_status_pass else "FAIL",
    )

    print(
        "Final strategy approved:",
        "PASS" if final_approval else "FAIL",
    )

    print(
        "Revision number preserved:",
        "PASS" if revision_number_final else "FAIL",
    )

    if not (
        final_status_pass
        and final_approval
        and revision_number_final
    ):
        raise SystemExit(
            "TEST 5 FAILED"
        )

    # ========================================================
    # TEST 6
    # ========================================================

    print()
    print("=" * 60)
    print("TEST 6 - APPROVAL HISTORY")
    print("=" * 60)

    history = workflow.get_history()

    print()
    print("Approval history:")

    for index, decision in enumerate(
        history,
        start=1,
    ):
        print()
        print(f"Decision {index}:")
        print(decision)

    # There should be exactly two decisions:
    #
    # 1. Revision requested
    # 2. Approved

    history_count_pass = (
        len(history) == 2
    )

    first_decision_pass = (
        history[0]["status"]
        == ApprovalStatus.REVISION_REQUESTED.value
    )

    second_decision_pass = (
        history[1]["status"]
        == ApprovalStatus.APPROVED.value
    )

    first_feedback_pass = (
        history[0]["feedback"]
        == revision_feedback
    )

    second_feedback_pass = (
        history[1]["feedback"]
        == "Approved after revision."
    )

    print()
    print(
        "History count:",
        "PASS" if history_count_pass else "FAIL",
    )

    print(
        "First decision:",
        "PASS" if first_decision_pass else "FAIL",
    )

    print(
        "Second decision:",
        "PASS" if second_decision_pass else "FAIL",
    )

    print(
        "Revision feedback:",
        "PASS" if first_feedback_pass else "FAIL",
    )

    print(
        "Approval feedback:",
        "PASS" if second_feedback_pass else "FAIL",
    )

    if not (
        history_count_pass
        and first_decision_pass
        and second_decision_pass
        and first_feedback_pass
        and second_feedback_pass
    ):
        raise SystemExit(
            "TEST 6 FAILED"
        )

    # ========================================================
    # TEST 7
    # ========================================================

    print()
    print("=" * 60)
    print("TEST 7 - WORKFLOW STATE")
    print("=" * 60)

    workflow_data = workflow.to_dict()

    print()
    print("Workflow state:")
    print(workflow_data)

    status_pass = (
        workflow_data["status"]
        == ApprovalStatus.APPROVED.value
    )

    revision_pass = (
        workflow_data["revision_number"] == 1
    )

    strategy_pass = (
        workflow_data["strategy"]
        == REVISED_STRATEGY
    )

    metadata_pass = (
        workflow_data["metadata"]["source"]
        == "agent"
    )

    print()
    print(
        "Final status stored:",
        "PASS" if status_pass else "FAIL",
    )

    print(
        "Final revision stored:",
        "PASS" if revision_pass else "FAIL",
    )

    print(
        "Final strategy stored:",
        "PASS" if strategy_pass else "FAIL",
    )

    print(
        "Agent metadata stored:",
        "PASS" if metadata_pass else "FAIL",
    )

    if not (
        status_pass
        and revision_pass
        and strategy_pass
        and metadata_pass
    ):
        raise SystemExit(
            "TEST 7 FAILED"
        )

    # ========================================================
    # FINAL VERIFICATION
    # ========================================================

    print()
    print("=" * 60)
    print("STEP 3.2 VERIFICATION")
    print("=" * 60)

    print("Workflow creation: PASS")
    print("Agent strategy loading: PASS")
    print("Human revision request: PASS")
    print("Apply revised strategy: PASS")
    print("Re-approval: PASS")
    print("Approval history: PASS")
    print("Final workflow state: PASS")

    print()
    print("=" * 60)
    print(
        "STEP 3.2 COMPLETE - HUMAN APPROVAL + "
        "AGENT WORKFLOW PASSED"
    )
    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()