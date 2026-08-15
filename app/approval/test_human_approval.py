from __future__ import annotations

from app.approval.human_approval import (
    ApprovalStatus,
    HumanApprovalManager,
)


# ============================================================
# TEST HELPERS
# ============================================================

def print_test(
    number: int,
    title: str,
) -> None:

    print()
    print("=" * 60)
    print(f"TEST {number} - {title}")
    print("=" * 60)


def assert_pass(
    condition: bool,
    message: str,
) -> bool:

    if condition:
        print(f"{message}: PASS")
        return True

    print(f"{message}: FAIL")
    return False


# ============================================================
# TEST 1
# ============================================================

def test_session_creation(
    manager: HumanApprovalManager,
) -> bool:

    print_test(
        1,
        "CREATE APPROVAL SESSION",
    )

    strategy = """
AI Marketing Strategy

Product:
AI Study Assistant

Audience:
College students aged 18-25

Budget:
₹50,000

Goal:
1,000 signups
""".strip()

    session = manager.create_session(
        strategy
    )

    print()
    print("Initial status:")
    print(session.status.value)

    print()
    print("Revision number:")
    print(session.revision_number)

    return (
        assert_pass(
            session.status
            == ApprovalStatus.PENDING,
            "Initial status",
        )
        and assert_pass(
            session.revision_number == 0,
            "Initial revision number",
        )
    )


# ============================================================
# TEST 2
# ============================================================

def test_approve(
    manager: HumanApprovalManager,
    session,
) -> bool:

    print_test(
        2,
        "HUMAN APPROVES STRATEGY",
    )

    manager.approve(
        session,
        feedback="Strategy looks good.",
    )

    print()
    print("Status:")
    print(session.status.value)

    print()
    print("Feedback:")
    print(session.current_feedback)

    return (
        assert_pass(
            session.status
            == ApprovalStatus.APPROVED,
            "Approval status",
        )
        and assert_pass(
            manager.is_approved(session),
            "is_approved()",
        )
    )


# ============================================================
# TEST 3
# ============================================================

def test_revision(
    manager: HumanApprovalManager,
) -> bool:

    print_test(
        3,
        "HUMAN REQUESTS REVISION",
    )

    strategy = """
AI Marketing Strategy

Budget:
₹50,000

Channels:
Instagram
Influencers
Content Marketing
""".strip()

    session = manager.create_session(
        strategy
    )

    manager.request_revision(
        session,
        feedback=(
            "Reduce influencer spending and "
            "increase Instagram advertising."
        ),
    )

    print()
    print("Status:")
    print(session.status.value)

    print()
    print("Revision number:")
    print(session.revision_number)

    print()
    print("Feedback:")
    print(session.current_feedback)

    return (
        assert_pass(
            session.status
            == ApprovalStatus.REVISION_REQUESTED,
            "Revision status",
        )
        and assert_pass(
            session.revision_number == 1,
            "Revision number",
        )
        and assert_pass(
            manager.needs_revision(session),
            "needs_revision()",
        )
    )


# ============================================================
# TEST 4
# ============================================================

def test_apply_revision(
    manager: HumanApprovalManager,
) -> bool:

    print_test(
        4,
        "APPLY REVISED STRATEGY",
    )

    original_strategy = """
Original Strategy

Instagram:
₹20,000

Influencers:
₹15,000

Content:
₹10,000

Other:
₹5,000
""".strip()

    session = manager.create_session(
        original_strategy
    )

    manager.request_revision(
        session,
        feedback=(
            "Increase Instagram budget "
            "and reduce influencer spending."
        ),
    )

    revised_strategy = """
Revised Strategy

Instagram:
₹25,000

Influencers:
₹10,000

Content:
₹10,000

Other:
₹5,000
""".strip()

    manager.apply_revision(
        session,
        revised_strategy,
    )

    print()
    print("Status after revision:")
    print(session.status.value)

    print()
    print("Revision number:")
    print(session.revision_number)

    print()
    print("Revised strategy:")
    print(session.strategy)

    return (
        assert_pass(
            session.status
            == ApprovalStatus.PENDING,
            "Returned to approval",
        )
        and assert_pass(
            session.revision_number == 1,
            "Revision number preserved",
        )
        and assert_pass(
            "₹25,000" in session.strategy,
            "Revised strategy stored",
        )
    )


# ============================================================
# TEST 5
# ============================================================

def test_reapprove_after_revision(
    manager: HumanApprovalManager,
) -> bool:

    print_test(
        5,
        "APPROVE REVISED STRATEGY",
    )

    strategy = """
Revised AI Marketing Strategy

Budget:
₹50,000

Instagram:
₹25,000

Influencers:
₹10,000

Content:
₹10,000

Other:
₹5,000
""".strip()

    session = manager.create_session(
        strategy
    )

    manager.request_revision(
        session,
        feedback=(
            "Increase Instagram allocation."
        ),
    )

    manager.apply_revision(
        session,
        strategy,
    )

    manager.approve(
        session,
        feedback=(
            "Revised strategy approved."
        ),
    )

    print()
    print("Final status:")
    print(session.status.value)

    print()
    print("Revision number:")
    print(session.revision_number)

    return (
        assert_pass(
            session.status
            == ApprovalStatus.APPROVED,
            "Final approval",
        )
        and assert_pass(
            manager.is_approved(session),
            "Final strategy approved",
        )
    )


# ============================================================
# TEST 6
# ============================================================

def test_approval_history(
    manager: HumanApprovalManager,
) -> bool:

    print_test(
        6,
        "APPROVAL HISTORY",
    )

    strategy = """
AI Marketing Strategy
Budget: ₹50,000
Goal: 1,000 signups
""".strip()

    session = manager.create_session(
        strategy
    )

    manager.request_revision(
        session,
        feedback=(
            "Improve the channel allocation."
        ),
    )

    manager.apply_revision(
        session,
        """
Revised AI Marketing Strategy
Budget: ₹50,000
Improved channel allocation.
""".strip(),
    )

    manager.approve(
        session,
        feedback="Approved after revision.",
    )

    history = manager.get_history(
        session
    )

    print()
    print("Approval history:")

    for index, item in enumerate(
        history,
        start=1,
    ):
        print()
        print(f"Decision {index}:")
        print(item)

    return (
        assert_pass(
            len(history) == 2,
            "History count",
        )
        and assert_pass(
            history[0]["status"]
            == "revision_requested",
            "First decision",
        )
        and assert_pass(
            history[1]["status"]
            == "approved",
            "Second decision",
        )
    )


# ============================================================
# TEST 7
# ============================================================

def test_validation(
    manager: HumanApprovalManager,
) -> bool:

    print_test(
        7,
        "VALIDATION",
    )

    passed = True

    try:
        manager.create_session("")
        passed = False
    except ValueError:
        print(
            "Empty strategy rejected: PASS"
        )

    session = manager.create_session(
        "Test strategy"
    )

    try:
        manager.request_revision(
            session,
            "",
        )
        passed = False
    except ValueError:
        print(
            "Empty revision feedback rejected: PASS"
        )

    return assert_pass(
        passed,
        "Validation",
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("STEP 3.1 - HUMAN APPROVAL TEST")
    print("=" * 60)

    print()
    print(
        "This test does NOT call Groq."
    )

    print()
    print(
        "Testing human-in-the-loop approval workflow."
    )

    manager = HumanApprovalManager(
        reviewer="project_owner"
    )

    results = []

    # --------------------------------------------------------
    # TEST 1
    # --------------------------------------------------------

    strategy = """
AI Marketing Strategy

Product:
AI-powered Study Assistant

Audience:
College students aged 18-25

Budget:
₹50,000

Goal:
1,000 signups
""".strip()

    session = manager.create_session(
        strategy
    )

    results.append(
        test_session_creation(manager)
    )

    # --------------------------------------------------------
    # TEST 2
    # --------------------------------------------------------

    results.append(
        test_approve(
            manager,
            session,
        )
    )

    # --------------------------------------------------------
    # TEST 3
    # --------------------------------------------------------

    results.append(
        test_revision(manager)
    )

    # --------------------------------------------------------
    # TEST 4
    # --------------------------------------------------------

    results.append(
        test_apply_revision(manager)
    )

    # --------------------------------------------------------
    # TEST 5
    # --------------------------------------------------------

    results.append(
        test_reapprove_after_revision(
            manager
        )
    )

    # --------------------------------------------------------
    # TEST 6
    # --------------------------------------------------------

    results.append(
        test_approval_history(
            manager
        )
    )

    # --------------------------------------------------------
    # TEST 7
    # --------------------------------------------------------

    results.append(
        test_validation(
            manager
        )
    )

    # ========================================================
    # FINAL VERIFICATION
    # ========================================================

    print()
    print("=" * 60)
    print("STEP 3.1 VERIFICATION")
    print("=" * 60)

    names = [
        "Session creation",
        "Human approval",
        "Revision request",
        "Apply revision",
        "Re-approval",
        "Approval history",
        "Validation",
    ]

    for name, result in zip(
        names,
        results,
    ):
        print(
            f"{name}:",
            "PASS" if result else "FAIL",
        )

    print()

    if all(results):

        print("=" * 60)
        print(
            "STEP 3.1 COMPLETE - "
            "HUMAN APPROVAL WORKFLOW PASSED"
        )
        print("=" * 60)

    else:

        print("=" * 60)
        print(
            "STEP 3.1 FAILED - "
            "CHECK THE FAILED TEST"
        )
        print("=" * 60)

        raise SystemExit(1)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()