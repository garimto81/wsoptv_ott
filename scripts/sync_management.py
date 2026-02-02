"""
Management synchronization CLI script.

Integrates Gmail and Slack synchronization to WSOPTV management logs.
"""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

# Add scripts/sync to path
_script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(_script_dir / "sync"))

from sync.slack_sync import sync_slack_to_log  # noqa: E402

app = typer.Typer(help="WSOPTV Management Synchronization Tool")
console = Console()


@app.command()
def sync(
    gmail: bool = typer.Option(False, "--gmail", help="Sync Gmail only"),
    slack: bool = typer.Option(False, "--slack", help="Sync Slack only"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be synced without writing"),
    days: int = typer.Option(7, "--days", help="Number of days to sync"),
    channel_id: str = typer.Option("C09TX3M1J2W", "--channel", help="Slack channel ID"),
):
    """
    Synchronize Gmail and Slack to management logs.

    By default, syncs both Gmail and Slack.
    Use --gmail or --slack to sync only one source.
    """
    # Default: sync both if neither flag is set
    sync_gmail = gmail or (not gmail and not slack)
    sync_slack = slack or (not gmail and not slack)

    results = {}

    # Gmail sync (placeholder - not yet implemented)
    if sync_gmail:
        console.print("[bold cyan]Gmail 동기화 중...[/bold cyan]")
        console.print("  [yellow]Gmail 동기화는 아직 구현되지 않았습니다.[/yellow]")
        results["gmail"] = None

    # Slack sync
    if sync_slack:
        console.print("\n[bold cyan]Slack 동기화 중...[/bold cyan]")

        try:
            slack_log_path = Path("C:/claude/wsoptv_ott/docs/management/SLACK-LOG.md")
            result = sync_slack_to_log(
                log_path=slack_log_path,
                channel_id=channel_id,
                days=days,
                dry_run=dry_run,
            )

            results["slack"] = result

            # Summary
            console.print(f"  [green]{result.added}개 추가, {result.skipped}개 스킵[/green]")

            if result.errors > 0:
                console.print(f"  [yellow]{result.errors}개 에러[/yellow]")

        except Exception as e:
            console.print(f"  [red]Slack 동기화 실패: {e}[/red]")
            results["slack"] = None

    # Final summary
    if not dry_run:
        console.print("\n[bold green]동기화 완료![/bold green]")
    else:
        console.print("\n[bold yellow]Dry-run 완료 (파일 변경 없음)[/bold yellow]")

    # Show stats
    console.print("\n[bold]통계:[/bold]")
    if results.get("gmail"):
        console.print(f"  Gmail: {results['gmail']}")
    if results.get("slack"):
        console.print(f"  Slack: {results['slack']}")


@app.command()
def status():
    """Show current synchronization status."""
    console.print("[bold cyan]== 동기화 상태 ==[/bold cyan]")

    # Check Slack log
    slack_log_path = Path("C:/claude/wsoptv_ott/docs/management/SLACK-LOG.md")
    if slack_log_path.exists():
        content = slack_log_path.read_text(encoding="utf-8")
        # Count entries by looking for ts comments
        import re

        entries = len(re.findall(r"<!-- ts: [\d.]+ -->", content))
        console.print(f"  [green]Slack 로그: {entries}개 메시지[/green]")
    else:
        console.print("  [yellow]Slack 로그: 없음[/yellow]")

    # Check Gmail log (placeholder)
    gmail_log_path = Path("C:/claude/wsoptv_ott/docs/management/GMAIL-LOG.md")
    if gmail_log_path.exists():
        console.print("  [green]Gmail 로그: 존재함[/green]")
    else:
        console.print("  [yellow]Gmail 로그: 없음[/yellow]")


@app.command()
def init():
    """Initialize management log files."""
    console.print("[bold cyan]관리 로그 파일 초기화 중...[/bold cyan]")

    # Create management directory
    mgmt_dir = Path("C:/claude/wsoptv_ott/docs/management")
    mgmt_dir.mkdir(parents=True, exist_ok=True)

    # Initialize Slack log
    slack_log = mgmt_dir / "SLACK-LOG.md"
    if not slack_log.exists():
        from datetime import datetime

        initial_content = f"""# WSOPTV 슬랙 관리 로그

**최종 업데이트**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

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

"""
        slack_log.write_text(initial_content, encoding="utf-8")
        console.print(f"  [green]{slack_log} 생성됨[/green]")
    else:
        console.print(f"  [blue]{slack_log} 이미 존재함[/blue]")

    # Initialize Gmail log (placeholder)
    gmail_log = mgmt_dir / "GMAIL-LOG.md"
    if not gmail_log.exists():
        gmail_log.write_text("# WSOPTV Gmail 관리 로그\n\n(준비 중)\n", encoding="utf-8")
        console.print(f"  [green]{gmail_log} 생성됨[/green]")
    else:
        console.print(f"  [blue]{gmail_log} 이미 존재함[/blue]")

    console.print("\n[bold green]초기화 완료![/bold green]")


def main():
    """Entry point."""
    app()


if __name__ == "__main__":
    main()
