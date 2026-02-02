"""
Slack to SLACK-LOG.md synchronization script.

Fetches Slack channel history and syncs to SLACK-LOG.md format with:
- Chronological message grouping by date
- Pattern detection for decisions/action items
- Duplicate prevention using ts (timestamp)
- User name resolution
"""

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Add C:\claude to path for lib.slack import
_script_dir = Path(__file__).resolve().parent
_wsoptv_root = _script_dir.parents[1]
_claude_root = _script_dir.parents[2]
sys.path.insert(0, str(_claude_root))

from lib.slack import SlackClient, SlackMessage, SlackUser  # noqa: E402

# Import models from same directory
try:
    from .models import SyncResult
except ImportError:
    from models import SyncResult


class PatternDetector:
    """Detect decisions and action items in Slack messages."""

    # Decision keywords
    DECISION_PATTERNS = [
        r"결정",
        r"확정",
        r"동의합니다",
        r"합의",
        r"이렇게.*진행",
        r"승인",
        r"채택",
    ]

    # Action item patterns
    ACTION_PATTERNS = [
        r"@(\w+).*(\d{4}-\d{2}-\d{2})",  # @user ... date
        r"담당.*:.*@(\w+)",
        r"@(\w+).*검토",
        r"@(\w+).*확인",
        r"@(\w+).*업데이트",
    ]

    # Follow-up patterns
    FOLLOWUP_PATTERNS = [
        r"후속.*:",
        r"액션.*:",
        r"다음.*단계",
    ]

    @classmethod
    def is_decision(cls, text: str) -> bool:
        """Check if message contains decision."""
        return any(re.search(pattern, text) for pattern in cls.DECISION_PATTERNS)

    @classmethod
    def is_action_item(cls, text: str) -> bool:
        """Check if message contains action item."""
        return any(re.search(pattern, text) for pattern in cls.ACTION_PATTERNS)

    @classmethod
    def extract_assignee(cls, text: str) -> Optional[str]:
        """Extract assignee from action item."""
        for pattern in cls.ACTION_PATTERNS:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None

    @classmethod
    def extract_deadline(cls, text: str) -> Optional[datetime]:
        """Extract deadline from text."""
        match = re.search(r"(\d{4}-\d{2}-\d{2})", text)
        if match:
            try:
                return datetime.strptime(match.group(1), "%Y-%m-%d")
            except ValueError:
                pass
        return None


class MarkdownParser:
    """Parse existing SLACK-LOG.md to extract existing entries."""

    @staticmethod
    def extract_existing_ts(log_content: str) -> set[str]:
        """Extract all existing ts values from log."""
        ts_set = set()
        # Pattern: <!-- ts: 1706824200.123456 -->
        for match in re.finditer(r"<!-- ts: ([\d.]+) -->", log_content):
            ts_set.add(match.group(1))
        return ts_set

    @staticmethod
    def find_insert_position(log_content: str, date: datetime) -> int:
        """Find position to insert new date section."""
        # Find all date headers (### YYYY-MM-DD)
        date_pattern = r"### (\d{4}-\d{2}-\d{2})"
        matches = list(re.finditer(date_pattern, log_content))

        target_date_str = date.strftime("%Y-%m-%d")

        # Find position after "## 슬랙 로그 (최신순)"
        log_section_match = re.search(r"## 슬랙 로그 \(최신순\)", log_content)
        if not log_section_match:
            return -1

        log_section_pos = log_section_match.end()

        # Check if date already exists
        for match in matches:
            if match.group(1) == target_date_str:
                return match.start()

        # Find first date section AFTER target date (newer date)
        for match in matches:
            if match.group(1) > target_date_str and match.start() > log_section_pos:
                return match.start()

        # If no newer date found, insert after log section header
        if matches and matches[0].start() > log_section_pos:
            return matches[0].start()

        # Insert at end of log section (before next ## section)
        next_section = re.search(r"\n## ", log_content[log_section_pos:])
        if next_section:
            return log_section_pos + next_section.start()

        return len(log_content)


class SlackLogFormatter:
    """Format Slack messages to SLACK-LOG.md format."""

    def __init__(self, client: SlackClient):
        self.client = client
        self._user_cache: dict[str, SlackUser] = {}

    def _get_user_name(self, user_id: str) -> str:
        """Get user display name with caching."""
        if user_id not in self._user_cache:
            try:
                user = self.client.get_user(user_id)
                self._user_cache[user_id] = user
            except Exception:
                return user_id

        user = self._user_cache[user_id]
        return user.display_name or user.name or user_id

    def format_message(
        self,
        msg: SlackMessage,
        channel_name: str,
        is_decision: bool = False,
        is_action: bool = False,
    ) -> str:
        """Format single message to markdown."""
        lines = []

        # Time and channel header
        time_str = msg.timestamp.strftime("%H:%M") if msg.timestamp else "??:??"
        lines.append(f"#### {time_str} - #{channel_name}")

        # ts comment for duplicate detection
        lines.append(f"<!-- ts: {msg.ts} -->")

        # Message content
        user_name = self._get_user_name(msg.user) if msg.user else "Unknown"
        lines.append(f"> @{user_name}: {msg.text}")

        # Add tags if decision or action item
        if is_decision:
            lines.append("")
            lines.append("**결정**: ✅ (요약 필요)")
        elif is_action:
            lines.append("")
            lines.append("**상태**: 🟡 추가 확인 필요")

        lines.append("")
        return "\n".join(lines)

    def format_date_section(self, date: datetime, messages: list[dict]) -> str:
        """Format all messages for a specific date."""
        lines = []
        lines.append(f"### {date.strftime('%Y-%m-%d')}")
        lines.append("")

        for msg_data in messages:
            lines.append(
                self.format_message(
                    msg_data["msg"],
                    msg_data["channel_name"],
                    msg_data["is_decision"],
                    msg_data["is_action"],
                )
            )

        return "\n".join(lines)


def sync_slack_to_log(
    log_path: Path,
    channel_id: str = "C09TX3M1J2W",
    days: int = 7,
    dry_run: bool = False,
) -> SyncResult:
    """
    Sync Slack channel to SLACK-LOG.md.

    Args:
        log_path: Path to SLACK-LOG.md
        channel_id: Slack channel ID
        days: Number of days to fetch
        dry_run: If True, only show what would be added

    Returns:
        SyncResult with counts
    """
    result = SyncResult()

    # Initialize client
    client = SlackClient()
    formatter = SlackLogFormatter(client)

    # Get channel name
    channels = client.list_channels(include_private=True)
    channel_name = next(
        (ch.name for ch in channels if ch.id == channel_id),
        channel_id,
    )

    # Fetch messages
    print(f"Fetching messages from #{channel_name} (last {days} days)...")
    messages = client.get_history(channel_id, limit=1000)

    # Filter by date range
    cutoff_date = datetime.now() - timedelta(days=days)
    messages = [msg for msg in messages if msg.timestamp and msg.timestamp >= cutoff_date]

    print(f"Found {len(messages)} messages")

    # Read existing log
    if log_path.exists():
        log_content = log_path.read_text(encoding="utf-8")
        existing_ts = MarkdownParser.extract_existing_ts(log_content)
    else:
        log_content = _create_initial_log()
        existing_ts = set()

    print(f"Existing entries: {len(existing_ts)}")

    # Group messages by date
    messages_by_date: dict[str, list[dict]] = {}

    for msg in messages:
        # Skip existing
        if msg.ts in existing_ts:
            result.skipped += 1
            continue

        # Detect patterns
        is_decision = PatternDetector.is_decision(msg.text)
        is_action = PatternDetector.is_action_item(msg.text)

        if not msg.timestamp:
            result.errors += 1
            continue

        date_key = msg.timestamp.strftime("%Y-%m-%d")

        if date_key not in messages_by_date:
            messages_by_date[date_key] = []

        messages_by_date[date_key].append(
            {
                "msg": msg,
                "channel_name": channel_name,
                "is_decision": is_decision,
                "is_action": is_action,
            }
        )

    # Format new entries
    new_entries: list[tuple[datetime, str]] = []

    for date_str, msgs in sorted(messages_by_date.items(), reverse=True):
        date = datetime.strptime(date_str, "%Y-%m-%d")
        formatted = formatter.format_date_section(date, msgs)
        new_entries.append((date, formatted))
        result.added += len(msgs)

    if dry_run:
        print("\n=== DRY RUN ===")
        for date, content in new_entries:
            print(f"\n{content}")
        return result

    # Insert new entries
    for date, content in new_entries:
        insert_pos = MarkdownParser.find_insert_position(log_content, date)

        if insert_pos == -1:
            print(f"WARNING: Could not find insert position for {date}")
            continue

        # Check if date section exists
        date_str = date.strftime("%Y-%m-%d")
        date_section_exists = f"### {date_str}" in log_content

        if date_section_exists:
            # Find position after date header
            date_header_pos = log_content.find(f"### {date_str}")
            # Find next date header or section
            next_section = re.search(
                r"\n(###|\##) ",
                log_content[date_header_pos + 10 :],
            )
            if next_section:
                insert_pos = date_header_pos + 10 + next_section.start()
            else:
                insert_pos = len(log_content)

            # Insert just messages (skip date header)
            message_content = "\n".join(content.split("\n")[2:])  # Skip "### YYYY-MM-DD" and empty line
            log_content = (
                log_content[:insert_pos] + "\n" + message_content + log_content[insert_pos:]
            )
        else:
            # Insert full date section
            log_content = log_content[:insert_pos] + content + "\n\n" + log_content[insert_pos:]

    # Write back
    log_path.write_text(log_content, encoding="utf-8")
    print(f"\n✅ Synced to {log_path}")

    return result


def _create_initial_log() -> str:
    """Create initial SLACK-LOG.md structure."""
    return """# WSOPTV 슬랙 관리 로그

**최종 업데이트**: {now}

---

## 요약 대시보드

| 구분 | 미완료 | 진행 중 | 완료 |
|------|:------:|:------:|:----:|
| 의사결정 | 0 | 0 | 0 |
| 액션 아이템 | 0 | 0 | 0 |

---

## 미완료 액션 아이템

(자동 감지된 액션 아이템이 여기에 표시됩니다)

---

## 최근 의사결정

(자동 감지된 의사결정이 여기에 표시됩니다)

---

## 슬랙 로그 (최신순)

""".format(now=datetime.now().strftime("%Y-%m-%d %H:%M"))


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Sync Slack to SLACK-LOG.md")
    parser.add_argument(
        "--log",
        type=Path,
        default=Path("C:/claude/wsoptv_ott/docs/management/SLACK-LOG.md"),
        help="Path to SLACK-LOG.md",
    )
    parser.add_argument(
        "--channel",
        default="C09TX3M1J2W",
        help="Slack channel ID",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days to sync",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be synced without writing",
    )

    args = parser.parse_args()

    result = sync_slack_to_log(
        log_path=args.log,
        channel_id=args.channel,
        days=args.days,
        dry_run=args.dry_run,
    )

    print(f"\n{result}")


if __name__ == "__main__":
    main()
