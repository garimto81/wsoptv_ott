#!/usr/bin/env python
"""
WSOPTV Daily Sync Script

매일 아침 실행하여:
1. Slack 채널 메시지 수집 → SLACK-LOG.md
2. Gmail (WSOPTV 라벨) 수집 → EMAIL-LOG.md
3. Slack Lists 동기화 → VENDOR-DASHBOARD.md
4. 일일 요약 포스팅 → Slack 채널

Usage:
    python scripts/daily_sync.py                    # 전체 동기화
    python scripts/daily_sync.py --init             # 최초 1회 전체 수집 (365일)
    python scripts/daily_sync.py --slack            # Slack만
    python scripts/daily_sync.py --gmail            # Gmail만
    python scripts/daily_sync.py --lists            # Slack Lists만
    python scripts/daily_sync.py --post-summary     # 일일 요약 포스팅
    python scripts/daily_sync.py --dry-run          # 미리보기
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add scripts/sync to path
_script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(_script_dir / "sync"))
# Add C:\claude to path for lib imports
_claude_root = _script_dir.parents[1]
sys.path.insert(0, str(_claude_root))

from sync.slack_sync import sync_slack_to_log  # noqa: E402
from sync.gmail_sync import sync_gmail_to_log  # noqa: E402
from sync.lists_sync import sync_lists_to_dashboard, post_daily_summary, ListsSyncManager  # noqa: E402
from sync.models import SyncResult  # noqa: E402

app = typer.Typer(help="WSOPTV 일일 동기화 도구")
console = Console()

# Default paths
MANAGEMENT_DIR = Path("C:/claude/wsoptv_ott/docs/management")
SLACK_LOG = MANAGEMENT_DIR / "SLACK-LOG.md"
EMAIL_LOG = MANAGEMENT_DIR / "EMAIL-LOG.md"
VENDOR_DASHBOARD = MANAGEMENT_DIR / "VENDOR-DASHBOARD.md"
SYNC_STATE_FILE = MANAGEMENT_DIR / ".sync_state.json"

# Configuration
DEFAULT_CHANNEL_ID = "C09TX3M1J2W"
DEFAULT_GMAIL_LABEL = "wsoptv"
DAILY_DAYS = 7    # 매일 동기화: 최근 7일
INIT_DAYS = 365   # 초기화: 최근 1년


def save_sync_state(state: dict) -> None:
    """Save sync state to file."""
    import json
    SYNC_STATE_FILE.write_text(json.dumps(state, indent=2, default=str), encoding="utf-8")


def load_sync_state() -> dict:
    """Load sync state from file."""
    import json
    if SYNC_STATE_FILE.exists():
        return json.loads(SYNC_STATE_FILE.read_text(encoding="utf-8"))
    return {"initialized": False, "last_sync": None}


def print_header(text: str) -> None:
    """Print section header."""
    console.print(f"\n{'='*60}")
    console.print(f"  {text}")
    console.print(f"{'='*60}\n")


def print_result(name: str, result: SyncResult) -> None:
    """Print sync result."""
    if result.errors > 0:
        status = "[yellow]WARN[/yellow]"
    else:
        status = "[green]OK[/green]"

    console.print(f"  {status} {name}: added={result.added}, skipped={result.skipped}, errors={result.errors}")


@app.command()
def sync(
    init: bool = typer.Option(False, "--init", help="최초 1회 전체 수집 (과거 1년)"),
    slack: bool = typer.Option(False, "--slack", help="Slack 메시지만 동기화"),
    gmail: bool = typer.Option(False, "--gmail", help="Gmail만 동기화"),
    lists: bool = typer.Option(False, "--lists", help="Slack Lists만 동기화"),
    post_summary: bool = typer.Option(False, "--post-summary", help="일일 요약 Slack 포스팅"),
    dry_run: bool = typer.Option(False, "--dry-run", help="변경 없이 미리보기"),
    days: Optional[int] = typer.Option(None, "--days", help="동기화 기간 (일)"),
    channel: str = typer.Option(DEFAULT_CHANNEL_ID, "--channel", help="Slack 채널 ID"),
    label: str = typer.Option(DEFAULT_GMAIL_LABEL, "--label", help="Gmail 라벨"),
):
    """
    WSOPTV 프로젝트 관리 데이터 동기화.

    기본: 최근 7일간 Slack + Gmail + Lists 동기화
    --init: 최초 1회 전체 수집 (과거 1년)
    """
    # Determine sync scope
    sync_all = not (slack or gmail or lists or post_summary)
    sync_slack = slack or sync_all
    sync_gmail = gmail or sync_all
    sync_lists = lists or sync_all

    # Determine days
    if days is None:
        days = INIT_DAYS if init else DAILY_DAYS

    # Load state
    state = load_sync_state()

    if init:
        print_header(f"WSOPTV Initial Sync (past {days} days)")
        console.print("[yellow]Full collection mode - this may take a while[/yellow]\n")
    else:
        print_header(f"WSOPTV Daily Sync (last {days} days)")

    results = {}

    # 1. Slack 메시지 동기화
    if sync_slack:
        console.print("\n[bold]1. Slack Messages...[/bold]")
        try:
            result = sync_slack_to_log(
                log_path=SLACK_LOG,
                channel_id=channel,
                days=days,
                dry_run=dry_run,
            )
            results["slack"] = result
            print_result("Slack", result)
        except Exception as e:
            console.print(f"  [red]ERROR: Slack sync failed: {e}[/red]")
            results["slack"] = None

    # 2. Gmail 동기화
    if sync_gmail:
        console.print("\n[bold]2. Gmail...[/bold]")
        try:
            result = sync_gmail_to_log(
                log_path=EMAIL_LOG,
                query=f"label:{label}",
                days=days,
                dry_run=dry_run,
            )
            results["gmail"] = result
            print_result("Gmail", result)
        except Exception as e:
            console.print(f"  [red]ERROR: Gmail sync failed: {e}[/red]")
            results["gmail"] = None

    # 3. Slack Lists 동기화
    if sync_lists:
        console.print("\n[bold]3. Slack Lists...[/bold]")
        try:
            result = sync_lists_to_dashboard(
                dashboard_path=VENDOR_DASHBOARD,
                dry_run=dry_run,
            )
            results["lists"] = result
            print_result("Lists", result)
        except Exception as e:
            console.print(f"  [red]ERROR: Lists sync failed: {e}[/red]")
            results["lists"] = None

    # 4. 일일 요약 포스팅
    if post_summary or (sync_all and not dry_run and not init):
        console.print("\n[bold]4. Daily Summary Posting...[/bold]")
        try:
            success = post_daily_summary(dry_run=dry_run)
            if success:
                console.print("  [green]OK: Summary posted[/green]")
            else:
                console.print("  [yellow]WARN: Summary posting failed[/yellow]")
        except Exception as e:
            console.print(f"  [red]ERROR: Posting failed: {e}[/red]")

    # Summary
    console.print()
    if dry_run:
        console.print("[yellow]DRY RUN completed - no actual changes[/yellow]")
    else:
        # Update state
        state["last_sync"] = datetime.now().isoformat()
        if init:
            state["initialized"] = True
        save_sync_state(state)

        console.print("[green]Sync completed![/green]")

    # Statistics table
    table = Table(title="동기화 결과")
    table.add_column("소스", style="cyan")
    table.add_column("추가", justify="right", style="green")
    table.add_column("스킵", justify="right")
    table.add_column("에러", justify="right", style="red")

    for name, result in results.items():
        if result:
            table.add_row(name, str(result.added), str(result.skipped), str(result.errors))
        else:
            table.add_row(name, "-", "-", "실패")

    console.print(table)


@app.command()
def status():
    """현재 동기화 상태 확인."""
    state = load_sync_state()

    print_header("WSOPTV Sync Status")

    # Initialization status
    if state.get("initialized"):
        console.print("  [green]OK: Initialized[/green]")
    else:
        console.print("  [yellow]WARN: Not initialized (run --init)[/yellow]")

    # Last sync
    last_sync = state.get("last_sync")
    if last_sync:
        console.print(f"  마지막 동기화: {last_sync}")
    else:
        console.print("  마지막 동기화: 없음")

    # File status
    console.print("\n[bold]파일 상태:[/bold]")

    files = [
        ("SLACK-LOG.md", SLACK_LOG),
        ("EMAIL-LOG.md", EMAIL_LOG),
        ("VENDOR-DASHBOARD.md", VENDOR_DASHBOARD),
    ]

    for name, path in files:
        if path.exists():
            size = path.stat().st_size
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
            console.print(f"  [green]OK[/green] {name}: {size:,}B, modified: {mtime:%Y-%m-%d %H:%M}")
        else:
            console.print(f"  [red]MISSING[/red] {name}")


@app.command()
def analyze():
    """수집된 데이터 분석 및 인사이트 생성."""
    print_header("Data Analysis")

    try:
        manager = ListsSyncManager()
        items = manager.get_list_items()

        # Status breakdown
        console.print("\n[bold]업체별 현황:[/bold]")
        table = Table()
        table.add_column("업체", style="cyan")
        table.add_column("상태")
        table.add_column("견적")
        table.add_column("다음 액션")

        for item in items:
            status_emoji = {
                "협상 중": "[green]>>[/green]",
                "검토 중": "[yellow]--[/yellow]",
                "견적 대기": "[cyan]..[/cyan]",
                "보류": "[red]XX[/red]",
            }.get(item.get("status", ""), "--")

            table.add_row(
                item.get("vendor_name", "-"),
                f"{status_emoji} {item.get('status', '-')}",
                item.get("quote", "-"),
                item.get("next_action", "-"),
            )

        console.print(table)

        # Pending actions
        console.print("\n[bold]Pending Actions:[/bold]")
        for item in items:
            if item.get("next_action") and item.get("next_action") != "-":
                console.print(f"  - {item['vendor_name']}: {item['next_action']}")

    except Exception as e:
        console.print(f"[red]분석 실패: {e}[/red]")


@app.command()
def post(
    dry_run: bool = typer.Option(False, "--dry-run", help="포스팅 없이 미리보기"),
):
    """일일 요약을 Slack에 포스팅."""
    print_header("Daily Summary Posting")

    success = post_daily_summary(dry_run=dry_run)

    if success:
        if dry_run:
            console.print("[yellow]DRY RUN - no actual posting[/yellow]")
        else:
            console.print("[green]Posting completed[/green]")
    else:
        console.print("[red]Posting failed[/red]")


def main():
    """Entry point."""
    app()


if __name__ == "__main__":
    main()
