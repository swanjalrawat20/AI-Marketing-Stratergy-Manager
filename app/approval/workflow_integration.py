"""
STEP 3.2 - HUMAN APPROVAL + AGENT WORKFLOW INTEGRATION

Connects an AI-generated marketing strategy to the existing
HumanApproval workflow.

This module does NOT call Groq.

Flow:

Agent Strategy
      ↓
Approval Session
      ↓
Human Review
      ↓
Approve OR Request Revision
      ↓
Revised Strategy
      ↓
Re-approval
      ↓
Final Approved Strategy
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from app.approval.human_approval import (
    ApprovalSession,
    HumanApprovalManager,
    ApprovalStatus,
)


class ApprovalWorkflow:
    """
    Integration layer between an AI-generated strategy and
    the HumanApprovalManager.

    The workflow itself does not call an LLM.

    Responsibilities:
        - create approval session
        - expose current strategy
        - approve strategy
        - request human revision
        - apply revised strategy
        - expose approval state
        - expose approval history
        - serialize workflow state
    """

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        strategy: str,
        metadata: Optional[Dict[str, Any]] = None,
        reviewer: str = "project_owner",
    ) -> None:

        if not strategy or not strategy.strip():
            raise ValueError(
                "strategy cannot be empty"
            )

        self.metadata = metadata or {}

        self.manager = HumanApprovalManager(
            reviewer=reviewer
        )

        self.session = self.manager.create_session(
            strategy=strategy
        )

    # ========================================================
    # APPROVE
    # ========================================================

    def approve(
        self,
        feedback: str = "",
        reviewer: Optional[str] = None,
    ) -> ApprovalSession:
        """
        Approve the current strategy.

        Returns the updated ApprovalSession.
        """

        if reviewer is not None:
            original_reviewer = self.manager.reviewer
            self.manager.reviewer = reviewer

            try:
                return self.manager.approve(
                    self.session,
                    feedback=feedback,
                )
            finally:
                self.manager.reviewer = original_reviewer

        return self.manager.approve(
            self.session,
            feedback=feedback,
        )

    # ========================================================
    # REQUEST REVISION
    # ========================================================

    def request_revision(
        self,
        feedback: str,
        reviewer: Optional[str] = None,
    ) -> ApprovalSession:
        """
        Request a human revision of the current strategy.
        """

        if not feedback or not feedback.strip():
            raise ValueError(
                "Revision feedback cannot be empty."
            )

        if reviewer is not None:
            original_reviewer = self.manager.reviewer
            self.manager.reviewer = reviewer

            try:
                return self.manager.request_revision(
                    self.session,
                    feedback=feedback,
                )
            finally:
                self.manager.reviewer = original_reviewer

        return self.manager.request_revision(
            self.session,
            feedback=feedback,
        )

    # ========================================================
    # APPLY REVISION
    # ========================================================

    def apply_revision(
        self,
        revised_strategy: str,
    ) -> ApprovalSession:
        """
        Apply the revised AI-generated strategy.

        After applying the revision, the strategy returns to
        PENDING and must be reviewed again.
        """

        if not revised_strategy or not revised_strategy.strip():
            raise ValueError(
                "revised_strategy cannot be empty."
            )

        return self.manager.apply_revision(
            self.session,
            revised_strategy=revised_strategy,
        )

    # ========================================================
    # STATUS
    # ========================================================

    @property
    def status(self) -> ApprovalStatus:
        """
        Current approval status.
        """

        return self.session.status

    # ========================================================
    # REVISION NUMBER
    # ========================================================

    @property
    def revision_number(self) -> int:
        """
        Current revision number.
        """

        return self.session.revision_number

    # ========================================================
    # CURRENT STRATEGY
    # ========================================================

    @property
    def current_strategy(self) -> str:
        """
        Current strategy awaiting approval or already approved.
        """

        return self.session.strategy

    # ========================================================
    # FEEDBACK
    # ========================================================

    @property
    def current_feedback(self) -> str:
        """
        Most recent human feedback.
        """

        return self.session.current_feedback

    # ========================================================
    # IS APPROVED
    # ========================================================

    def is_approved(self) -> bool:
        """
        Return True when the current strategy is approved.
        """

        return self.manager.is_approved(
            self.session
        )

    # ========================================================
    # NEEDS REVISION
    # ========================================================

    def needs_revision(self) -> bool:
        """
        Return True when the human requested a revision.
        """

        return self.manager.needs_revision(
            self.session
        )

    # ========================================================
    # GET REVISION FEEDBACK
    # ========================================================

    def get_revision_feedback(self) -> str:
        """
        Return the latest revision feedback.
        """

        return self.manager.get_revision_feedback(
            self.session
        )

    # ========================================================
    # APPROVAL HISTORY
    # ========================================================

    def get_history(self) -> list[dict[str, Any]]:
        """
        Return the complete human approval history.
        """

        return self.manager.get_history(
            self.session
        )

    # ========================================================
    # HUMAN DECISION
    # ========================================================

    def request_human_decision(
        self,
        input_func=input,
    ) -> ApprovalSession:
        """
        Run the interactive terminal human approval step.
        """

        return self.manager.request_human_decision(
            self.session,
            input_func=input_func,
        )

    # ========================================================
    # SERIALIZATION
    # ========================================================

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the complete approval workflow into a
        serializable dictionary.

        This is used by the Step 3.2 integration test and
        can later be used by the UI/API layer.
        """

        return {
            "status": self.status.value,
            "revision_number": self.revision_number,
            "strategy": self.current_strategy,
            "current_feedback": self.current_feedback,
            "metadata": self.metadata.copy(),
            "is_approved": self.is_approved(),
            "needs_revision": self.needs_revision(),
            "history": self.get_history(),
            "created_at": self.session.created_at,
            "updated_at": self.session.updated_at,
        }

    # ========================================================
    # FINAL APPROVED STRATEGY
    # ========================================================

    def get_approved_strategy(self) -> Optional[str]:
        """
        Return the strategy only if it is currently approved.

        Returns:
            Approved strategy string, or None if approval has
            not been granted.
        """

        if not self.is_approved():
            return None

        return self.current_strategy


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

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

    workflow = ApprovalWorkflow(
        strategy=INITIAL_STRATEGY,
        metadata={
            "source": "agent",
            "campaign": "AI Study Assistant",
        },
    )

    print("=" * 60)
    print("APPROVAL WORKFLOW DEMO")
    print("=" * 60)

    print()
    print("Initial:")
    print(workflow.to_dict())

    workflow.request_revision(
        feedback=(
            "Reduce influencer spending and increase "
            "Instagram advertising."
        )
    )

    print()
    print("After revision request:")
    print(workflow.to_dict())

    workflow.apply_revision(
        revised_strategy=REVISED_STRATEGY
    )

    print()
    print("After applying revised strategy:")
    print(workflow.to_dict())

    workflow.approve(
        feedback="Approved after revision."
    )

    print()
    print("Final:")
    print(workflow.to_dict())

    print()
    print("Approved strategy:")
    print(workflow.get_approved_strategy())