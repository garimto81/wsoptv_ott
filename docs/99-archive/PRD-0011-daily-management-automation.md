# PRD-0011: WSOPTV 일일 프로젝트 관리 자동화

**버전**: 1.1.0
**작성일**: 2026-02-02
**작성자**: Claude Code
**상태**: Implemented

---

## 1. 개요

### 1.1 배경

WSOPTV 프로젝트는 4개 업체(메가존클라우드, Brightcove, Vimeo OTT, 맑음소프트)와의 RFP 프로세스를 관리하며, Gmail, Slack, Slack Lists 등 다양한 채널을 통해 커뮤니케이션합니다.

현재 관리 체계:
- **이메일**: `docs/management/EMAIL-LOG.md` - 업체별 이메일 추적
- **슬랙**: `docs/management/SLACK-LOG.md` - 의사결정/액션 아이템
- **업체 현황**: `docs/management/VENDOR-DASHBOARD.md` - RFP 진행 상태
- **칸반 보드**: Slack Lists (`F0ACQJS6KND`) - 실시간 상태 관리

**문제점**: 매일 수동으로 동기화 작업 필요, 미회신 추적 누락 가능성, 일관성 유지 어려움

### 1.2 목표

**매일 아침 한 번 실행으로 프로젝트 현황 자동 동기화 및 리포트 생성**

| 목표 | 측정 지표 |
|------|----------|
| 수동 작업 시간 감소 | 30분/일 → 5분/일 |
| 미회신 추적 누락률 | 0% (자동 알림) |
| 데이터 일관성 | 모든 소스 동기화 |

---

## 2. 범위

### 2.1 In-Scope

| 기능 | 설명 | 우선순위 |
|------|------|:--------:|
| **Gmail 동기화** | wsoptv 라벨 이메일 → EMAIL-LOG.md | P0 |
| **Slack 동기화** | 프로젝트 채널 메시지 → SLACK-LOG.md | P0 |
| **Slack Lists 동기화** | 칸반 보드 → VENDOR-DASHBOARD.md | P0 |
| **미회신 알림** | D+3 이상 미회신 → Slack 알림 | P0 |
| **일일 리포트** | 요약 대시보드 생성 → README.md | P1 |
| **액션 아이템 추출** | 의사결정/할일 자동 감지 | P1 |

### 2.2 Out-of-Scope

- Google Calendar 연동
- 자동 이메일 발송 (리마인더)
- 외부 CRM 연동

---

## 3. 기능 상세

### 3.1 아키텍처

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Daily Morning Sync (08:00 KST)                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │  Gmail   │    │  Slack   │    │  Slack   │    │  Local   │          │
│  │   API    │    │ Messages │    │  Lists   │    │   MD     │          │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘          │
│       │               │               │               │                │
│       ▼               ▼               ▼               ▼                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                     Sync Engine (Python)                        │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │   │
│  │  │ gmail_sync  │ │ slack_sync  │ │ lists_sync  │               │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘               │   │
│  │                                                                 │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │   │
│  │  │ dedup_check │ │ decision_   │ │ action_     │               │   │
│  │  │             │ │ detector    │ │ extractor   │               │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                               │                                         │
│                               ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      Output Generator                            │   │
│  │                                                                  │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                │   │
│  │  │ EMAIL-LOG   │ │ SLACK-LOG   │ │ VENDOR-     │                │   │
│  │  │    .md      │ │    .md      │ │ DASHBOARD   │                │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘                │   │
│  │                                                                  │   │
│  │  ┌─────────────┐ ┌─────────────┐                                │   │
│  │  │  README.md  │ │ Slack Alert │                                │   │
│  │  │ (Daily Sum) │ │ (Webhooks)  │                                │   │
│  │  └─────────────┘ └─────────────┘                                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 데이터 흐름

#### 3.2.1 Gmail 동기화

**입력**: Gmail API (`wsoptv` 라벨)
**출력**: `docs/management/EMAIL-LOG.md`

```python
# 업체 매핑 규칙
VENDOR_PATTERNS = {
    "megazone": ["@mz.co.kr", "@megazone.com", "메가존"],
    "brightcove": ["@brightcove.com", "Brightcove"],
    "vimeo": ["@vimeo.com", "Vimeo"],
    "malgeum": ["@malgeum.com", "맑음소프트"],
}

# 미회신 감지 규칙
PENDING_THRESHOLD_DAYS = 3  # D+3 이상 = 미회신
```

**처리 로직**:
1. 최근 7일 wsoptv 라벨 이메일 조회
2. email_id 기반 중복 제거
3. 업체 자동 분류 (발신자/수신자 도메인 매칭)
4. 미회신 상태 계산 (마지막 수신 vs 마지막 발신 비교)
5. EMAIL-LOG.md 업데이트 (신규 항목만 추가)

#### 3.2.2 Slack 메시지 동기화

**입력**: Slack Bot Token (채널: `C09TX3M1J2W`)
**출력**: `docs/management/SLACK-LOG.md`

```python
# 의사결정 감지 패턴
DECISION_PATTERNS = [
    r"확정",
    r"결정",
    r"승인",
    r"동의",
    r"합의",
    r"선정",
]

# 액션 아이템 감지 패턴
ACTION_PATTERNS = [
    r"@\w+.*해주세요",
    r"@\w+.*부탁",
    r"@\w+.*처리",
    r"\[ \]",  # Markdown checkbox
]
```

**처리 로직**:
1. 최근 7일 채널 메시지 조회
2. ts(timestamp) 기반 중복 제거
3. 의사결정/액션 아이템 자동 감지
4. SLACK-LOG.md 업데이트

#### 3.2.3 Slack Lists 동기화

**입력**: Slack User Token (List ID: `F0ACQJS6KND`)
**출력**: `docs/management/VENDOR-DASHBOARD.md`

**컬럼 매핑**:

| Slack Lists 컬럼 | 컬럼 ID | VENDOR-DASHBOARD 필드 |
|------------------|---------|----------------------|
| 업체명 | `Col0ACBLXEU66` | 업체명 |
| 상태 | `Col0ABWF6TEQP` | 상태 |
| 견적 | `Col0ACQRUJ073` | 견적 |
| 최종 연락 | `Col0ACQRVGHKK` | 최종 연락일 |
| 다음 액션 | `Col0ABWF0K4DV` | 후속 조치 |
| 비고 | `Col0ABWF1LL9M` | 비고 |

**상태 옵션 ID 매핑**:

| 상태 | Option ID |
|------|-----------|
| 검토 중 | `OptN4JBLQ9C` |
| 견적 대기 | `Opt2QCAWCYN` |
| 협상 중 | `OptZSZEAEHJ` |
| 보류 | `OptBAAGMVM4` |

### 3.3 미회신 알림

**조건**: 발송 후 3일 이상 회신 없음

**알림 채널**: Slack Webhook → `#wsoptv-alerts` (또는 프로젝트 채널)

**알림 형식**:
```
🔴 [미회신 알림] Brightcove 견적 요청 (D+5)
• 발송일: 2026-01-28
• 제목: WSOPTV OTT Platform 견적 요청
• 권장 조치: 2차 리마인더 발송
```

### 3.4 일일 리포트

**생성 위치**: `docs/management/README.md` "오늘의 요약" 섹션

**리포트 구조**:
```markdown
## 오늘의 요약 (2026-02-02)

### 🔴 긴급 (Action Required)
- [자동 생성] 미회신 항목 목록

### 🟡 주의
- [자동 생성] D+2 경과 항목

### ✅ 완료
- [자동 생성] 최근 24시간 내 완료 항목

### 📊 통계
- 총 이메일: 12건 (수신 8, 발신 4)
- 미회신: 1건
- 의사결정: 2건
- 액션 아이템: 3건 (미완료)
```

---

## 4. 기술 명세

### 4.1 파일 구조

```
C:\claude\wsoptv_ott\
├── scripts/
│   ├── daily_sync.py           # 메인 실행 스크립트
│   ├── sync/
│   │   ├── __init__.py
│   │   ├── gmail_sync.py       # Gmail 동기화
│   │   ├── slack_sync.py       # Slack 메시지 동기화
│   │   ├── lists_sync.py       # Slack Lists 동기화
│   │   └── report_generator.py # 리포트 생성
│   └── config/
│       └── sync_config.yaml    # 설정 파일
├── docs/management/
│   ├── README.md               # 일일 요약 (자동 업데이트)
│   ├── EMAIL-LOG.md            # 이메일 로그 (자동 업데이트)
│   ├── SLACK-LOG.md            # 슬랙 로그 (자동 업데이트)
│   ├── VENDOR-DASHBOARD.md     # 업체 대시보드 (자동 업데이트)
│   └── slack-kanban-config.md  # Slack Lists 설정 (참조)
```

### 4.2 설정 파일

```yaml
# scripts/config/sync_config.yaml

sync:
  gmail:
    label: "wsoptv"
    days: 7
    enabled: true

  slack:
    channel: "C09TX3M1J2W"
    days: 7
    enabled: true

  lists:
    list_id: "F0ACQJS6KND"
    enabled: true

alerts:
  pending_threshold_days: 3
  slack_webhook: "${SLACK_WEBHOOK_URL}"
  enabled: true

output:
  email_log: "docs/management/EMAIL-LOG.md"
  slack_log: "docs/management/SLACK-LOG.md"
  vendor_dashboard: "docs/management/VENDOR-DASHBOARD.md"
  daily_summary: "docs/management/README.md"
```

### 4.3 CLI 인터페이스

```powershell
# 전체 동기화 (기본)
python scripts/daily_sync.py

# 개별 모듈 실행
python scripts/daily_sync.py --gmail      # Gmail만
python scripts/daily_sync.py --slack      # Slack 메시지만
python scripts/daily_sync.py --lists      # Slack Lists만
python scripts/daily_sync.py --report     # 리포트만

# 옵션
python scripts/daily_sync.py --days 14    # 최근 14일
python scripts/daily_sync.py --dry-run    # 미리보기 (변경 없음)
python scripts/daily_sync.py --verbose    # 상세 로그
python scripts/daily_sync.py --no-alert   # 알림 비활성화
```

### 4.4 의존성

```python
# requirements.txt (추가)
google-auth>=2.0.0
google-auth-oauthlib>=1.0.0
google-api-python-client>=2.0.0
slack-sdk>=3.0.0
pyyaml>=6.0.0
```

### 4.5 인증

| 서비스 | 인증 방식 | 토큰 위치 |
|--------|----------|----------|
| Gmail | OAuth 2.0 (Browser) | `C:\claude\json\gmail_token.json` |
| Slack Bot | Bot Token | `C:\claude\json\slack_token.json` |
| Slack Lists | User Token | `C:\claude\json\slack_user_token.json` |

---

## 5. 구현 계획

### 5.1 Phase 1: 기본 동기화 (P0)

| 태스크 | 설명 | 예상 시간 |
|--------|------|----------|
| Gmail Sync 모듈 | wsoptv 라벨 이메일 조회/파싱 | 2시간 |
| Slack Sync 모듈 | 채널 메시지 조회/파싱 | 2시간 |
| Lists Sync 모듈 | Slack Lists 조회/파싱 | 1시간 |
| 중복 제거 로직 | email_id/ts 기반 dedup | 1시간 |
| MD 파일 업데이트 | 마크다운 파싱/생성 | 2시간 |

### 5.2 Phase 2: 알림 및 리포트 (P1)

| 태스크 | 설명 | 예상 시간 |
|--------|------|----------|
| 미회신 감지 | D+N 계산 로직 | 1시간 |
| Slack 알림 | Webhook 연동 | 1시간 |
| 일일 리포트 | README.md 업데이트 | 2시간 |
| 의사결정/액션 감지 | 패턴 매칭 | 2시간 |

### 5.3 Phase 3: 자동화 (P2)

| 태스크 | 설명 | 예상 시간 |
|--------|------|----------|
| Windows Task Scheduler | 매일 08:00 실행 | 1시간 |
| 에러 핸들링 | 재시도/알림 로직 | 1시간 |
| 로깅 | 실행 이력 기록 | 1시간 |

---

## 6. 리스크 및 대응

| 리스크 | 영향 | 확률 | 대응 |
|--------|:----:|:----:|------|
| API Rate Limit | 중 | 낮음 | 지수 백오프 재시도 |
| 토큰 만료 | 높음 | 중간 | 자동 갱신 로직 |
| 파싱 실패 | 중 | 낮음 | 원본 보존, 수동 복구 |
| 네트워크 오류 | 낮음 | 낮음 | 재시도 3회 |

---

## 7. 성공 지표

| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| 동기화 성공률 | ≥ 99% | 실행 로그 분석 |
| 미회신 감지율 | 100% | 수동 크로스체크 |
| 일일 실행 시간 | < 60초 | 실행 시간 측정 |
| 사용자 개입 빈도 | < 1회/주 | 수동 수정 횟수 |

---

## 8. 관련 문서

| 문서 | 경로 | 용도 |
|------|------|------|
| 슬랙 칸반 설정 | [slack-kanban-config.md](../management/slack-kanban-config.md) | API ID 참조 |
| 기존 동기화 스크립트 | `scripts/sync_management.py` | 참조용 |
| Slack 라이브러리 | `C:\claude\lib\slack\` | API 클라이언트 |
| Gmail 라이브러리 | `C:\claude\lib\gmail\` | API 클라이언트 |

---

## Revision History

| 버전 | 날짜 | 작성자 | 내용 |
|------|------|--------|------|
| 1.0.0 | 2026-02-02 | Claude Code | 최초 작성 |
