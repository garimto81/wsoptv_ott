"""Thread analyzer for detecting bidirectional communication patterns."""

import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# Add root for lib imports
sys.path.insert(0, str(Path(__file__).parents[4]))

from lib.gmail import GmailClient

# Import models from parent
sys.path.insert(0, str(Path(__file__).parents[1]))
from models_v2 import EmailThread, CommunicationDirection
from config_models import ProjectConfig


class ThreadAnalyzer:
    """Analyze email threads to detect negotiation patterns."""

    def __init__(self, gmail_client: Optional[GmailClient] = None, config: Optional[ProjectConfig] = None):
        """Initialize with Gmail client and project config."""
        self.gmail_client = gmail_client or GmailClient()
        self.config = config
        self._user_email = None

    @property
    def user_email(self) -> str:
        """Get current user's email address."""
        if self._user_email is None:
            profile = self.gmail_client.get_profile()
            self._user_email = profile.get("emailAddress", "").lower()
        return self._user_email

    def analyze(self, thread_id: str) -> EmailThread:
        """
        Analyze a single thread.

        Args:
            thread_id: Gmail thread ID

        Returns:
            EmailThread with analysis results
        """
        thread = self.gmail_client.get_thread(thread_id)

        inbound = 0
        outbound = 0
        first_date = None
        last_date = None
        last_direction = None
        vendor_name = ""
        response_times = []
        prev_date = None
        prev_direction = None

        for msg in thread.messages:
            sender_lower = msg.sender.lower()
            is_from_user = self.user_email in sender_lower

            if is_from_user:
                outbound += 1
                direction = CommunicationDirection.OUTBOUND
            else:
                inbound += 1
                direction = CommunicationDirection.INBOUND

                # Detect vendor from sender
                if self.config and not vendor_name:
                    vendor = self.config.get_vendor_by_domain(msg.sender)
                    if vendor:
                        vendor_name = vendor.name

            # Track dates
            if msg.date:
                if first_date is None or msg.date < first_date:
                    first_date = msg.date
                if last_date is None or msg.date > last_date:
                    last_date = msg.date
                    last_direction = direction

                # Calculate response time (if direction changed)
                if prev_date and prev_direction and prev_direction != direction:
                    delta = (msg.date - prev_date).total_seconds() / 3600  # hours
                    if delta > 0:
                        response_times.append(delta)

                prev_date = msg.date
                prev_direction = direction

        # Calculate average response time
        avg_response = None
        if response_times:
            avg_response = sum(response_times) / len(response_times)

        return EmailThread(
            thread_id=thread_id,
            vendor=vendor_name,
            message_count=len(thread.messages),
            inbound_count=inbound,
            outbound_count=outbound,
            first_date=first_date,
            last_date=last_date,
            last_direction=last_direction,
            avg_response_time_hours=avg_response,
        )

    def analyze_vendor_threads(self, vendor_domain: str, days: int = 30) -> List[EmailThread]:
        """
        Analyze all threads with a specific vendor.

        Args:
            vendor_domain: Domain to filter (e.g., "megazone.com")
            days: Number of days to look back

        Returns:
            List of analyzed EmailThread objects
        """
        from datetime import timedelta

        cutoff = datetime.now() - timedelta(days=days)
        query = f"from:{vendor_domain} OR to:{vendor_domain} after:{cutoff.strftime('%Y/%m/%d')}"

        messages = self.gmail_client.list_emails(query=query, max_results=100)

        # Group by thread_id
        thread_ids = set()
        for msg in messages:
            thread_ids.add(msg.thread_id)

        threads = []
        for tid in thread_ids:
            try:
                thread = self.analyze(tid)
                threads.append(thread)
            except Exception as e:
                print(f"Error analyzing thread {tid}: {e}")

        return threads

    def detect_active_negotiations(self, threads: List[EmailThread]) -> List[EmailThread]:
        """
        Filter threads that have bidirectional communication.

        Args:
            threads: List of analyzed threads

        Returns:
            List of threads with active negotiation (both inbound and outbound)
        """
        return [t for t in threads if t.is_active_negotiation]

    def has_active_negotiation(self, threads: List[EmailThread]) -> bool:
        """Check if any thread has bidirectional communication."""
        return any(t.is_active_negotiation for t in threads)
