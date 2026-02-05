"""Status inference engine for automatic status transitions."""

from datetime import datetime
from typing import List, Optional

from .thread_analyzer import ThreadAnalyzer

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))

from models_v2 import (
    VendorStatus, EmailThread, StatusTransition, VendorState
)
from config_models import ProjectConfig, StatusTransitionRule


class StatusInferencer:
    """Infer vendor status based on communication patterns and keywords."""

    # Default status progression (if no config rules)
    DEFAULT_PROGRESSION = {
        VendorStatus.INITIAL_CONTACT: VendorStatus.RFP_SENT,
        VendorStatus.RFP_SENT: VendorStatus.QUOTE_WAITING,
        VendorStatus.QUOTE_WAITING: VendorStatus.QUOTE_RECEIVED,
        VendorStatus.QUOTE_RECEIVED: VendorStatus.REVIEWING,
        VendorStatus.REVIEWING: VendorStatus.NEGOTIATING,
        VendorStatus.NEGOTIATING: VendorStatus.CONTRACT_REVIEW,
    }

    # Status string to enum mapping
    STATUS_MAP = {
        "initial_contact": VendorStatus.INITIAL_CONTACT,
        "rfp_sent": VendorStatus.RFP_SENT,
        "quote_waiting": VendorStatus.QUOTE_WAITING,
        "견적 대기": VendorStatus.QUOTE_WAITING,
        "quote_received": VendorStatus.QUOTE_RECEIVED,
        "reviewing": VendorStatus.REVIEWING,
        "검토 중": VendorStatus.REVIEWING,
        "negotiating": VendorStatus.NEGOTIATING,
        "협상 중": VendorStatus.NEGOTIATING,
        "contract_review": VendorStatus.CONTRACT_REVIEW,
        "계약 검토": VendorStatus.CONTRACT_REVIEW,
        "on_hold": VendorStatus.ON_HOLD,
        "보류": VendorStatus.ON_HOLD,
        "excluded": VendorStatus.EXCLUDED,
        "제외": VendorStatus.EXCLUDED,
    }

    def __init__(self, config: Optional[ProjectConfig] = None):
        """Initialize with optional project config."""
        self.config = config

    def _parse_status(self, status_str: str) -> Optional[VendorStatus]:
        """Convert status string to VendorStatus enum."""
        status_lower = status_str.lower().replace(" ", "_")
        return self.STATUS_MAP.get(status_lower) or self.STATUS_MAP.get(status_str)

    def infer_status(
        self,
        current: VendorStatus,
        threads: List[EmailThread],
        keyword_signals: List[str],
    ) -> Optional[StatusTransition]:
        """
        Infer next status based on current state and signals.

        Args:
            current: Current vendor status
            threads: Analyzed email threads
            keyword_signals: Keywords detected from messages

        Returns:
            StatusTransition if change recommended, None otherwise
        """
        # Priority 1: Active negotiation detection (bidirectional communication)
        if any(t.is_active_negotiation for t in threads):
            if current not in [VendorStatus.NEGOTIATING, VendorStatus.CONTRACT_REVIEW]:
                return StatusTransition(
                    from_status=current,
                    to_status=VendorStatus.NEGOTIATING,
                    trigger="active_thread_detected",
                    confidence=0.95,
                    evidence=[
                        f"Thread {t.thread_id}: {t.inbound_count} inbound, {t.outbound_count} outbound"
                        for t in threads if t.is_active_negotiation
                    ][:3],  # Limit evidence
                    requires_approval=False,
                )

        # Priority 2: Config-based rules
        if self.config and self.config.status_rules:
            for rule in self.config.status_rules:
                if self._rule_matches(rule, current, keyword_signals):
                    to_status = self._parse_status(rule.to_status)
                    if to_status and to_status != current:
                        return StatusTransition(
                            from_status=current,
                            to_status=to_status,
                            trigger=rule.triggers[0] if rule.triggers else "rule_match",
                            confidence=0.9 if rule.direction == "positive" else 0.7,
                            evidence=[f"Matched rule: {rule.triggers}"],
                            requires_approval=not rule.auto_apply,
                        )

        # Priority 3: Keyword-based inference (fallback)
        transition = self._infer_from_keywords(current, keyword_signals)
        if transition:
            return transition

        return None

    def _rule_matches(
        self,
        rule: StatusTransitionRule,
        current: VendorStatus,
        signals: List[str],
    ) -> bool:
        """Check if a rule matches current state and signals."""
        # Check from_status
        if rule.from_status != "*":
            from_status = self._parse_status(rule.from_status)
            if from_status != current:
                return False

        # Check triggers
        signals_lower = [s.lower() for s in signals]
        for trigger in rule.triggers:
            if trigger.lower() in signals_lower:
                return True
            # Partial match
            for signal in signals_lower:
                if trigger.lower() in signal:
                    return True

        return False

    def _infer_from_keywords(
        self,
        current: VendorStatus,
        signals: List[str],
    ) -> Optional[StatusTransition]:
        """Fallback keyword-based inference."""
        signals_text = " ".join(signals).lower()

        # Quote received signals
        if any(kw in signals_text for kw in ["견적 수령", "견적 도착", "견적서"]):
            if current in [VendorStatus.QUOTE_WAITING, VendorStatus.RFP_SENT]:
                return StatusTransition(
                    from_status=current,
                    to_status=VendorStatus.QUOTE_RECEIVED,
                    trigger="견적 수령",
                    confidence=0.85,
                    evidence=["Keyword detected: 견적"],
                )

        # Negotiation signals
        if any(kw in signals_text for kw in ["협상", "미팅", "회의"]):
            if current in [VendorStatus.REVIEWING, VendorStatus.QUOTE_RECEIVED]:
                return StatusTransition(
                    from_status=current,
                    to_status=VendorStatus.NEGOTIATING,
                    trigger="협상 시작",
                    confidence=0.8,
                    evidence=["Keyword detected: 협상/미팅"],
                )

        # Contract signals
        if any(kw in signals_text for kw in ["계약", "법무", "contract"]):
            if current == VendorStatus.NEGOTIATING:
                return StatusTransition(
                    from_status=current,
                    to_status=VendorStatus.CONTRACT_REVIEW,
                    trigger="계약 검토",
                    confidence=0.8,
                    evidence=["Keyword detected: 계약"],
                )

        return None

    def infer_vendor_status(self, state: VendorState) -> Optional[StatusTransition]:
        """
        Infer status for a complete VendorState.

        Args:
            state: Current vendor state with threads, attachments, etc.

        Returns:
            StatusTransition if change recommended
        """
        # Collect signals from various sources
        signals = []

        # From notes
        if state.notes:
            signals.append(state.notes)

        # From next_action
        if state.next_action:
            signals.append(state.next_action)

        # From quote status
        if state.quote.options:
            signals.append("견적 수령")

        return self.infer_status(state.status, state.threads, signals)


def create_inferencer(config_path: Optional[str] = None) -> StatusInferencer:
    """Factory function to create StatusInferencer with config."""
    config = None
    if config_path:
        from pathlib import Path
        config = ProjectConfig.from_yaml(Path(config_path))
    return StatusInferencer(config)
