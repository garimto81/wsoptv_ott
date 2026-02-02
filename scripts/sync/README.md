# Management Synchronization System

Gmail과 Slack 메시지를 관리 로그로 동기화하는 시스템입니다.

## 설치

```powershell
pip install typer rich
```

## 사용법

### 통합 CLI (권장)

```powershell
# 전체 동기화 (Gmail + Slack)
python scripts/sync_management.py sync

# Gmail만 동기화
python scripts/sync_management.py sync --gmail

# Slack만 동기화
python scripts/sync_management.py sync --slack

# Dry-run (실제 파일 변경 없이 미리보기)
python scripts/sync_management.py sync --dry-run

# 특정 기간 동기화 (기본값: 7일)
python scripts/sync_management.py sync --days 14

# 상태 확인
python scripts/sync_management.py status

# 초기화
python scripts/sync_management.py init
```

### 개별 모듈

```powershell
# Slack 직접 실행
python scripts/sync/slack_sync.py --days 7 --dry-run

# Gmail 직접 실행 (준비 중)
python scripts/sync/gmail_sync.py
```

## 아키텍처

```
scripts/
├── sync_management.py          # 통합 CLI (typer)
└── sync/
    ├── __init__.py
    ├── models.py               # 공유 데이터 모델
    ├── slack_sync.py           # Slack 동기화
    └── gmail_sync.py           # Gmail 동기화 (준비 중)
```

## 출력 파일

| 파일 | 내용 |
|------|------|
| `docs/management/SLACK-LOG.md` | Slack 메시지 로그 (의사결정/액션 아이템 자동 감지) |
| `docs/management/GMAIL-LOG.md` | Gmail 메시지 로그 (준비 중) |

## 기능

### Slack 동기화

- 채널 히스토리 자동 가져오기
- 메시지 중복 방지 (ts 기반)
- 의사결정 자동 감지
- 액션 아이템 자동 감지
- 날짜별 그룹화 (최신순)

### Gmail 동기화 (준비 중)

- 라벨 기반 필터링
- 양방향 (보낸 메일/받은 메일)
- 상태 추적 (대기/진행 중/완료)

## 패턴 감지

### 의사결정 키워드

- 결정, 확정, 동의합니다, 합의
- 이렇게...진행, 승인, 채택

### 액션 아이템 패턴

- @사용자 ... YYYY-MM-DD
- 담당: @사용자
- @사용자 ... 검토/확인/업데이트

## 환경 변수

```powershell
# Slack (필수)
$env:SLACK_BOT_TOKEN = "xoxb-..."

# Gmail (선택, 준비 중)
# OAuth 브라우저 인증 사용
```

## 데이터 모델

### SyncResult

```python
@dataclass
class SyncResult:
    added: int = 0      # 새로 추가된 항목
    skipped: int = 0    # 이미 존재하는 항목
    errors: int = 0     # 에러 발생 항목
```

### SlackDecision

```python
@dataclass
class SlackDecision:
    decision_id: str
    timestamp: datetime
    channel: str
    participants: list[str]
    decision_text: str
    rationale: str
    follow_ups: list[str]
```

### SlackActionItem

```python
@dataclass
class SlackActionItem:
    assignee: str
    description: str
    source_channel: str
    source_date: datetime
    requester: str
    deadline: Optional[datetime]
    status: ActionItemStatus
    slack_ts: str
```

## 예제 출력

```
Slack 동기화 중...
Fetching messages from #wsoptv-project (last 7 days)...
Found 23 messages
Existing entries: 15

  8개 추가, 15개 스킵

동기화 완료!

통계:
  Slack: Added: 8, Skipped: 15, Errors: 0
```

## 문제 해결

### Slack 토큰 에러

```powershell
# 환경 변수 확인
echo $env:SLACK_BOT_TOKEN

# 토큰 재설정
$env:SLACK_BOT_TOKEN = "xoxb-..."
```

### 중복 메시지

시스템이 자동으로 방지합니다. `<!-- ts: 1706824200.123456 -->` 주석을 이용한 중복 체크.

### 날짜 정렬 문제

SLACK-LOG.md를 수동으로 편집한 경우, 백업 후 `init` 명령으로 재생성하세요.

## 자동화 설정

Windows Task Scheduler로 매일 자동 실행:

```powershell
# Task Scheduler 열기
taskschd.msc

# 새 작업 만들기
# 트리거: 매일 09:00
# 동작: python.exe C:\claude\wsoptv_ott\scripts\sync_management.py sync
```

## 향후 계획

- [ ] Gmail 동기화 구현
- [ ] 의사결정 요약 자동 생성
- [ ] 액션 아이템 대시보드
- [ ] Slack 알림 연동
- [ ] GitHub Issues 연동

## 개발자 정보

### 클래스 구조

```python
# slack_sync.py
PatternDetector      # 패턴 감지 (결정/액션)
MarkdownParser       # 기존 로그 파싱
SlackLogFormatter    # 메시지 포맷팅
sync_slack_to_log()  # 메인 동기화 함수

# models.py
SyncResult           # 동기화 결과
SlackDecision        # 의사결정 기록
SlackActionItem      # 액션 아이템
EmailLogEntry        # Gmail 로그 항목
```

### 테스트

```powershell
# CLI 테스트
python scripts/sync_management.py --help
python scripts/sync_management.py sync --help
python scripts/sync_management.py status

# 패턴 감지 테스트
python -c "from scripts.sync.slack_sync import PatternDetector; print(PatternDetector.is_decision('결정합니다'))"
```
