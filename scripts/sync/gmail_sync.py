"""
Gmail to EMAIL-LOG.md synchronization script.

Fetches Gmail messages with wsoptv label and syncs to EMAIL-LOG.md format with:
- Chronological message grouping by date
- Company detection from email addresses
- Duplicate prevention using email_id
- Direction detection (sent/received)
"""

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Add C:\claude to path for lib.gmail import
_script_dir = Path(__file__).resolve().parent
_wsoptv_root = _script_dir.parents[1]
_claude_root = _script_dir.parents[2]
sys.path.insert(0, str(_claude_root))

from lib.gmail import GmailClient, GmailMessage  # noqa: E402

# Import models from same directory
try:
    from .models import SyncResult, EmailDirection
except ImportError:
    from models import SyncResult, EmailDirection


# Company detection patterns
COMPANY_PATTERNS = {
    "brightcove": {
        "name": "Brightcove",
        "domains": ["brightcove.com"],
    },
    "megazone": {
        "name": "메가존클라우드",
        "domains": ["megazone.com", "megazonecloud.com"],
    },
    "vimeo": {
        "name": "Vimeo",
        "domains": ["vimeo.com"],
    },
    "malgum": {
        "name": "맑음소프트",
        "domains": ["malgum.com", "malgumsoft.com"],
    },
}


class CompanyDetector:
    """Detect company from email address."""

    @staticmethod
    def detect(email: str) -> Optional[str]:
        """
        Detect company name from email address.

        Args:
            email: Email address string (may contain name like "Name <email@domain.com>")

        Returns:
            Company name if detected, None otherwise
        """
        # Extract email from "Name <email>" format
        match = re.search(r"<([^>]+)>", email)
        if match:
            email = match.group(1)

        email = email.lower()

        for key, info in COMPANY_PATTERNS.items():
            for domain in info["domains"]:
                if domain in email:
                    return info["name"]

        return None


class MarkdownParser:
    """Parse existing EMAIL-LOG.md to extract existing entries."""

    @staticmethod
    def extract_existing_ids(log_content: str) -> set[str]:
        """Extract all existing email_id values from log."""
        id_set = set()
        # Pattern: <!-- email_id: abc123xyz -->
        for match in re.finditer(r"<!-- email_id: ([a-zA-Z0-9_-]+) -->", log_content):
            id_set.add(match.group(1))
        return id_set

    @staticmethod
    def find_date_section_position(log_content: str, date: datetime) -> tuple[int, bool]:
        """
        Find position to insert new date section.

        Returns:
            (position, date_exists): Position to insert and whether date section exists
        """
        date_str = date.strftime("%Y-%m-%d")
        weekday = ["월", "화", "수", "목", "금", "토", "일"][date.weekday()]
        date_header = f"### {date_str} ({weekday})"

        # Check if date section exists
        date_exists = date_header in log_content

        # Find "## 메일 로그" section
        log_section_match = re.search(r"## 메일 로그", log_content)
        if not log_section_match:
            return -1, False

        log_section_pos = log_section_match.end()

        # Find all date headers after log section
        date_pattern = r"### (\d{4}-\d{2}-\d{2})"
        matches = list(re.finditer(date_pattern, log_content[log_section_pos:]))

        if date_exists:
            # Find the exact position of the date header
            for match in matches:
                if match.group(1) == date_str:
                    # Find next section after this date
                    abs_pos = log_section_pos + match.end()
                    next_section = re.search(r"\n### \d{4}-\d{2}-\d{2}|\n## ", log_content[abs_pos:])
                    if next_section:
                        return abs_pos + next_section.start(), True
                    return len(log_content), True
            return -1, True

        # Find position for new date (after newer dates)
        for match in matches:
            if match.group(1) < date_str:
                return log_section_pos + match.start(), False

        # If no date found or all dates are newer, insert after log section header
        next_line = log_content.find("\n", log_section_pos)
        if next_line != -1:
            return next_line + 1, False

        return len(log_content), False


class EmailLogFormatter:
    """Format Gmail messages to EMAIL-LOG.md format."""

    def __init__(self, user_email: str):
        self.user_email = user_email.lower()

    def _detect_direction(self, msg: GmailMessage) -> EmailDirection:
        """Detect if email was sent or received."""
        sender_email = msg.sender.lower()

        # Check if sender matches user email
        if self.user_email in sender_email:
            return EmailDirection.SENT

        # Check if any recipient is user email
        for recipient in msg.to:
            if self.user_email in recipient.lower():
                return EmailDirection.RECEIVED

        # Default: if in SENT label, it was sent
        if "SENT" in msg.labels:
            return EmailDirection.SENT

        return EmailDirection.RECEIVED

    def format_message(self, msg: GmailMessage) -> str:
        """Format single message to markdown."""
        lines = []

        direction = self._detect_direction(msg)
        company = CompanyDetector.detect(msg.sender if direction == EmailDirection.RECEIVED else msg.to[0] if msg.to else "")
        company_str = company or "Unknown"

        # Direction header
        direction_str = "RECEIVED" if direction == EmailDirection.RECEIVED else "SENT"
        lines.append(f"#### [{direction_str}] {company_str}")
        lines.append("")

        # email_id comment for duplicate detection
        lines.append(f"<!-- email_id: {msg.id} -->")

        # Email details
        if direction == EmailDirection.RECEIVED:
            lines.append(f"**발신자**: {msg.sender}")
            lines.append(f"**수신자**: {', '.join(msg.to)}")
        else:
            lines.append(f"**수신자**: {', '.join(msg.to)}")
            lines.append(f"**발신자**: {msg.sender}")

        lines.append(f"**제목**: {msg.subject}")
        lines.append("")

        # Summary from snippet
        lines.append("**요약**:")
        snippet = msg.snippet[:200] + "..." if len(msg.snippet) > 200 else msg.snippet
        lines.append(f"- {snippet}")
        lines.append("")

        # Status placeholder
        lines.append("**상태**: 대기 중")
        lines.append("**후속조치**: (확인 필요)")
        lines.append("")
        lines.append("---")
        lines.append("")

        return "\n".join(lines)

    def format_date_section(self, date: datetime, messages: list[str]) -> str:
        """Format all messages for a specific date."""
        weekday = ["월", "화", "수", "목", "금", "토", "일"][date.weekday()]
        lines = []
        lines.append(f"### {date.strftime('%Y-%m-%d')} ({weekday})")
        lines.append("")

        for msg_content in messages:
            lines.append(msg_content)

        return "\n".join(lines)


def sync_gmail_to_log(
    log_path: Path,
    query: str = "label:wsoptv",
    days: int = 7,
    dry_run: bool = False,
) -> SyncResult:
    """
    Sync Gmail to EMAIL-LOG.md.

    Args:
        log_path: Path to EMAIL-LOG.md
        query: Gmail search query
        days: Number of days to fetch
        dry_run: If True, only show what would be added

    Returns:
        SyncResult with counts
    """
    result = SyncResult()

    # Initialize client
    client = GmailClient()
    profile = client.get_profile()
    user_email = profile.get("emailAddress", "")

    formatter = EmailLogFormatter(user_email)

    # Build date-based query
    cutoff_date = datetime.now() - timedelta(days=days)
    date_query = cutoff_date.strftime("after:%Y/%m/%d")
    full_query = f"{query} {date_query}"

    print(f"Fetching emails with query: {full_query}")
    messages = client.list_emails(query=full_query, max_results=100)

    print(f"Found {len(messages)} messages")

    # Read existing log
    if log_path.exists():
        log_content = log_path.read_text(encoding="utf-8")
        existing_ids = MarkdownParser.extract_existing_ids(log_content)
    else:
        log_content = _create_initial_log()
        existing_ids = set()

    print(f"Existing entries: {len(existing_ids)}")

    # Group messages by date
    messages_by_date: dict[str, list[str]] = {}

    for msg in messages:
        # Skip existing
        if msg.id in existing_ids:
            result.skipped += 1
            continue

        if not msg.date:
            result.errors += 1
            continue

        date_key = msg.date.strftime("%Y-%m-%d")
        formatted = formatter.format_message(msg)

        if date_key not in messages_by_date:
            messages_by_date[date_key] = []

        messages_by_date[date_key].append(formatted)
        result.added += 1

    if dry_run:
        print("\n=== DRY RUN ===")
        for date_str, msgs in sorted(messages_by_date.items(), reverse=True):
            date = datetime.strptime(date_str, "%Y-%m-%d")
            content = formatter.format_date_section(date, msgs)
            print(f"\n{content}")
        return result

    # Insert new entries into log
    for date_str, msgs in sorted(messages_by_date.items(), reverse=True):
        date = datetime.strptime(date_str, "%Y-%m-%d")
        insert_pos, date_exists = MarkdownParser.find_date_section_position(log_content, date)

        if insert_pos == -1:
            print(f"WARNING: Could not find insert position for {date_str}")
            continue

        if date_exists:
            # Insert just messages after date header
            messages_content = "\n".join(msgs)
            log_content = (
                log_content[:insert_pos] + "\n" + messages_content + log_content[insert_pos:]
            )
        else:
            # Insert full date section
            content = formatter.format_date_section(date, msgs)
            log_content = log_content[:insert_pos] + "\n" + content + "\n" + log_content[insert_pos:]

    # Write back
    log_path.write_text(log_content, encoding="utf-8")
    print(f"\nSynced to {log_path}")

    return result


def _create_initial_log() -> str:
    """Create initial EMAIL-LOG.md structure."""
    return f"""# EMAIL-LOG

**Version**: 1.0.0
**Last Updated**: {datetime.now().strftime("%Y-%m-%d")}

WSOPTV OTT 프로젝트 이메일 커뮤니케이션 로그 및 대기 현황 관리

---

## 요약 대시보드

| 업체 | 미회신 | 대기 중 | 완료 | 최종 연락일 |
|------|--------|---------|------|-------------|
| **합계** | **0** | **0** | **0** | - |

---

## Action Required (미회신 알림)

(미회신 메일이 여기에 표시됩니다)

---

## 메일 로그

"""


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Sync Gmail to EMAIL-LOG.md")
    parser.add_argument(
        "--log",
        type=Path,
        default=Path("C:/claude/wsoptv_ott/docs/management/EMAIL-LOG.md"),
        help="Path to EMAIL-LOG.md",
    )
    parser.add_argument(
        "--query",
        default="label:wsoptv",
        help="Gmail search query",
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

    result = sync_gmail_to_log(
        log_path=args.log,
        query=args.query,
        days=args.days,
        dry_run=args.dry_run,
    )

    print(f"\n{result}")


if __name__ == "__main__":
    main()
