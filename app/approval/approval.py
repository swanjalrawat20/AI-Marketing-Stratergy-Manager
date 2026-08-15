from datetime import datetime
from enum import Enum


class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REVISION_REQUESTED = "revision_requested"


class ApprovalSession:
    """
    Stores the complete human-approval state for one strategy.

    Flow:

        Agent strategy
              ↓
           PENDING
          ↙       ↘
     APPROVED   REVISION_REQUESTED
                    ↓
              revised strategy
                    ↓
                 PENDING
                    ↓
                APPROVED
    """

    def __init__(self, strategy: str):
        if not strategy or not strategy.strip():
            raise ValueError("Strategy cannot be empty.")

        self.strategy = strategy
        self.status = ApprovalStatus.PENDING
        self.revision_number = 0

        self.feedback = None
        self.reviewer = None

        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

        self._history = []

    # ========================================================
    # APPROVAL
    # ========================================================

    def approve(
        self,
        feedback: str = "",
        reviewer: str = "project_owner",
    ):
        if self.status != ApprovalStatus.PENDING:
            raise ValueError(
                "Strategy can only be approved when status is pending."
            )

        self.status = ApprovalStatus.APPROVED
        self.feedback = feedback
        self.reviewer = reviewer
        self.updated_at = datetime.now().isoformat()

        self._history.append(
            {
                "status": self.status.value,
                "feedback": feedback,
                "reviewer": reviewer,
                "timestamp": self.updated_at,
                "revision_number": self.revision_number,
            }
        )

    # ========================================================
    # REVISION REQUEST
    # ========================================================

    def request_revision(
        self,
        feedback: str,
        reviewer: str = "project_owner",
    ):
        if not feedback or not feedback.strip():
            raise ValueError(
                "Revision feedback cannot be empty."
            )

        if self.status != ApprovalStatus.PENDING:
            raise ValueError(
                "Revision can only be requested when status is pending."
            )

        self.revision_number += 1

        self.status = ApprovalStatus.REVISION_REQUESTED
        self.feedback = feedback
        self.reviewer = reviewer
        self.updated_at = datetime.now().isoformat()

        self._history.append(
            {
                "status": self.status.value,
                "feedback": feedback,
                "reviewer": reviewer,
                "timestamp": self.updated_at,
                "revision_number": self.revision_number,
            }
        )

    # ========================================================
    # APPLY REVISION
    # ========================================================

    def apply_revision(self, revised_strategy: str):
        if not revised_strategy or not revised_strategy.strip():
            raise ValueError(
                "Revised strategy cannot be empty."
            )

        if self.status != ApprovalStatus.REVISION_REQUESTED:
            raise ValueError(
                "A revision can only be applied after "
                "a revision has been requested."
            )

        self.strategy = revised_strategy

        # Revision number is preserved.
        # The strategy goes back into the approval queue.
        self.status = ApprovalStatus.PENDING

        self.updated_at = datetime.now().isoformat()

    # ========================================================
    # STATE HELPERS
    # ========================================================

    def is_approved(self) -> bool:
        return self.status == ApprovalStatus.APPROVED

    def needs_revision(self) -> bool:
        return self.status == ApprovalStatus.REVISION_REQUESTED

    def is_pending(self) -> bool:
        return self.status == ApprovalStatus.PENDING

    # ========================================================
    # HISTORY
    # ========================================================

    def get_history(self):
        return list(self._history)

    # ========================================================
    # SERIALIZATION
    # ========================================================

    def to_dict(self):
        return {
            "strategy": self.strategy,
            "status": self.status.value,
            "revision_number": self.revision_number,
            "feedback": self.feedback,
            "reviewer": self.reviewer,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "history": self.get_history(),
        }