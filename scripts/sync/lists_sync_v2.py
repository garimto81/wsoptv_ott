"""
Slack Lists Sync v2.0 - Unified 4-Layer Pipeline

Integrates all Phase 1-3 modules into a unified workflow:
- Layer 1 (Source): Gmail collection via GmailClient
- Layer 2 (Analyzer): ThreadAnalyzer, AttachmentParser, QuoteExtractor
- Layer 3 (Processor): StatusInferencer, QuoteAggregator
- Layer 4 (Output): SlackListsWriter

Usage:
    python lists_sync_v2.py sync --days 7 --dry-run
    python lists_sync_v2.py sync --full --vendor megazone
    python lists_sync_v2.py status
    python lists_sync_v2.py analyze-attachments --vendor brightcove
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, TextColumn, BarColumn
from rich.table import Table

# Fix Windows console encoding for rich spinners
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

# Add paths for imports
_script_dir = Path(__file__).resolve().parent
_wsoptv_root = _script_dir.parents[1]
_claude_root = _script_dir.parents[2]
sys.path.insert(0, str(_claude_root))
sys.path.insert(0, str(_script_dir))

# Core imports
from lib.gmail import GmailClient
from lib.slack import SlackClient

# Handle imports for both direct run and module run
try:
    # When run as module
    from .config_models import ProjectConfig
    from .models_v2 import (
        VendorState,
        VendorStatus,
        EmailThread,
        VendorQuote,
        QuoteOption,
        Attachment,
        StatusTransition,
    )
    from .analyzers.thread_analyzer import ThreadAnalyzer
    from .analyzers.status_inferencer import StatusInferencer
    from .collectors.attachment_downloader import AttachmentDownloader
    from .parsers.pdf_parser import PDFParser, get_pdf_parser
    from .parsers.excel_parser import ExcelParser, get_excel_parser
    from .extractors.quote_extractor import QuoteExtractor, get_quote_extractor
    from .lists_sync import ListsSyncManager, LISTS_CONFIG
except ImportError:
    # When run directly
    from config_models import ProjectConfig
    from models_v2 import (
        VendorState,
        VendorStatus,
        EmailThread,
        VendorQuote,
        QuoteOption,
        Attachment,
        StatusTransition,
    )
    from analyzers.thread_analyzer import ThreadAnalyzer
    from analyzers.status_inferencer import StatusInferencer
    from collectors.attachment_downloader import AttachmentDownloader
    from parsers.pdf_parser import PDFParser, get_pdf_parser
    from parsers.excel_parser import ExcelParser, get_excel_parser
    from extractors.quote_extractor import QuoteExtractor, get_quote_extractor
    from lists_sync import ListsSyncManager, LISTS_CONFIG

# CLI app
app = typer.Typer(help="Slack Lists Sync v2 - 4-Layer Pipeline")
console = Console()


# =============================================================================
# State Management
# =============================================================================

class SyncStateV2:
    """State management for v2 sync operations."""

    def __init__(self, state_file: Path):
        """Initialize with state file path."""
        self.state_file = state_file
        self.state = self._load()

    def _load(self) -> dict:
        """Load state from file."""
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return self._default_state()

    def _default_state(self) -> dict:
        """Return default state structure."""
        return {
            "version": "2.0",
            "last_sync": None,
            "processed_emails": [],
            "processed_threads": [],
            "vendor_states": {},
            "quotes": {},
            "pending_transitions": [],
        }

    def save(self):
        """Save state to file."""
        self.state["last_sync"] = datetime.now().isoformat()
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(
            json.dumps(self.state, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )

    def is_email_processed(self, email_id: str) -> bool:
        """Check if email was already processed."""
        return email_id in self.state["processed_emails"]

    def mark_email_processed(self, email_id: str):
        """Mark email as processed."""
        if email_id not in self.state["processed_emails"]:
            self.state["processed_emails"].append(email_id)
            # Keep only last 1000
            if len(self.state["processed_emails"]) > 1000:
                self.state["processed_emails"] = self.state["processed_emails"][-1000:]

    def is_thread_processed(self, thread_id: str) -> bool:
        """Check if thread was already processed."""
        return thread_id in self.state["processed_threads"]

    def mark_thread_processed(self, thread_id: str):
        """Mark thread as processed."""
        if thread_id not in self.state["processed_threads"]:
            self.state["processed_threads"].append(thread_id)
            if len(self.state["processed_threads"]) > 500:
                self.state["processed_threads"] = self.state["processed_threads"][-500:]

    def get_vendor_state(self, vendor_name: str) -> Optional[dict]:
        """Get stored vendor state."""
        return self.state["vendor_states"].get(vendor_name)

    def update_vendor_state(self, vendor_name: str, data: dict):
        """Update vendor state."""
        if vendor_name not in self.state["vendor_states"]:
            self.state["vendor_states"][vendor_name] = {}
        self.state["vendor_states"][vendor_name].update(data)
        self.state["vendor_states"][vendor_name]["updated_at"] = datetime.now().isoformat()

    def add_quote(self, vendor_name: str, quote_data: dict):
        """Add or update vendor quote."""
        self.state["quotes"][vendor_name] = quote_data

    def get_quote(self, vendor_name: str) -> Optional[dict]:
        """Get vendor quote."""
        return self.state["quotes"].get(vendor_name)

    def add_pending_transition(self, transition: dict):
        """Add pending status transition for review."""
        transition["detected_at"] = datetime.now().isoformat()
        self.state["pending_transitions"].append(transition)

    def get_pending_transitions(self) -> List[dict]:
        """Get all pending transitions."""
        return self.state["pending_transitions"]

    def clear_pending_transitions(self):
        """Clear pending transitions after applying."""
        self.state["pending_transitions"] = []

    def get_stats(self) -> dict:
        """Get sync statistics."""
        return {
            "last_sync": self.state.get("last_sync"),
            "processed_emails": len(self.state.get("processed_emails", [])),
            "processed_threads": len(self.state.get("processed_threads", [])),
            "vendors_tracked": len(self.state.get("vendor_states", {})),
            "quotes_stored": len(self.state.get("quotes", {})),
            "pending_transitions": len(self.state.get("pending_transitions", [])),
        }


# =============================================================================
# Quote Aggregator (Layer 3)
# =============================================================================

class QuoteAggregator:
    """Aggregate quotes from multiple sources."""

    def __init__(self, config: ProjectConfig):
        """Initialize with config."""
        self.config = config
        self.pdf_parser = get_pdf_parser()
        self.excel_parser = get_excel_parser()
        self.quote_extractor = get_quote_extractor()

    def aggregate_from_attachments(
        self,
        attachments: List[Attachment],
        vendor_name: str,
    ) -> VendorQuote:
        """
        Aggregate quote data from attachments.

        Args:
            attachments: List of downloaded attachments
            vendor_name: Vendor name for the quote

        Returns:
            VendorQuote with all extracted options
        """
        all_options: List[QuoteOption] = []

        for att in attachments:
            if not att.local_path or not Path(att.local_path).exists():
                continue

            try:
                options = self._extract_from_attachment(att)
                all_options.extend(options)
            except Exception as e:
                console.print(f"[yellow]Warning: Failed to parse {att.filename}: {e}[/yellow]")

        # Deduplicate by amount
        unique_options = self._deduplicate_options(all_options)

        return VendorQuote(
            vendor=vendor_name,
            options=unique_options,
            received_date=datetime.now() if unique_options else None,
        )

    def _extract_from_attachment(self, att: Attachment) -> List[QuoteOption]:
        """Extract quotes from a single attachment."""
        path = Path(att.local_path)
        options = []

        if att.file_type == "pdf":
            # Extract from PDF
            pdf_data = self.pdf_parser.extract_all(path)

            # Try tables first (more structured)
            for table in pdf_data.get("tables", []):
                table_opts = self.quote_extractor.extract_from_table(table)
                for opt in table_opts:
                    opt.source_file = att.filename
                options.extend(table_opts)

            # Fallback to text
            if not options:
                text_opts = self.quote_extractor.extract_from_text(pdf_data.get("text", ""))
                for opt in text_opts:
                    opt.source_file = att.filename
                options.extend(text_opts)

        elif att.file_type == "excel":
            # Extract from Excel
            sheets = self.excel_parser.parse(path)
            excel_opts = self.quote_extractor.extract_from_excel(sheets)
            for opt in excel_opts:
                opt.source_file = att.filename
            options.extend(excel_opts)

        # Update attachment parse status
        att.parsed = True
        att.parse_result = {"options_found": len(options)}

        return options

    def _deduplicate_options(self, options: List[QuoteOption]) -> List[QuoteOption]:
        """Remove duplicate options by amount."""
        seen = set()
        unique = []

        for opt in options:
            key = (opt.total_amount, opt.option_name)
            if key not in seen:
                seen.add(key)
                unique.append(opt)

        return unique


# =============================================================================
# Slack Lists Writer (Layer 4)
# =============================================================================

class SlackListsWriter:
    """Write vendor states to Slack Lists."""

    def __init__(self, config: ProjectConfig):
        """Initialize with config."""
        self.config = config
        self.manager = ListsSyncManager()

    def update_vendor(
        self,
        vendor_state: VendorState,
        dry_run: bool = False,
    ) -> bool:
        """
        Update vendor in Slack Lists.

        Args:
            vendor_state: Vendor state to write
            dry_run: If True, only preview changes

        Returns:
            True if successful (or dry_run)
        """
        vendor_name = vendor_state.vendor_name

        # Map status to Slack option
        status_text = self._map_status(vendor_state.status)

        # Format quote
        quote_text = vendor_state.quote_summary

        # Format last contact
        last_contact = vendor_state.last_contact

        # Format next action
        next_action = vendor_state.next_action

        if dry_run:
            console.print(f"[dim]Would update {vendor_name}:[/dim]")
            console.print(f"  Status: {status_text}")
            console.print(f"  Quote: {quote_text}")
            if last_contact:
                console.print(f"  Last Contact: {last_contact.strftime('%Y-%m-%d')}")
            if next_action:
                console.print(f"  Next Action: {next_action}")
            return True

        try:
            success = self.manager.update_item(
                vendor_name=vendor_name,
                status=status_text,
                quote=quote_text if quote_text != "미수령" else None,
                last_contact=last_contact,
                next_action=next_action,
            )
            return success
        except Exception as e:
            console.print(f"[red]Error updating {vendor_name}: {e}[/red]")
            return False

    def _map_status(self, status: VendorStatus) -> Optional[str]:
        """Map VendorStatus to Slack Lists status option."""
        mapping = {
            VendorStatus.REVIEWING: "검토 중",
            VendorStatus.QUOTE_WAITING: "견적 대기",
            VendorStatus.NEGOTIATING: "협상 중",
            VendorStatus.ON_HOLD: "보류",
            VendorStatus.QUOTE_RECEIVED: "검토 중",  # Map to reviewing
            VendorStatus.CONTRACT_REVIEW: "협상 중",  # Map to negotiating
        }
        return mapping.get(status)

    def refresh_summary(self) -> bool:
        """Refresh the pinned summary message."""
        try:
            items = self.manager.get_list_items()
            message = self.manager.generate_summary_message(items)
            ts = self.manager.post_summary(message)
            return ts is not None
        except Exception as e:
            console.print(f"[red]Error refreshing summary: {e}[/red]")
            return False


# =============================================================================
# Main Pipeline
# =============================================================================

class SyncPipeline:
    """Main 4-layer sync pipeline."""

    def __init__(
        self,
        config_path: Optional[Path] = None,
    ):
        """
        Initialize pipeline.

        Args:
            config_path: Path to YAML config file
        """
        # Load config
        if config_path is None:
            config_path = _wsoptv_root / "wsoptv_sync_config.yaml"

        self.config = ProjectConfig.from_yaml(config_path)

        # Initialize state
        self.state = SyncStateV2(self.config.state_file)

        # Initialize clients
        self.gmail_client = GmailClient()

        # Initialize components
        self.thread_analyzer = ThreadAnalyzer(self.gmail_client, self.config)
        self.status_inferencer = StatusInferencer(self.config)
        self.attachment_downloader = AttachmentDownloader(
            self.gmail_client,
            self.config.attachments_dir,
        )
        self.quote_aggregator = QuoteAggregator(self.config)
        self.slack_writer = SlackListsWriter(self.config)

    def sync_vendor_states(
        self,
        days: int = 7,
        vendor_filter: Optional[str] = None,
        dry_run: bool = False,
        full_scan: bool = False,
    ) -> Dict:
        """
        Main sync workflow.

        Args:
            days: Number of days to look back
            vendor_filter: Filter to specific vendor
            dry_run: Preview changes without applying
            full_scan: Process all emails, ignore incremental state

        Returns:
            Results dict with counts and details
        """
        results = {
            "vendors_processed": 0,
            "threads_analyzed": 0,
            "quotes_extracted": 0,
            "status_changes": [],
            "errors": [],
        }

        console.print(Panel(
            f"[bold]Slack Lists Sync v2[/bold]\n"
            f"Mode: {'FULL' if full_scan else 'INCREMENTAL'}\n"
            f"Days: {days}\n"
            f"Vendor: {vendor_filter or 'All'}",
            title="Sync Configuration",
        ))

        # Layer 1: Collect emails
        with Progress(
            TextColumn("[bold blue]>>>[/bold blue]"),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Layer 1: Collecting emails...", total=None)

            vendor_emails = self._collect_vendor_emails(days, vendor_filter, full_scan)
            progress.update(task, completed=True)

        console.print(f"  Found {sum(len(v) for v in vendor_emails.values())} emails from {len(vendor_emails)} vendors")

        # Layer 2: Analyze threads and attachments
        with Progress(
            TextColumn("[bold blue]>>>[/bold blue]"),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Layer 2: Analyzing...", total=None)

            vendor_states = self._analyze_vendors(vendor_emails)
            results["threads_analyzed"] = sum(len(v.threads) for v in vendor_states.values())
            progress.update(task, completed=True)

        console.print(f"  Analyzed {results['threads_analyzed']} threads")

        # Layer 3: Process status and quotes
        with Progress(
            TextColumn("[bold blue]>>>[/bold blue]"),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Layer 3: Processing...", total=None)

            transitions = self._process_status_changes(vendor_states)
            results["status_changes"] = transitions
            progress.update(task, completed=True)

        console.print(f"  Detected {len(transitions)} status changes")

        # Layer 4: Write to Slack Lists
        with Progress(
            TextColumn("[bold blue]>>>[/bold blue]"),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Layer 4: Writing to Slack...", total=None)

            self._write_to_slack(vendor_states, transitions, dry_run)
            results["vendors_processed"] = len(vendor_states)
            progress.update(task, completed=True)

        # Save state
        if not dry_run:
            self.state.save()
            console.print("[green]State saved[/green]")

        # Display results
        self._display_results(results, vendor_states, transitions)

        return results

    def _collect_vendor_emails(
        self,
        days: int,
        vendor_filter: Optional[str],
        full_scan: bool,
    ) -> Dict[str, List]:
        """Collect emails grouped by vendor."""
        vendor_emails: Dict[str, List] = {}

        after_date = (datetime.now() - timedelta(days=days)).strftime("%Y/%m/%d")

        for vendor in self.config.vendors:
            if vendor_filter and vendor_filter.lower() not in vendor.name.lower():
                continue

            # Build query for vendor domains
            domain_queries = [f"from:{d}" for d in vendor.domains]
            domain_queries.extend([f"to:{d}" for d in vendor.domains])
            query = f"({' OR '.join(domain_queries)}) after:{after_date}"

            try:
                emails = self.gmail_client.list_emails(query=query, max_results=50)

                # Filter out processed emails in incremental mode
                if not full_scan:
                    emails = [
                        e for e in emails
                        if not self.state.is_email_processed(
                            getattr(e, "id", "") or getattr(e, "message_id", "")
                        )
                    ]

                if emails:
                    vendor_emails[vendor.name] = emails

            except Exception as e:
                console.print(f"[yellow]Warning: Failed to fetch emails for {vendor.name}: {e}[/yellow]")

        return vendor_emails

    def _analyze_vendors(
        self,
        vendor_emails: Dict[str, List],
    ) -> Dict[str, VendorState]:
        """Analyze emails and build vendor states."""
        vendor_states: Dict[str, VendorState] = {}

        for vendor_name, emails in vendor_emails.items():
            # Get existing state or create new
            stored = self.state.get_vendor_state(vendor_name)
            status = VendorStatus(stored.get("status", "initial_contact")) if stored else VendorStatus.INITIAL_CONTACT

            # Analyze threads
            thread_ids = set()
            for email in emails:
                tid = getattr(email, "thread_id", None)
                if tid:
                    thread_ids.add(tid)

                # Mark email processed
                email_id = getattr(email, "id", "") or getattr(email, "message_id", "")
                if email_id:
                    self.state.mark_email_processed(email_id)

            # Analyze each thread
            threads: List[EmailThread] = []
            for tid in thread_ids:
                try:
                    thread = self.thread_analyzer.analyze(tid)
                    threads.append(thread)
                    self.state.mark_thread_processed(tid)
                except Exception as e:
                    console.print(f"[yellow]Warning: Thread {tid} analysis failed: {e}[/yellow]")

            # Find latest contact date
            last_contact = None
            for thread in threads:
                if thread.last_date and (last_contact is None or thread.last_date > last_contact):
                    last_contact = thread.last_date

            # Get stored quote
            stored_quote = self.state.get_quote(vendor_name)
            quote = VendorQuote(vendor=vendor_name)
            if stored_quote:
                quote = VendorQuote(
                    vendor=vendor_name,
                    options=[QuoteOption(**o) for o in stored_quote.get("options", [])],
                    received_date=datetime.fromisoformat(stored_quote["received_date"]) if stored_quote.get("received_date") else None,
                )

            vendor_states[vendor_name] = VendorState(
                vendor_name=vendor_name,
                status=status,
                threads=threads,
                quote=quote,
                last_contact=last_contact,
            )

        return vendor_states

    def _process_status_changes(
        self,
        vendor_states: Dict[str, VendorState],
    ) -> List[StatusTransition]:
        """Process and infer status changes."""
        transitions: List[StatusTransition] = []

        for vendor_name, state in vendor_states.items():
            transition = self.status_inferencer.infer_vendor_status(state)

            if transition:
                transitions.append(transition)

                # Handle transition
                if transition.requires_approval:
                    self.state.add_pending_transition({
                        "vendor": vendor_name,
                        "from": transition.from_status.value,
                        "to": transition.to_status.value,
                        "trigger": transition.trigger,
                        "confidence": transition.confidence,
                    })
                else:
                    # Auto-apply positive transitions
                    state.status = transition.to_status

        return transitions

    def _write_to_slack(
        self,
        vendor_states: Dict[str, VendorState],
        transitions: List[StatusTransition],
        dry_run: bool,
    ):
        """Write states to Slack Lists."""
        for vendor_name, state in vendor_states.items():
            # Update vendor state
            self.slack_writer.update_vendor(state, dry_run)

            # Store state
            if not dry_run:
                self.state.update_vendor_state(vendor_name, {
                    "status": state.status.value,
                    "last_contact": state.last_contact.isoformat() if state.last_contact else None,
                    "has_negotiation": state.has_active_negotiation,
                })

        # Refresh summary
        if not dry_run:
            self.slack_writer.refresh_summary()

    def _display_results(
        self,
        results: Dict,
        vendor_states: Dict[str, VendorState],
        transitions: List[StatusTransition],
    ):
        """Display sync results."""
        table = Table(title="Sync Results")
        table.add_column("Vendor", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Threads", justify="right")
        table.add_column("Last Contact")
        table.add_column("Quote")

        for vendor_name, state in vendor_states.items():
            table.add_row(
                vendor_name,
                state.status.value,
                str(len(state.threads)),
                state.last_contact.strftime("%Y-%m-%d") if state.last_contact else "-",
                state.quote_summary,
            )

        console.print(table)

        # Show status transitions
        if transitions:
            console.print("\n[bold]Status Transitions:[/bold]")
            for t in transitions:
                approval = " [yellow](needs approval)[/yellow]" if t.requires_approval else ""
                console.print(f"  {t.from_status.value} -> {t.to_status.value} (trigger: {t.trigger}){approval}")

    def analyze_threads(
        self,
        vendor_filter: Optional[str] = None,
        days: int = 30,
    ) -> Dict[str, List[EmailThread]]:
        """
        Analyze threads for all or specific vendor.

        Args:
            vendor_filter: Filter to specific vendor
            days: Number of days to look back

        Returns:
            Dict mapping vendor name to list of threads
        """
        results: Dict[str, List[EmailThread]] = {}

        for vendor in self.config.vendors:
            if vendor_filter and vendor_filter.lower() not in vendor.name.lower():
                continue

            console.print(f"Analyzing threads for [cyan]{vendor.name}[/cyan]...")

            for domain in vendor.domains:
                threads = self.thread_analyzer.analyze_vendor_threads(domain, days)
                if threads:
                    if vendor.name not in results:
                        results[vendor.name] = []
                    results[vendor.name].extend(threads)

        # Display results
        for vendor_name, threads in results.items():
            active = self.thread_analyzer.detect_active_negotiations(threads)
            console.print(f"  {vendor_name}: {len(threads)} threads ({len(active)} active negotiations)")

        return results

    def extract_quotes(
        self,
        vendor_filter: Optional[str] = None,
        days: int = 30,
    ) -> Dict[str, VendorQuote]:
        """
        Extract quotes from vendor attachments.

        Args:
            vendor_filter: Filter to specific vendor
            days: Number of days to look back

        Returns:
            Dict mapping vendor name to VendorQuote
        """
        results: Dict[str, VendorQuote] = {}

        # First collect emails with attachments
        after_date = (datetime.now() - timedelta(days=days)).strftime("%Y/%m/%d")

        for vendor in self.config.vendors:
            if vendor_filter and vendor_filter.lower() not in vendor.name.lower():
                continue

            console.print(f"Extracting quotes for [cyan]{vendor.name}[/cyan]...")

            # Build query
            domain_queries = [f"from:{d}" for d in vendor.domains]
            query = f"({' OR '.join(domain_queries)}) has:attachment after:{after_date}"

            try:
                emails = self.gmail_client.list_emails(query=query, max_results=20)
            except Exception as e:
                console.print(f"[yellow]Warning: Failed to fetch emails: {e}[/yellow]")
                continue

            # Download and parse attachments
            all_attachments: List[Attachment] = []

            for email in emails:
                email_id = getattr(email, "id", "") or getattr(email, "message_id", "")
                if not email_id:
                    continue

                attachments = self.attachment_downloader.get_quote_attachments(email_id)
                all_attachments.extend(attachments)

            console.print(f"  Downloaded {len(all_attachments)} attachments")

            # Aggregate quotes
            quote = self.quote_aggregator.aggregate_from_attachments(
                all_attachments,
                vendor.name,
            )

            if quote.options:
                results[vendor.name] = quote

                # Store in state
                self.state.add_quote(vendor.name, {
                    "options": [o.model_dump() for o in quote.options],
                    "received_date": quote.received_date.isoformat() if quote.received_date else None,
                })

                console.print(f"  Found {len(quote.options)} quote options")
                for opt in quote.options:
                    console.print(f"    - {opt.option_name}: {opt.total_amount_display}")

        self.state.save()
        return results


# =============================================================================
# CLI Commands
# =============================================================================

@app.command()
def sync(
    days: int = typer.Option(7, "--days", "-d", help="Number of days to look back"),
    vendor: Optional[str] = typer.Option(None, "--vendor", "-v", help="Filter to specific vendor"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview changes without applying"),
    full: bool = typer.Option(False, "--full", help="Full scan (ignore incremental state)"),
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="Path to config file"),
):
    """
    Sync vendor states to Slack Lists.

    Main workflow that collects Gmail, analyzes threads, infers status changes,
    and updates Slack Lists.
    """
    pipeline = SyncPipeline(config)
    pipeline.sync_vendor_states(
        days=days,
        vendor_filter=vendor,
        dry_run=dry_run,
        full_scan=full,
    )


@app.command()
def status():
    """Show current sync state and statistics."""
    config_path = _wsoptv_root / "wsoptv_sync_config.yaml"
    config = ProjectConfig.from_yaml(config_path)
    state = SyncStateV2(config.state_file)
    stats = state.get_stats()

    table = Table(title="Sync State v2")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Last Sync", stats["last_sync"] or "Never")
    table.add_row("Processed Emails", str(stats["processed_emails"]))
    table.add_row("Processed Threads", str(stats["processed_threads"]))
    table.add_row("Vendors Tracked", str(stats["vendors_tracked"]))
    table.add_row("Quotes Stored", str(stats["quotes_stored"]))
    table.add_row("Pending Transitions", str(stats["pending_transitions"]))

    console.print(table)

    # Show pending transitions
    pending = state.get_pending_transitions()
    if pending:
        console.print("\n[bold]Pending Transitions (require approval):[/bold]")
        for p in pending:
            console.print(f"  {p['vendor']}: {p['from']} -> {p['to']} (trigger: {p['trigger']})")


@app.command("analyze-threads")
def analyze_threads_cmd(
    vendor: Optional[str] = typer.Option(None, "--vendor", "-v", help="Filter to specific vendor"),
    days: int = typer.Option(30, "--days", "-d", help="Number of days to look back"),
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="Path to config file"),
):
    """Analyze email threads for vendors."""
    pipeline = SyncPipeline(config)
    pipeline.analyze_threads(vendor_filter=vendor, days=days)


@app.command("analyze-attachments")
def analyze_attachments_cmd(
    vendor: Optional[str] = typer.Option(None, "--vendor", "-v", help="Filter to specific vendor"),
    days: int = typer.Option(30, "--days", "-d", help="Number of days to look back"),
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="Path to config file"),
):
    """Extract quotes from vendor attachments."""
    pipeline = SyncPipeline(config)
    pipeline.extract_quotes(vendor_filter=vendor, days=days)


@app.command("approve")
def approve_transitions(
    vendor: Optional[str] = typer.Option(None, "--vendor", "-v", help="Approve for specific vendor"),
    all_pending: bool = typer.Option(False, "--all", help="Approve all pending transitions"),
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="Path to config file"),
):
    """Approve pending status transitions."""
    config_path = config or _wsoptv_root / "wsoptv_sync_config.yaml"
    proj_config = ProjectConfig.from_yaml(config_path)
    state = SyncStateV2(proj_config.state_file)
    pending = state.get_pending_transitions()

    if not pending:
        console.print("[green]No pending transitions[/green]")
        return

    # Filter
    if vendor:
        pending = [p for p in pending if vendor.lower() in p["vendor"].lower()]

    if not pending:
        console.print(f"[yellow]No pending transitions for {vendor}[/yellow]")
        return

    console.print("[bold]Pending Transitions:[/bold]")
    for i, p in enumerate(pending, 1):
        console.print(f"  {i}. {p['vendor']}: {p['from']} -> {p['to']}")

    if not all_pending:
        confirm = typer.confirm("Approve all listed transitions?")
        if not confirm:
            console.print("[yellow]Cancelled[/yellow]")
            return

    # Apply transitions
    slack_writer = SlackListsWriter(proj_config)

    for p in pending:
        try:
            # Update Slack Lists
            status_map = {
                "reviewing": "검토 중",
                "negotiating": "협상 중",
                "on_hold": "보류",
                "excluded": "제외",
            }
            status_text = status_map.get(p["to"])
            if status_text:
                slack_writer.manager.update_item(
                    vendor_name=p["vendor"],
                    status=status_text,
                )
                console.print(f"[green]Updated {p['vendor']} to {p['to']}[/green]")

            # Update state
            state.update_vendor_state(p["vendor"], {"status": p["to"]})

        except Exception as e:
            console.print(f"[red]Error updating {p['vendor']}: {e}[/red]")

    # Clear approved transitions
    state.clear_pending_transitions()
    state.save()
    console.print("[green]Transitions applied and cleared[/green]")


@app.command("clear-state")
def clear_state(
    confirm: bool = typer.Option(False, "--yes", "-y", help="Confirm clearing state"),
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="Path to config file"),
):
    """Clear sync state (reset incremental tracking)."""
    if not confirm:
        console.print("[yellow]Use --yes to confirm clearing state[/yellow]")
        return

    config_path = config or _wsoptv_root / "wsoptv_sync_config.yaml"
    proj_config = ProjectConfig.from_yaml(config_path)

    if proj_config.state_file.exists():
        proj_config.state_file.unlink()
        console.print("[green]State cleared[/green]")
    else:
        console.print("[yellow]No state file found[/yellow]")


if __name__ == "__main__":
    app()
