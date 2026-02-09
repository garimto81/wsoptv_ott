# Slack Kanban Board 설정

**생성일**: 2026-02-02
**Workspace**: GGProduction
**List ID**: `F0ACQJS6KND`
**프로젝트 채널**: `C09TX3M1J2W`
**자동화 상태**: ✅ User Token 설정 완료

## User Token 설정 가이드

Slack Lists API(`lists:read`, `lists:write`)는 **User Token Scopes**에만 존재합니다.
자동화를 위해서는 User Token 발급이 필요합니다.

### Step 1: Slack App 설정

1. https://api.slack.com/apps 접속
2. 해당 앱 선택 → **OAuth & Permissions**
3. **User Token Scopes** 섹션에 추가:
   - `lists:read`
   - `lists:write`
4. **Reinstall to Workspace** 클릭

### Step 2: User Token 발급

```powershell
# Slack App에 client_id, client_secret 설정 필요
# C:\claude\json\slack_credentials.json에 추가:
# {
#   "client_id": "your-client-id",
#   "client_secret": "your-client-secret"
# }

# User Token 포함 로그인
cd C:\claude && python -m lib.slack login --user
```

### Step 3: Slack Lists 자동화

```python
from lib.slack import SlackUserClient

client = SlackUserClient()  # User Token 사용
result = client.create_list("WSOPTV 업체 관리", "업체 선정 프로세스")
```

---

## 수동 생성 방법 (User Token 없이)

## 수동 생성 방법

1. **Slack 열기**
2. 좌측 사이드바 → **Lists** 탭 클릭
3. **+ Create list** → 이름: "WSOPTV 업체 관리"
4. 컬럼 추가:
   - 업체명 (Text, Primary)
   - 상태 (Select)
   - 견적 (Text)
   - 비고 (Text)
5. 상태 옵션 설정:
   - RFP 발송 (blue)
   - 견적 대기 (yellow)
   - 평가 중 (orange)
   - 협상 중 (green)
   - 완료 (green)
   - 제외 (red)
6. 우측 상단 필터 아이콘 → **Layout** → **Board** 선택

## 칸반 컬럼 (상태)

| 상태 | 의미 | 옵션 ID |
|------|------|---------|
| **검토 중** | 내부 검토 진행 중 | `OptN4JBLQ9C` |
| **견적 대기** | 견적서 회신 대기 중 | `Opt2QCAWCYN` |
| **협상 중** | 우선협상대상 선정, 계약 협상 | `OptZSZEAEHJ` |
| **보류** | 진행 보류, 추후 검토 | `OptBAAGMVM4` |

## 컬럼 ID 참조

| 컬럼 | 컬럼 ID | 타입 |
|------|---------|------|
| 업체명 | `Col0ACBLXEU66` | Text |
| 상태 | `Col0ABWF6TEQP` | Select |
| 견적 | `Col0ACQRUJ073` | Text |
| 최종 연락 | `Col0ACQRVGHKK` | Date |
| 다음 액션 | `Col0ABWF0K4DV` | Text |
| 비고 | `Col0ABWF1LL9M` | Text |

## 아이템 ID 참조

| 업체 | 아이템 ID |
|------|----------|
| 메가존클라우드 | `Rec0AC9KQD7TQ` |
| 맑음소프트 | `Rec0ACBM3P1PC` |
| Brightcove | `Rec0AC9KQQEDC` |
| Vimeo OTT | `Rec0ACQJY2W65` |

## 첨부 파일 참조

| 업체 | 파일명 | 파일 ID | 날짜 |
|------|--------|---------|------|
| 맑음소프트 | `맑음소프트_WSOPTV 견적 제안_ver1.0.pdf` | `F0AABGL8X40` | 2026-01-19 |

### 맑음소프트 견적 상세 (F0AABGL8X40)

**총 견적: 3억 7,400만원** (부가세 별도)

| 단계 | 금액 | 기간 | 투입 인력 |
|------|------|------|----------|
| **컨설팅** | 6,600만원 | 2개월 | 3인 |
| **서비스 구축** | 3억 800만원 | 4개월 | 맑음소프트 + 코드팩 협업 |
| **합계** | 3억 7,400만원 | 6개월 | - |

**구축 범위:**
- OTT 플랫폼 설계 및 개발
- Multi-view 기능 지원
- 맑음소프트 + 코드팩 공동 수행

## 현재 업체 데이터 (2026-02-02)

| 업체 | 상태 | 견적 | 최종 연락 | 다음 액션 | 비고 |
|------|------|------|----------|----------|------|
| 메가존클라우드 | 협상 중 | 48억+15억/년 | 01-30 | SLA 협상 (02-08) | Multi-view, Timeshift, 통합SI 지원 |
| 맑음소프트 | 검토 중 | 3.74억 (컨설팅+구축, 6개월) | 01-19 | 내부 검토 | Multi-view 지원, 코드팩 협업 |
| Brightcove | 견적 대기 | 미수령 | 01-30 | Follow-up (D+5) | Multi-view 커스텀 개발 필요 |
| Vimeo OTT | 보류 | - | 01-30 | 회신 대기 | 준비 부족 우려 전달, 개선 요청 |

## 동기화 정책

- **Slack Lists ↔ VENDOR-DASHBOARD.md**: 수동 동기화
- 주요 변경 발생 시 양쪽 모두 업데이트 필요
- 일일 점검 시 불일치 확인

## Pinned Summary Message

| 항목 | 값 |
|------|-----|
| **Channel** | `C09TX3M1J2W` |
| **Message TS** | `1770011097.422069` |
| **역할** | 업체 현황 자동 업데이트용 고정 메시지 |

> `daily_sync.py --post-summary` 실행 시 이 메시지가 업데이트됩니다.

## 관련 문서

- [VENDOR-DASHBOARD.md](./VENDOR-DASHBOARD.md) - 상세 업체 정보
- [EMAIL-LOG.md](./EMAIL-LOG.md) - 이메일 커뮤니케이션
- [SLACK-LOG.md](./SLACK-LOG.md) - 의사결정 기록
