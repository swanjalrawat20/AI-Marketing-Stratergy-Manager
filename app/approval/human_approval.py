from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


# ============================================================
# APPROVAL STATUS
# ============================================================

class ApprovalStatus(str, Enum):
    """
    Possible states of a human approval workflow.
    """

    PENDING = "pending"
    APPROVED = "approved"
    REVISION_REQUESTED = "revision_requested"


# ============================================================
# APPROVAL DECISION
# ============================================================

@dataclass
class ApprovalDecision:
    """
    Represents one human approval/revision decision.
    """

    status: ApprovalStatus

    feedback: str = ""

    reviewer: str = "human"

    timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    revision_number: int = 0

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the decision into a serializable dictionary.
        """

        return {
            "status": self.status.value,
            "feedback": self.feedback,
            "reviewer": self.reviewer,
            "timestamp": self.timestamp,
            "revision_number": self.revision_number,
        }


# ============================================================
# APPROVAL SESSION
# ============================================================

@dataclass
class ApprovalSession:
    """
    Stores the complete human approval workflow for one strategy.
    """

    strategy: str

    status: ApprovalStatus = ApprovalStatus.PENDING

    revision_number: int = 0

    current_feedback: str = ""

    history: list[ApprovalDecision] = field(
        default_factory=list
    )

    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    def record_decision(
        self,
        decision: ApprovalDecision,
    ) -> None:
        """
        Record a human decision.
        """

        self.status = decision.status
        self.current_feedback = decision.feedback

        if decision.status == ApprovalStatus.REVISION_REQUESTED:
            self.revision_number += 1

        self.history.append(decision)

        self.updated_at = datetime.now().isoformat()

    def update_strategy(
        self,
        revised_strategy: str,
    ) -> None:
        """
        Replace the current strategy after a revision.
        """

        if not revised_strategy or not revised_strategy.strip():
            raise ValueError(
                "revised_strategy cannot be empty"
            )

        self.strategy = revised_strategy.strip()

        self.status = ApprovalStatus.PENDING

        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the session into a serializable dictionary.
        """

        return {
            "strategy": self.strategy,
            "status": self.status.value,
            "revision_number": self.revision_number,
            "current_feedback": self.current_feedback,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "history": [
                decision.to_dict()
                for decision in self.history
            ],
        }


# ============================================================
# HUMAN APPROVAL MANAGER
# ============================================================

class HumanApprovalManager:
    """
    Controls the human-in-the-loop approval process.

    Workflow:

        AI strategy
             ↓
        Human review
          /      \
      approve   revise
         ↓        ↓
       final    revision
                  ↓
              human review
    """

    def __init__(
        self,
        reviewer: str = "human",
    ) -> None:

        self.reviewer = reviewer

    # ========================================================
    # CREATE SESSION
    # ========================================================

    def create_session(
        self,
        strategy: str,
    ) -> ApprovalSession:

        if not strategy or not strategy.strip():
            raise ValueError(
                "strategy cannot be empty"
            )

        return ApprovalSession(
            strategy=strategy.strip()
        )

    # ========================================================
    # APPROVE
    # ========================================================

    def approve(
        self,
        session: ApprovalSession,
        feedback: str = "",
    ) -> ApprovalSession:
        """
        Approve the current strategy.
        """

        decision = ApprovalDecision(
            status=ApprovalStatus.APPROVED,
            feedback=feedback.strip(),
            reviewer=self.reviewer,
            revision_number=session.revision_number,
        )

        session.record_decision(decision)

        return session

    # ========================================================
    # REQUEST REVISION
    # ========================================================

    def request_revision(
        self,
        session: ApprovalSession,
        feedback: str,
    ) -> ApprovalSession:
        """
        Ask the AI workflow to revise the strategy.
        """

        if not feedback or not feedback.strip():
            raise ValueError(
                "Revision feedback cannot be empty."
            )

        decision = ApprovalDecision(
            status=ApprovalStatus.REVISION_REQUESTED,
            feedback=feedback.strip(),
            reviewer=self.reviewer,
            revision_number=session.revision_number + 1,
        )

        session.record_decision(decision)

        return session

    # ========================================================
    # APPLY REVISION
    # ========================================================

    def apply_revision(
        self,
        session: ApprovalSession,
        revised_strategy: str,
    ) -> ApprovalSession:
        """
        Store the revised strategy and return the workflow
        to the human approval stage.
        """

        session.update_strategy(
            revised_strategy
        )

        return session

    # ========================================================
    # INTERACTIVE APPROVAL
    # ========================================================

    def request_human_decision(
        self,
        session: ApprovalSession,
        input_func: Callable[[str], str] = input,
    ) -> ApprovalSession:
        """
        Interactive terminal approval.

        Accepted choices:

        A / APPROVE
        R / REVISE
        """

        print()
        print("=" * 60)
        print("HUMAN APPROVAL REQUIRED")
        print("=" * 60)

        print()
        print("CURRENT MARKETING STRATEGY")
        print("-" * 60)
        print(session.strategy)

        print()
        print("-" * 60)
        print("REVISION NUMBER:")
        print(session.revision_number)

        print()
        print("Choose:")
        print("  A = Approve")
        print("  R = Request Revision")

        while True:

            choice = input_func(
                "\nYour decision [A/R]: "
            ).strip().lower()

            if choice in {
                "a",
                "approve",
                "approved",
            }:

                feedback = input_func(
                    "Optional approval comment: "
                ).strip()

                return self.approve(
                    session,
                    feedback=feedback,
                )

            if choice in {
                "r",
                "revise",
                "revision",
            }:

                feedback = input_func(
                    "Revision feedback: "
                ).strip()

                if not feedback:
                    print(
                        "Revision feedback cannot be empty."
                    )
                    continue

                return self.request_revision(
                    session,
                    feedback,
                )

            print(
                "Invalid choice. Enter A for approve "
                "or R for revise."
            )

    # ========================================================
    # FINAL STATUS
    # ========================================================

    def is_approved(
        self,
        session: ApprovalSession,
    ) -> bool:

        return (
            session.status
            == ApprovalStatus.APPROVED
        )

    # ========================================================
    # REVISION REQUIRED
    # ========================================================

    def needs_revision(
        self,
        session: ApprovalSession,
    ) -> bool:

        return (
            session.status
            == ApprovalStatus.REVISION_REQUESTED
        )

    # ========================================================
    # GET REVISION FEEDBACK
    # ========================================================

    def get_revision_feedback(
        self,
        session: ApprovalSession,
    ) -> str:

        return session.current_feedback

    # ========================================================
    # GET APPROVAL HISTORY
    # ========================================================

    def get_history(
        self,
        session: ApprovalSession,
    ) -> list[dict[str, Any]]:

        return [
            decision.to_dict()
            for decision in session.history
        ]


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    manager = HumanApprovalManager(
        reviewer="project_owner"
    )

    strategy = """
AI Marketing Strategy

Product:
AI-powered Study Assistant

Target Audience:
College students aged 18-25

Budget:
₹50,000

Goal:
1,000 signups

Channels:
- Instagram
- Influencer Marketing
- Content Marketing
- Referral Marketing

Strategy:
Use short-form educational content, student influencers,
free trials and referral campaigns to drive signups.
"""

    session = manager.create_session(
        strategy
    )

    session = manager.request_human_decision(
        session
    )

    print()
    print("=" * 60)
    print("APPROVAL RESULT")
    print("=" * 60)

    print()
    print(session.to_dict())