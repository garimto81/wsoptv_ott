"""
WSOPTV 업체 관리 칸반보드 - Slack Lists 설정 스크립트

Slack Lists API를 사용하여 업체 선정 프로세스를 추적하는 칸반보드를 생성합니다.

Requirements:
- Slack 유료 플랜 (Lists 기능 필수)
- lib.slack 라이브러리 인증 완료

Usage:
    python scripts/setup_slack_kanban.py
"""

import sys
from pathlib import Path

# Add C:\claude to path for lib.slack import
_script_dir = Path(__file__).resolve().parent
_wsoptv_root = _script_dir.parent
_claude_root = _script_dir.parents[1]
sys.path.insert(0, str(_claude_root))

from lib.slack import SlackClient  # noqa: E402


def create_vendor_kanban():
    """Create WSOPTV Vendor Management Kanban Board."""

    client = SlackClient()

    # 1. 리스트 생성
    print("Creating WSOPTV Vendor Kanban Board...")

    # 칸반 컬럼 정의 - 단순화 (todo_mode가 기본 컬럼 추가)
    # todo_mode=True로 설정하면 Completed, Assignee, Due date 자동 추가됨
    columns = [
        {
            "key": "vendor_name",
            "name": "업체명",
            "type": "text",
            "is_primary_column": True,
        },
        {
            "key": "status",
            "name": "상태",
            "type": "select",
            "options": {
                "choices": [
                    {"label": "RFP 발송", "value": "rfp_sent", "color": "blue"},
                    {"label": "견적 대기", "value": "quote_pending", "color": "yellow"},
                    {"label": "평가 중", "value": "evaluating", "color": "orange"},
                    {"label": "협상 중", "value": "negotiating", "color": "green"},
                    {"label": "완료", "value": "completed", "color": "green"},
                    {"label": "제외", "value": "excluded", "color": "red"},
                ]
            },
        },
        {
            "key": "quote",
            "name": "견적",
            "type": "text",
        },
        {
            "key": "notes",
            "name": "비고",
            "type": "text",
        },
    ]

    try:
        result = client.create_list(
            name="WSOPTV 업체 관리 칸반보드",
            description="OTT 플랫폼 구축 대행사 선정 프로세스 추적",
            todo_mode=True,  # Assignee, Due date 컬럼 자동 추가
            schema=columns,
        )

        list_id = result.get("list", {}).get("id")
        print(f"[OK] List created: {list_id}")

        # 2. 업체 아이템 추가
        vendors = [
            {
                "vendor_name": "메가존클라우드",
                "status": "협상 중",
                "quote": "48억 (구축) + 15억/년",
                "notes": "최우선 협상 대상, 평가점수 3.9",
            },
            {
                "vendor_name": "Brightcove",
                "status": "견적 대기",
                "quote": "대기 중",
                "notes": "D+5 미회신, 리마인더 필요",
            },
            {
                "vendor_name": "Vimeo OTT",
                "status": "제외",
                "quote": "-",
                "notes": "매각 진행 중으로 제외",
            },
            {
                "vendor_name": "맑음소프트",
                "status": "제외",
                "quote": "-",
                "notes": "Multi-view 미지원으로 제외",
            },
        ]

        print("\nAdding vendor items...")
        for vendor in vendors:
            try:
                item_result = client.add_list_item(list_id, vendor)
                item_id = item_result.get("item", {}).get("id")
                print(f"  ✅ {vendor['vendor_name']}: {item_id}")
            except Exception as e:
                print(f"  ❌ {vendor['vendor_name']}: {e}")

        print(f"\n🎉 칸반보드 생성 완료!")
        print(f"   List ID: {list_id}")
        print(f"   Slack에서 Lists 탭 → Layout → Board 선택하여 칸반 뷰로 전환하세요")

        return list_id

    except Exception as e:
        error_msg = str(e)

        if "paid_only" in error_msg or "not_allowed" in error_msg:
            print("\n❌ Slack Lists는 유료 플랜에서만 사용 가능합니다.")
            print("   - Slack Pro, Business+, Enterprise Grid 플랜 필요")
            print("\n대안:")
            print("   1. Slack 유료 플랜 업그레이드")
            print("   2. Trello 연동 (무료)")
            print("   3. Notion 연동 (무료)")
            print("   4. 현재 Markdown 대시보드 유지")
        elif "missing_scope" in error_msg:
            print("\n❌ Slack 앱에 Lists 권한이 없습니다.")
            print("   필요한 scope: lists:write, lists:read")
            print("   Slack App 설정에서 OAuth Scopes 추가 후 재인증하세요")
        else:
            print(f"\n❌ 오류 발생: {e}")

        return None


def check_slack_plan():
    """Check if Slack workspace supports Lists."""
    client = SlackClient()

    try:
        # auth.test로 워크스페이스 정보 확인
        auth_info = client.auth_test()
        team = auth_info.get("team", "Unknown")
        user = auth_info.get("user", "Unknown")

        print(f"Slack Workspace: {team}")
        print(f"Authenticated as: {user}")
        print()

        return True
    except Exception as e:
        print(f"❌ Slack 인증 실패: {e}")
        return False


def main():
    """Main entry point."""
    print("=" * 50)
    print("WSOPTV 업체 관리 칸반보드 설정")
    print("=" * 50)
    print()

    # 1. Slack 인증 확인
    print("1. Slack 연결 확인...")
    if not check_slack_plan():
        return

    # 2. 칸반보드 생성
    print("2. 칸반보드 생성...")
    list_id = create_vendor_kanban()

    if list_id:
        # 설정 정보 저장
        config_path = Path("C:/claude/wsoptv_ott/docs/management/slack-kanban-config.md")
        config_content = f"""# Slack Kanban Board 설정

**생성일**: 2026-02-02
**List ID**: `{list_id}`

## 사용 방법

1. Slack 열기
2. 좌측 사이드바 → **Lists** 탭
3. "WSOPTV 업체 관리 칸반보드" 선택
4. 우측 상단 필터 아이콘 → **Layout** → **Board** 선택

## 컬럼 (상태별)

| 상태 | 의미 |
|------|------|
| 🔵 RFP 발송 | 제안 요청 발송 완료 |
| 🟡 견적 대기 | 견적서 회신 대기 중 |
| 🟠 평가 중 | 평가표 작성 중 |
| 🟢 협상 중 | 우선협상대상 선정, 계약 협상 |
| ✅ 완료 | 계약 체결 완료 |
| 🔴 제외 | 선정 불가 |

## 동기화

- Slack Lists ↔ VENDOR-DASHBOARD.md 수동 동기화
- 주요 변경 시 양쪽 업데이트 필요
"""
        config_path.write_text(config_content, encoding="utf-8")
        print(f"\n설정 정보 저장: {config_path}")


if __name__ == "__main__":
    main()
