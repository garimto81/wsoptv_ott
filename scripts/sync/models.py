"""Data models for email and Slack sync operations."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class EmailStatus(Enum):
    """Email processing status."""

    PENDING = "pending"
    WAITING = "waiting"
    COMPLETED = "completed"


class EmailDirection(Enum):
    """Email direction."""

    SENT = "sent"
    RECEIVED = "received"


@dataclass
class EmailLogEntry:
    """Email log entry data."""

    email_id: str
    direction: EmailDirection
    date: datetime
    sender: str
    recipient: str
    subject: str
    summary: str
    status: EmailStatus
    next_action: str
    company: Optional[str] = None


class ActionItemStatus(Enum):
    """Action item completion status."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class SlackDecision:
    """Slack decision record."""

    decision_id: str
    timestamp: datetime
    channel: str
    participants: list[str]
    decision_text: str
    rationale: str
    follow_ups: list[str] = field(default_factory=list)


@dataclass
class SlackActionItem:
    """Slack action item."""

    assignee: str
    description: str
    source_channel: str
    source_date: datetime
    requester: str
    deadline: Optional[datetime]
    status: ActionItemStatus
    slack_ts: str


@dataclass
class SyncResult:
    """Result of a sync operation."""

    added: int = 0
    skipped: int = 0
    errors: int = 0

    def __str__(self) -> str:
        """String representation of sync result."""
        return f"Added: {self.added}, Skipped: {self.skipped}, Errors: {self.errors}"
