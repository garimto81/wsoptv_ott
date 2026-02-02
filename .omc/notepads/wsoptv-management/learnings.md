# WSOPTV 프로젝트 관리 시스템 - Learnings

**Created**: 2026-02-02
**Last Updated**: 2026-02-02

---

## 기술적 발견

### 1. Gmail/Slack 라이브러리 위치 및 인증
- **위치**: `C:\claude\lib\gmail\`, `C:\claude\lib\slack\`
- **인증 방식**: OAuth 2.0 (Browser 기반)
- Gmail 인증 계정: `aiden.kim@ggproduction.net`
- Slack 워크스페이스: `GGProduction`
- Slack Bot User ID: `U080DDS8AQ7`

### 2. Gmail wsoptv 라벨 사용
- Gmail에서 `label:wsoptv`로 필터링하여 업체 이메일 관리
- 업체별 이메일 주소 추적 가능

### 3. Slack 채널 정보
- 채널 ID: `C09TX3M1J2W`
- 채널명: `wsoptv` (WSOPTV 프로젝트 전용 채널)
- ggpnotice 앱으로 메시지 처리

### 4. 패턴 감지 시스템
- **의사결정 키워드**: "확정", "결정", "동의합니다", "합의", "승인", "채택"
- **액션 아이템 패턴**: `@멘션 + YYYY-MM-DD`, `담당.*:.*@멘션`, `@멘션.*검토/확인/업데이트`
- ts(timestamp) 기반 중복 방지

### 5. Windows 인코딩 이슈
- Console 출력 시 cp949 인코딩 에러 발생 (특수문자 • 등)
- 파일 쓰기는 UTF-8로 정상 작동
- Rich Console과 sys.stdout 래핑 충돌 → 수정 시도 후 롤백
- **결론**: 파일 쓰기는 문제없으며, 콘솔 표시만 이슈 (수용 가능)

---

## 구현 패턴

### Markdown 기반 관리 시스템
- 모든 로그는 `docs/management/*.md` 파일로 관리
- HTML 코멘트로 메타데이터 저장: `<!-- ts: 1706824200.123456 -->`
- 최신순 정렬로 데이터 삽입

### CLI 명령어 체계
```powershell
# 전체 동기화
python scripts/sync_management.py sync

# Slack만 (최근 7일)
python scripts/sync_management.py sync --slack --days 7

# Gmail만 (wsoptv 라벨)
python scripts/sync_management.py sync --gmail

# Dry-run (미리보기)
python scripts/sync_management.py sync --dry-run

# 상태 확인
python scripts/sync_management.py status
```

---

## 업체 정보

| 업체 | 역할 | 이메일 도메인 | 상태 |
|------|------|--------------|------|
| 메가존 | OVP 총판 | @megazone.com | 견적 수령 (48억) |
| Brightcove | 글로벌 OVP | @brightcove.com | 견적 대기 (D+5) |
| Vimeo | 글로벌 OVP | @vimeo.com | 미팅 완료 |
| 맑음소프트 | 국내 OVP | @malgum.com | 미팅 완료 |

---

## 파일 구조

```
docs/management/
├── README.md              # 관리 시스템 인덱스
├── EMAIL-LOG.md           # 업체별 이메일 로그
├── SLACK-LOG.md           # 슬랙 의사결정/액션 로그
├── VENDOR-DASHBOARD.md    # 업체 평가 대시보드
└── DOCUMENT-TRACKER.md    # 기획 문서 추적기

scripts/sync/
├── __init__.py            # 패키지 초기화
├── models.py              # 데이터 모델 정의
├── slack_sync.py          # Slack 동기화 구현
├── gmail_sync.py          # Gmail 동기화 (placeholder)
├── markdown_parser.py     # MD 파싱 유틸리티
└── pattern_detector.py    # 패턴 감지 클래스

scripts/
└── sync_management.py     # 메인 CLI 엔트리포인트
```
