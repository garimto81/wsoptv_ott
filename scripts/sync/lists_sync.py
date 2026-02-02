"""
Slack Lists synchronization script.

Syncs Slack Kanban board (Lists) with local VENDOR-DASHBOARD.md and SLACK-LOG.md.
Also updates pinned messages in the project channel.
"""

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
                    "select_option_id": option_id,
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
                "date": last_contact.strftime("%Y-%m-%d"),
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
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )

    args = parser.parse_args()

    if args.post_summary:
        post_daily_summary(dry_run=args.dry_run)
    else:
        result = sync_lists_to_dashboard(
            dashboard_path=args.dashboard,
            dry_run=args.dry_run,
        )
        print(f"\n{result}")


if __name__ == "__main__":
    main()
