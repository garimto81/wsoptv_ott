"""
Slack Lists synchronization script.

Syncs Slack Kanban board (Lists) with local VENDOR-DASHBOARD.md and SLACK-LOG.md.
Also updates pinned messages in the project channel.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add C:\claude to path for lib.slack import
_script_dir = Path(__file__).resolve().parent
_wsoptv_root = _script_dir.parents[1]
_claude_root = _script_dir.parents[2]
sys.path.insert(0, str(_claude_root))

from lib.slack import SlackClient, SlackUserClient  # noqa: E402

# Import models from same directory
try:
    from .models import SyncResult
except ImportError:
    from models import SyncResult


# Slack Lists Configuration (from slack-kanban-config.md)
LISTS_CONFIG = {
    "list_id": "F0ACQJS6KND",
    "team_id": "T03QGJ73GBB",
    "channel_id": "C09TX3M1J2W",
    "pinned_message_ts": "1770011097.422069",  # 고정 요약 메시지 ts
    "columns": {
        "vendor_name": "Col0ACBLXEU66",  # 업체명
        "status": "Col0ABWF6TEQP",        # 상태
        "quote": "Col0ACQRUJ073",         # 견적
        "last_contact": "Col0ACQRVGHKK",  # 최종 연락
        "next_action": "Col0ABWF0K4DV",   # 다음 액션
        "notes": "Col0ABWF1LL9M",         # 비고
    },
    "status_options": {
        "검토 중": "OptN4JBLQ9C",
        "견적 대기": "Opt2QCAWCYN",
        "협상 중": "OptZSZEAEHJ",
        "보류": "OptBAAGMVM4",
        "RFP 검토": "Opt987UPKAJ",  # 맑음소프트 상태
    },
    "items": {
        "메가존클라우드": "Rec0AC9KQD7TQ",
        "맑음소프트": "Rec0ACBM3P1PC",
        "Brightcove": "Rec0AC9KQQEDC",
        "Vimeo OTT": "Rec0ACQJY2W65",
    },
}


class ListsSyncManager:
    """Manage synchronization with Slack Lists."""

    def __init__(self):
        """Initialize with both bot and user clients."""
        self.bot_client = SlackClient()
        try:
            self.user_client = SlackUserClient()
        except Exception as e:
            print(f"Warning: User token not available, Lists API disabled: {e}")
            self.user_client = None

    def get_list_items(self) -> list[dict]:
        """
        Fetch all items from Slack List.

        Returns:
            List of item dictionaries with parsed fields
        """
        if not self.user_client:
            raise RuntimeError("User token required for Lists API")

        result = self.user_client.get_list_items(LISTS_CONFIG["list_id"])

        if not result.get("ok"):
            raise RuntimeError(f"Failed to fetch list items: {result}")

        items = []
        for item in result.get("items", []):
            parsed = self._parse_item(item)
            if parsed:
                items.append(parsed)

        return items

    def _parse_item(self, item: dict) -> Optional[dict]:
        """Parse a list item into structured data."""
        fields_list = item.get("fields", [])
        row_id = item.get("id", "")

        # Convert list of fields to dict by column_id
        fields = {}
        for field in fields_list:
            col_id = field.get("column_id", "")
            if col_id:
                fields[col_id] = field

        def get_text_field(column_id: str) -> str:
            """Extract text from rich_text field."""
            field = fields.get(column_id, {})
            # First try 'text' directly
            if field.get("text"):
                return field.get("text", "")
            # Then try rich_text parsing
            rich_text = field.get("rich_text", [])
            if rich_text:
                elements = rich_text[0].get("elements", [])
                if elements:
                    sections = elements[0].get("elements", [])
                    if sections:
                        return sections[0].get("text", "")
            return ""

        def get_select_field(column_id: str) -> str:
            """Extract selected option from select field."""
            field = fields.get(column_id, {})
            # Try 'select' array first
            select_arr = field.get("select", [])
            if select_arr:
                option_id = select_arr[0]
            else:
                option_id = field.get("value", "")
            # Reverse lookup option name
            for name, opt_id in LISTS_CONFIG["status_options"].items():
                if opt_id == option_id:
                    return name
            return ""

        def get_date_field(column_id: str) -> Optional[datetime]:
            """Extract date from date field."""
            field = fields.get(column_id, {})
            # Try 'date' array first
            date_arr = field.get("date", [])
            if date_arr:
                date_str = date_arr[0]
            else:
                date_str = field.get("value", "")
            if date_str:
                try:
                    return datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    pass
            return None

        return {
            "row_id": row_id,
            "vendor_name": get_text_field(LISTS_CONFIG["columns"]["vendor_name"]),
            "status": get_select_field(LISTS_CONFIG["columns"]["status"]),
            "quote": get_text_field(LISTS_CONFIG["columns"]["quote"]),
            "last_contact": get_date_field(LISTS_CONFIG["columns"]["last_contact"]),
            "next_action": get_text_field(LISTS_CONFIG["columns"]["next_action"]),
            "notes": get_text_field(LISTS_CONFIG["columns"]["notes"]),
        }

    def update_item(
        self,
        vendor_name: str,
        status: Optional[str] = None,
        quote: Optional[str] = None,
        last_contact: Optional[datetime] = None,
        next_action: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> bool:
        """
        Update a vendor item in Slack List.

        Args:
            vendor_name: Name of vendor to update
            status: New status (must match status_options keys)
            quote: Quote text
            last_contact: Last contact date
            next_action: Next action text
            notes: Notes text

        Returns:
            True if successful
        """
        if not self.user_client:
            raise RuntimeError("User token required for Lists API")

        row_id = LISTS_CONFIG["items"].get(vendor_name)
        if not row_id:
            raise ValueError(f"Unknown vendor: {vendor_name}")

        cells = []

        if status:
            option_id = LISTS_CONFIG["status_options"].get(status)
            if option_id:
                cells.append({
                    "column_id": LISTS_CONFIG["columns"]["status"],
                    "row_id": row_id,
                    "select": [option_id],  # select는 배열 형식
                })

        if quote:
            cells.append({
                "column_id": LISTS_CONFIG["columns"]["quote"],
                "row_id": row_id,
                "rich_text": [{"type": "rich_text", "elements": [{"type": "rich_text_section", "elements": [{"type": "text", "text": quote}]}]}],
            })

        if last_contact:
            cells.append({
                "column_id": LISTS_CONFIG["columns"]["last_contact"],
                "row_id": row_id,
                "date": [last_contact.strftime("%Y-%m-%d")],  # date도 배열 형식
            })

        if next_action:
            cells.append({
                "column_id": LISTS_CONFIG["columns"]["next_action"],
                "row_id": row_id,
                "rich_text": [{"type": "rich_text", "elements": [{"type": "rich_text_section", "elements": [{"type": "text", "text": next_action}]}]}],
            })

        if notes:
            cells.append({
                "column_id": LISTS_CONFIG["columns"]["notes"],
                "row_id": row_id,
                "rich_text": [{"type": "rich_text", "elements": [{"type": "rich_text_section", "elements": [{"type": "text", "text": notes}]}]}],
            })

        if not cells:
            return False

        result = self.user_client._client.api_call(
            "slackLists.items.update",
            json={
                "list_id": LISTS_CONFIG["list_id"],
                "cells": cells,
            },
        )

        return result.data.get("ok", False)

    def generate_summary_message(self, items: list[dict]) -> str:
        """
        Generate summary message for Slack posting.

        Args:
            items: List of vendor items

        Returns:
            Formatted Slack message with blocks support
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        team_id = LISTS_CONFIG["team_id"]
        list_id = LISTS_CONFIG["list_id"]
        list_url = f"https://ggproduction.slack.com/lists/{team_id}/{list_id}"

        lines = [
            f"<{list_url}|*WSOPTV Vendor Status*> (auto-update: {now})",
            "",
        ]

        # Group by status
        status_groups = {}
        for item in items:
            status = item.get("status", "미정")
            if status not in status_groups:
                status_groups[status] = []
            status_groups[status].append(item)

        # Status emoji mapping
        status_emoji = {
            "협상 중": ":large_green_circle:",
            "검토 중": ":large_yellow_circle:",
            "견적 대기": ":hourglass:",
            "보류": ":red_circle:",
        }

        for status, vendors in status_groups.items():
            emoji = status_emoji.get(status, "📋")
            lines.append(f"{emoji} *{status}* ({len(vendors)}개)")

            for vendor in vendors:
                name = vendor.get("vendor_name", "")
                quote = vendor.get("quote", "-")
                next_act = vendor.get("next_action", "-")
                lines.append(f"  • {name}: {quote}")
                if next_act and next_act != "-":
                    lines.append(f"    └ 다음: {next_act}")

            lines.append("")

        lines.append("_상세 현황: VENDOR-DASHBOARD.md 참조_")

        return "\n".join(lines)

    def post_summary(self, message: str, update_existing: bool = True) -> Optional[str]:
        """
        Post or update summary message to project channel.

        Args:
            message: Message text
            update_existing: If True, update pinned message instead of posting new

        Returns:
            Message timestamp if successful
        """
        channel_id = LISTS_CONFIG["channel_id"]
        pinned_ts = LISTS_CONFIG.get("pinned_message_ts")

        if update_existing and pinned_ts:
            # Update existing pinned message
            result = self.bot_client._client.chat_update(
                channel=channel_id,
                ts=pinned_ts,
                text=message,
            )
            return result.data.get("ts") if result.data.get("ok") else None
        else:
            # Post new message (fallback)
            result = self.bot_client.send_message(channel_id, message)
            return result.ts if result and result.ok else None


def sync_lists_to_dashboard(
    dashboard_path: Path,
    dry_run: bool = False,
) -> SyncResult:
    """
    Sync Slack Lists to VENDOR-DASHBOARD.md.

    Args:
        dashboard_path: Path to VENDOR-DASHBOARD.md
        dry_run: If True, only show what would be updated

    Returns:
        SyncResult with counts
    """
    result = SyncResult()

    try:
        manager = ListsSyncManager()
        items = manager.get_list_items()

        print(f"Fetched {len(items)} items from Slack List")

        for item in items:
            print(f"  - {item['vendor_name']}: {item['status']}")
            result.added += 1

        if dry_run:
            print("\n=== DRY RUN ===")
            print("Would update VENDOR-DASHBOARD.md with above data")
            return result

        # TODO: Parse and update VENDOR-DASHBOARD.md
        # For now, just output the data
        print("\nLists data fetched successfully")

    except Exception as e:
        print(f"Error: {e}")
        result.errors += 1

    return result


def post_daily_summary(dry_run: bool = False) -> bool:
    """
    Post daily summary to Slack channel.

    Args:
        dry_run: If True, only show message without posting

    Returns:
        True if successful
    """
    try:
        manager = ListsSyncManager()
        items = manager.get_list_items()

        message = manager.generate_summary_message(items)

        if dry_run:
            print("\n=== DRY RUN - Message Preview ===")
            print(message)
            return True

        ts = manager.post_summary(message)
        if ts:
            print(f"Summary posted to Slack (ts: {ts})")
            return True
        else:
            print("Failed to post summary")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False


class IncrementalSyncState:
    """Manage incremental sync state for Slack Lists updates."""

    STATE_FILE = Path("C:/claude/wsoptv_ott/docs/management/.slacklist_state.json")

    def __init__(self):
        """Load existing state or initialize new."""
        self.state = self._load_state()

    def _load_state(self) -> dict:
        """Load state from file or return default."""
        if self.STATE_FILE.exists():
            try:
                return json.loads(self.STATE_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return self._default_state()

    def _default_state(self) -> dict:
        """Return default state structure."""
        return {
            "version": "1.0",
            "last_sync": None,
            "processed": {
                "gmail": {"last_email_date": None, "email_ids": []},
                "slack": {"last_ts": None, "message_ts": []},
            },
            "vendors": {},
            "pending_changes": [],
        }

    def save(self):
        """Save current state to file."""
        self.state["last_sync"] = datetime.now().isoformat()
        self.STATE_FILE.write_text(
            json.dumps(self.state, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )

    def is_gmail_processed(self, email_id: str) -> bool:
        """Check if email was already processed."""
        return email_id in self.state["processed"]["gmail"]["email_ids"]

    def mark_gmail_processed(self, email_id: str):
        """Mark email as processed."""
        if email_id not in self.state["processed"]["gmail"]["email_ids"]:
            self.state["processed"]["gmail"]["email_ids"].append(email_id)

    def is_slack_processed(self, ts: str) -> bool:
        """Check if Slack message was already processed."""
        return ts in self.state["processed"]["slack"]["message_ts"]

    def mark_slack_processed(self, ts: str):
        """Mark Slack message as processed."""
        if ts not in self.state["processed"]["slack"]["message_ts"]:
            self.state["processed"]["slack"]["message_ts"].append(ts)

    def get_last_slack_ts(self) -> Optional[str]:
        """Get last processed Slack timestamp."""
        return self.state["processed"]["slack"]["last_ts"]

    def update_last_slack_ts(self, ts: str):
        """Update last processed Slack timestamp."""
        self.state["processed"]["slack"]["last_ts"] = ts

    def add_pending_change(self, change: dict):
        """Add a pending change for user review."""
        change["detected_at"] = datetime.now().isoformat()
        self.state["pending_changes"].append(change)

    def get_pending_changes(self) -> list:
        """Get all pending changes."""
        return self.state["pending_changes"]

    def clear_pending_changes(self):
        """Clear pending changes after applying."""
        self.state["pending_changes"] = []

    def update_vendor(self, vendor_name: str, updates: dict):
        """Update vendor state."""
        if vendor_name not in self.state["vendors"]:
            self.state["vendors"][vendor_name] = {"changes_history": []}

        vendor = self.state["vendors"][vendor_name]
        for key, value in updates.items():
            if key != "changes_history":
                old_value = vendor.get(key)
                if old_value != value:
                    vendor["changes_history"].append({
                        "field": key,
                        "old": old_value,
                        "new": value,
                        "changed_at": datetime.now().isoformat(),
                    })
                vendor[key] = value

    def get_vendor_state(self, vendor_name: str) -> Optional[dict]:
        """Get current vendor state."""
        return self.state["vendors"].get(vendor_name)

    def get_stats(self) -> dict:
        """Get sync statistics."""
        return {
            "last_sync": self.state.get("last_sync"),
            "gmail_processed": len(self.state["processed"]["gmail"]["email_ids"]),
            "slack_processed": len(self.state["processed"]["slack"]["message_ts"]),
            "vendors_tracked": len(self.state["vendors"]),
            "pending_changes": len(self.state["pending_changes"]),
        }


class VendorChangeDetector:
    """Detect vendor-related changes from Gmail and Slack messages."""

    # Vendor detection patterns (domain → vendor name)
    VENDOR_DOMAINS = {
        "brightcove": "Brightcove",
        "megazone": "메가존클라우드",
        "megazonecloud": "메가존클라우드",
        "vimeo": "Vimeo OTT",
        "wecandeo": "맑음소프트 (WECANDEO)",
        "malgum": "맑음소프트 (WECANDEO)",
    }

    # Status transition keywords
    STATUS_KEYWORDS = {
        "견적 수령": ("견적 대기", "검토 중"),
        "견적 도착": ("견적 대기", "검토 중"),
        "협상 시작": ("검토 중", "협상 중"),
        "조건 협의": ("검토 중", "협상 중"),
        "계약서 검토": ("협상 중", "계약 진행"),
        "법무 검토": ("협상 중", "계약 진행"),
        "미수령": ("견적 대기", "보류"),
        "무응답": ("*", "보류"),
        "매각": ("*", "제외"),
        "서비스 종료": ("*", "제외"),
    }

    # Action keywords for next_action field
    ACTION_KEYWORDS = [
        "미팅", "회의", "연락", "확인", "검토", "요청", "피드백", "리마인더", "follow-up"
    ]

    def __init__(self):
        """Initialize detector with pattern cache."""
        self._changes = []

    def detect_vendor_from_email(self, sender: str, subject: str) -> Optional[str]:
        """Detect vendor from email sender or subject."""
        email_domain = sender.split("@")[-1].lower() if "@" in sender else ""

        for domain_key, vendor_name in self.VENDOR_DOMAINS.items():
            if domain_key in email_domain or domain_key in subject.lower():
                return vendor_name
        return None

    def detect_status_change(self, text: str) -> Optional[tuple]:
        """Detect status change from text content."""
        text_lower = text.lower()
        for keyword, (from_status, to_status) in self.STATUS_KEYWORDS.items():
            if keyword in text_lower:
                return (from_status, to_status, keyword)
        return None

    def detect_action_item(self, text: str) -> Optional[str]:
        """Detect action item from text content."""
        import re

        # Pattern: date-like content with action keyword
        date_pattern = r"(\d{1,2}[-/]\d{1,2}|\d{2}-\d{2})"
        action_pattern = "|".join(self.ACTION_KEYWORDS)

        if re.search(date_pattern, text) and re.search(action_pattern, text, re.IGNORECASE):
            # Extract the action item portion
            lines = text.split("\n")
            for line in lines:
                if re.search(date_pattern, line) and re.search(action_pattern, line, re.IGNORECASE):
                    return line.strip()[:100]  # Limit to 100 chars
        return None

    def analyze_gmail_messages(self, emails: list[dict]) -> list[dict]:
        """
        Analyze Gmail messages for vendor changes.

        Args:
            emails: List of email dicts with keys: sender, subject, body, date

        Returns:
            List of detected changes
        """
        changes = []

        for email in emails:
            vendor = self.detect_vendor_from_email(
                email.get("sender", ""),
                email.get("subject", "")
            )
            if not vendor:
                continue

            change = {
                "source": "gmail",
                "vendor": vendor,
                "date": email.get("date"),
                "subject": email.get("subject", ""),
            }

            # Check for status change
            full_text = f"{email.get('subject', '')} {email.get('body', '')}"
            status_change = self.detect_status_change(full_text)
            if status_change:
                change["status_change"] = {
                    "from": status_change[0],
                    "to": status_change[1],
                    "trigger": status_change[2],
                }

            # Check for action item
            action = self.detect_action_item(full_text)
            if action:
                change["next_action"] = action

            # Always update last_contact for vendor emails
            change["last_contact"] = email.get("date")

            changes.append(change)

        return changes

    def analyze_slack_messages(self, messages: list) -> list[dict]:
        """
        Analyze Slack messages for vendor-related changes.

        Args:
            messages: List of SlackMessage objects or dicts with keys: text, user, ts

        Returns:
            List of detected changes
        """
        changes = []

        for msg in messages:
            # Handle both pydantic models and dicts
            if hasattr(msg, "text"):
                text = getattr(msg, "text", "")
            else:
                text = msg.get("text", "") if isinstance(msg, dict) else ""

            # Detect vendor mentions in message
            detected_vendor = None
            for domain_key, vendor_name in self.VENDOR_DOMAINS.items():
                if domain_key in text.lower() or vendor_name.lower() in text.lower():
                    detected_vendor = vendor_name
                    break

            if not detected_vendor:
                # Also check for vendor names in Korean
                vendor_keywords = {
                    "메가존": "메가존클라우드",
                    "브라이트코브": "Brightcove",
                    "비메오": "Vimeo OTT",
                    "맑음소프트": "맑음소프트 (WECANDEO)",
                }
                for keyword, vendor_name in vendor_keywords.items():
                    if keyword in text:
                        detected_vendor = vendor_name
                        break

            if not detected_vendor:
                continue

            # Get ts from model or dict
            msg_ts = getattr(msg, "ts", None) if hasattr(msg, "ts") else (msg.get("ts") if isinstance(msg, dict) else None)

            change = {
                "source": "slack",
                "vendor": detected_vendor,
                "ts": msg_ts,
                "text_preview": text[:100],
            }

            # Check for status change
            status_change = self.detect_status_change(text)
            if status_change:
                change["status_change"] = {
                    "from": status_change[0],
                    "to": status_change[1],
                    "trigger": status_change[2],
                }

            # Check for action item
            action = self.detect_action_item(text)
            if action:
                change["next_action"] = action

            changes.append(change)

        return changes

    def merge_changes(self, gmail_changes: list[dict], slack_changes: list[dict]) -> dict[str, dict]:
        """
        Merge changes from Gmail and Slack by vendor.

        Args:
            gmail_changes: Changes detected from Gmail
            slack_changes: Changes detected from Slack

        Returns:
            Dict mapping vendor name to aggregated changes
        """
        merged = {}

        for change in gmail_changes + slack_changes:
            vendor = change.get("vendor")
            if not vendor:
                continue

            if vendor not in merged:
                merged[vendor] = {
                    "vendor": vendor,
                    "sources": [],
                    "status_changes": [],
                    "next_actions": [],
                    "last_contact": None,
                }

            merged[vendor]["sources"].append(change.get("source"))

            if "status_change" in change:
                merged[vendor]["status_changes"].append(change["status_change"])

            if "next_action" in change:
                merged[vendor]["next_actions"].append(change["next_action"])

            if "last_contact" in change and change["last_contact"]:
                if not merged[vendor]["last_contact"] or change["last_contact"] > merged[vendor]["last_contact"]:
                    merged[vendor]["last_contact"] = change["last_contact"]

        return merged


def intelligent_update_slacklist(
    days: int = 7,
    dry_run: bool = False,
    auto_approve: bool = False,
    vendor_filter: Optional[str] = None,
    incremental: bool = True,
) -> dict:
    """
    Intelligently update Slack Lists based on Gmail and Slack message analysis.

    This is the main entry point for the "/auto update slacklist" workflow.

    Args:
        days: Number of days to analyze (ignored if incremental=True and state exists)
        dry_run: If True, show changes without applying
        auto_approve: If True, apply changes without confirmation
        vendor_filter: Filter to specific vendor
        incremental: If True, only process new messages since last sync

    Returns:
        Dict with update results
    """
    import sys
    sys.path.insert(0, str(Path(__file__).parents[2]))

    from lib.gmail import GmailClient
    from lib.slack import SlackClient

    # Load incremental state
    sync_state = IncrementalSyncState()
    stats = sync_state.get_stats()

    print(f"\n{'='*60}")
    print("[SYNC] Intelligent Slack Lists Update")
    print(f"{'='*60}")

    if incremental and stats["last_sync"]:
        print(f"Mode: INCREMENTAL (since {stats['last_sync'][:19]})")
        print(f"  Previously processed: Gmail {stats['gmail_processed']}, Slack {stats['slack_processed']}")
    else:
        print(f"Mode: FULL SCAN ({days} days)")

    if vendor_filter:
        print(f"Vendor Filter: {vendor_filter}")

    results = {
        "analyzed": {"gmail": 0, "slack": 0},
        "changes_detected": [],
        "changes_applied": [],
        "errors": [],
    }

    # Step 1: Collect data
    print("\n[Step 1] Collecting data...")

    # Gmail - search with multiple strategies to find vendor emails
    try:
        gmail_client = GmailClient()
        from datetime import datetime, timedelta
        after_date = (datetime.now() - timedelta(days=days)).strftime("%Y/%m/%d")

        # Strategy 1: Label-based search (if label exists)
        labeled_emails = gmail_client.list_emails(
            query=f"label:wsoptv after:{after_date}",
            max_results=100,
        )

        # Strategy 2: Keyword-based search (catches unlabeled emails)
        keyword_queries = [
            f"(WSOPTV OR WSOP) after:{after_date}",
            f"(from:brightcove OR from:megazone OR from:vimeo) after:{after_date}",
            f"(RFP OR OTT OR 스트리밍) after:{after_date}",
        ]

        keyword_emails = []
        seen_ids = {getattr(e, "id", None) or getattr(e, "message_id", "") for e in labeled_emails}

        for kw_query in keyword_queries:
            try:
                kw_results = gmail_client.list_emails(query=kw_query, max_results=50)
                for email in kw_results:
                    email_id = getattr(email, "id", None) or getattr(email, "message_id", "")
                    if email_id and email_id not in seen_ids:
                        keyword_emails.append(email)
                        seen_ids.add(email_id)
            except Exception:
                pass  # Continue with other queries if one fails

        all_emails = list(labeled_emails) + keyword_emails
        if keyword_emails:
            print(f"  [INFO] Found {len(keyword_emails)} unlabeled emails via keyword search")

        # Filter out already processed emails in incremental mode
        if incremental:
            emails = []
            for email in all_emails:
                email_id = getattr(email, "id", None) or getattr(email, "message_id", "")
                if not sync_state.is_gmail_processed(email_id):
                    emails.append(email)
            print(f"  [OK] Gmail: {len(emails)} new / {len(all_emails)} total")
        else:
            emails = all_emails
            print(f"  [OK] Gmail: {len(emails)} emails")

        results["analyzed"]["gmail"] = len(emails)
    except Exception as e:
        print(f"  [ERR] Gmail: {e}")
        results["errors"].append(f"Gmail: {e}")
        emails = []

    # Slack
    try:
        slack_client = SlackClient()
        all_slack_messages = slack_client.get_history(
            channel=LISTS_CONFIG["channel_id"],
            limit=200,
        )

        # Filter out already processed messages in incremental mode
        if incremental:
            slack_messages = []
            for msg in all_slack_messages:
                msg_ts = getattr(msg, "ts", None) if hasattr(msg, "ts") else msg.get("ts") if isinstance(msg, dict) else None
                if msg_ts and not sync_state.is_slack_processed(msg_ts):
                    slack_messages.append(msg)
            print(f"  [OK] Slack: {len(slack_messages)} new / {len(all_slack_messages)} total")
        else:
            slack_messages = all_slack_messages
            print(f"  [OK] Slack: {len(slack_messages)} messages")

        results["analyzed"]["slack"] = len(slack_messages)
    except Exception as e:
        print(f"  [ERR] Slack: {e}")
        results["errors"].append(f"Slack: {e}")
        slack_messages = []

    # Current Slack Lists
    try:
        manager = ListsSyncManager()
        current_items = manager.get_list_items()
        print(f"  [OK] Slack Lists: {len(current_items)} vendors")
    except Exception as e:
        print(f"  [ERR] Slack Lists: {e}")
        results["errors"].append(f"Slack Lists: {e}")
        current_items = []

    # Step 2: Analyze changes
    print("\n[Step 2] Analyzing changes...")

    detector = VendorChangeDetector()

    # Convert Gmail to expected format (GmailMessage is pydantic model)
    gmail_formatted = []
    for email in emails:
        email_id = getattr(email, "id", None) or getattr(email, "message_id", "")
        gmail_formatted.append({
            "id": email_id,
            "sender": getattr(email, "from_", "") or getattr(email, "sender", ""),
            "subject": getattr(email, "subject", ""),
            "body": getattr(email, "snippet", ""),
            "date": getattr(email, "date", ""),
        })

    gmail_changes = detector.analyze_gmail_messages(gmail_formatted)
    slack_changes = detector.analyze_slack_messages(slack_messages)

    print(f"  Gmail changes: {len(gmail_changes)}")
    print(f"  Slack changes: {len(slack_changes)}")

    # Mark processed (will save later if not dry_run)
    if incremental:
        for email in emails:
            email_id = getattr(email, "id", None) or getattr(email, "message_id", "")
            if email_id:
                sync_state.mark_gmail_processed(email_id)
        for msg in slack_messages:
            msg_ts = getattr(msg, "ts", None) if hasattr(msg, "ts") else msg.get("ts") if isinstance(msg, dict) else None
            if msg_ts:
                sync_state.mark_slack_processed(msg_ts)

    merged = detector.merge_changes(gmail_changes, slack_changes)

    # Apply vendor filter if specified
    if vendor_filter:
        filter_lower = vendor_filter.lower()
        merged = {k: v for k, v in merged.items() if filter_lower in k.lower()}
        print(f"  Filtered to: {len(merged)} vendors")

    if not merged:
        print("\n[OK] No changes detected")
        return results

    # Step 3: Generate updates
    print("\n[Step 3] Generating updates...")

    updates = []
    for vendor_name, changes in merged.items():
        update = {"vendor": vendor_name, "fields": {}}

        # Latest next_action
        if changes["next_actions"]:
            update["fields"]["next_action"] = changes["next_actions"][-1]

        # Latest last_contact
        if changes["last_contact"]:
            update["fields"]["last_contact"] = changes["last_contact"]

        # Status change (if any)
        if changes["status_changes"]:
            latest = changes["status_changes"][-1]
            update["fields"]["status_suggestion"] = latest

        if update["fields"]:
            updates.append(update)
            # Safe print (handle encoding errors)
            try:
                vendor_display = vendor_name.encode('ascii', 'replace').decode()
            except:
                vendor_display = vendor_name
            print(f"  * {vendor_display}:")
            for key, val in update["fields"].items():
                try:
                    val_display = str(val).encode('ascii', 'replace').decode()
                except:
                    val_display = str(val)
                print(f"    - {key}: {val_display}")

    results["changes_detected"] = updates

    if dry_run:
        print("\n[DRY RUN] Changes NOT applied")
        return results

    # Step 4: Apply updates
    if not auto_approve:
        print("\n[SKIP] auto_approve=False - Changes NOT applied (user confirmation needed)")
        return results

    print("\n[Step 4] Applying updates...")

    for update in updates:
        vendor = update["vendor"]
        fields = update["fields"]

        try:
            success = manager.update_item(
                vendor_name=vendor,
                next_action=fields.get("next_action"),
            )
            if success:
                results["changes_applied"].append(update)
                print(f"  [OK] {vendor} updated")
            else:
                print(f"  [FAIL] {vendor} update failed")
        except Exception as e:
            print(f"  [ERR] {vendor}: {e}")
            results["errors"].append(f"{vendor}: {e}")

    # Step 5: Update summary
    print("\n[Step 5] Updating summary message...")
    try:
        updated_items = manager.get_list_items()
        summary = manager.generate_summary_message(updated_items)
        ts = manager.post_summary(summary)
        if ts:
            print(f"  [OK] Pinned message updated (ts: {ts})")
        else:
            print("  [FAIL] Pinned message update failed")
    except Exception as e:
        print(f"  [ERR] Summary update: {e}")
        results["errors"].append(f"Summary: {e}")

    # Save incremental state
    if incremental and not dry_run:
        sync_state.save()
        print("\n[Step 6] State saved to .slacklist_state.json")

    print(f"\n{'='*60}")
    print("[DONE] Complete")
    print(f"  Analyzed: Gmail {results['analyzed']['gmail']}, Slack {results['analyzed']['slack']}")
    print(f"  Detected: {len(results['changes_detected'])} changes")
    print(f"  Applied: {len(results['changes_applied'])} changes")
    if results["errors"]:
        print(f"  Errors: {len(results['errors'])}")
    print(f"{'='*60}\n")

    return results


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Sync Slack Lists")
    parser.add_argument(
        "--dashboard",
        type=Path,
        default=Path("C:/claude/wsoptv_ott/docs/management/VENDOR-DASHBOARD.md"),
        help="Path to VENDOR-DASHBOARD.md",
    )
    parser.add_argument(
        "--post-summary",
        action="store_true",
        help="Post summary to Slack channel",
    )
    parser.add_argument(
        "--intelligent-update",
        action="store_true",
        help="Intelligently update from Gmail and Slack analysis",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days to analyze",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Auto-approve changes without confirmation",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "--vendor",
        type=str,
        default=None,
        help="Filter to specific vendor (e.g., 'megazone', 'brightcove')",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Full scan mode (disable incremental, re-process all)",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show sync state status",
    )

    args = parser.parse_args()

    if args.status:
        state = IncrementalSyncState()
        stats = state.get_stats()
        print("\n[SYNC STATE]")
        print(f"  Last sync: {stats['last_sync'] or 'Never'}")
        print(f"  Gmail processed: {stats['gmail_processed']}")
        print(f"  Slack processed: {stats['slack_processed']}")
        print(f"  Vendors tracked: {stats['vendors_tracked']}")
        print(f"  Pending changes: {stats['pending_changes']}")
    elif args.intelligent_update:
        intelligent_update_slacklist(
            days=args.days,
            dry_run=args.dry_run,
            auto_approve=args.yes,
            vendor_filter=args.vendor,
            incremental=not args.full,
        )
    elif args.post_summary:
        post_daily_summary(dry_run=args.dry_run)
    else:
        result = sync_lists_to_dashboard(
            dashboard_path=args.dashboard,
            dry_run=args.dry_run,
        )
        print(f"\n{result}")


if __name__ == "__main__":
    main()
