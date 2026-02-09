# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 프로젝트 개요

WSOP(World Series of Poker) 공식 OTT 스트리밍 플랫폼 프로젝트. 현재 기획/문서화 단계이며, Python 기반 관리 자동화 시스템을 포함한다.

- **목표**: Q3 2026 WSOPTV 론칭 (Vimeo SaaS 기반)
- **Phase 0**: 비전/비즈니스 전략 (완료)
- **Phase 1**: MVP 스펙 - Vimeo 기반 OTT (진행 중)
- **Phase 2+**: Advanced Mode, Multi-view (계획)

---

## 빌드 및 실행

### 동기화 CLI

```powershell
# 통합 CLI (Typer)
python C:\claude\wsoptv_ott\scripts\sync_management.py sync             # Gmail + Slack 동기화
python C:\claude\wsoptv_ott\scripts\sync_management.py sync --gmail     # Gmail만
python C:\claude\wsoptv_ott\scripts\sync_management.py sync --slack     # Slack만
python C:\claude\wsoptv_ott\scripts\sync_management.py sync --dry-run   # 미리보기

# 일일 동기화 (Slack Lists 포함)
python C:\claude\wsoptv_ott\scripts\daily_sync.py                       # 전체 동기화
python C:\claude\wsoptv_ott\scripts\daily_sync.py --init                # 초기화 (365일)
python C:\claude\wsoptv_ott\scripts\daily_sync.py --slack               # Slack만
python C:\claude\wsoptv_ott\scripts\daily_sync.py --lists               # Slack Lists만
python C:\claude\wsoptv_ott\scripts\daily_sync.py --dry-run             # 미리보기
```

### Vimeo POC

```powershell
python C:\claude\wsoptv_ott\scripts\vimeo\upload_poc.py test.mp4        # 업로드 테스트
python C:\claude\wsoptv_ott\scripts\vimeo\upload_poc.py --list          # 비디오 목록
```

### 목업 스크린샷

```powershell
npx playwright screenshot docs/mockups/PRD-0002/feature.html docs/images/PRD-0002/feature.png
```

### 의존성

typer, rich (CLI/터미널 UI). 별도 requirements.txt 없이 직접 import.

---

## 아키텍처

### 멀티노드 역할 분리

동시 세션 충돌 방지를 위해 두 노드 역할이 분리되어 있다. `.omc/NODE_ROLES.md` 참조.

| 노드 | 담당 영역 | 수정 가능 |
|------|----------|----------|
| **Docs Node** | 기획, 전략, PRD | `docs/phase0/`, `docs/phase1/`, `docs/mockups/` |
| **Sync Node** | 스크립트, 자동화 | `scripts/`, `docs/management/` |

각 노드는 상대 영역을 읽기만 가능하며 수정하지 않는다. 상태 파일은 `.omc/nodes/`에 저장된다.

### 동기화 파이프라인

```
Gmail (wsoptv 라벨) + Slack (#wsoptv) + Slack Lists
        ↓ (패턴 감지: 의사결정, 액션 아이템, 견적)
scripts/sync/ 모듈
        ↓ (마크다운 포맷)
docs/management/
├── SLACK-LOG.md           # Slack 의사결정 + 액션 항목
├── EMAIL-LOG.md           # Gmail 로그
└── VENDOR-DASHBOARD.md    # Slack Lists 업체 관리
```

### 동기화 모듈 구조 (`scripts/sync/`)

| 모듈 | 역할 |
|------|------|
| `models.py` | 데이터 모델 (EmailLogEntry, SlackDecision, SyncResult) |
| `slack_sync.py` | Slack 채널 → SLACK-LOG.md |
| `gmail_sync.py` | Gmail → EMAIL-LOG.md |
| `lists_sync.py` / `lists_sync_v2.py` | Slack Lists → VENDOR-DASHBOARD.md |
| `analyzers/` | 의사결정 감지, 상태 추론 |
| `parsers/` | PDF, Excel 파싱 |
| `extractors/` | 견적 추출 |
| `formatters/` | 마크다운 포맷팅 |
| `collectors/` | 첨부파일 다운로드 |

### 설정 파일

| 파일 | 역할 |
|------|------|
| `wsoptv_sync_config.yaml` | 업체 정보, Slack Lists 컬럼 매핑, 상태 전이 규칙 |
| `.project-sync.yaml` | `/auto --daily` 실행 시 daily-sync 스킬 자동 라우팅 |

### 상태 자동 전이 규칙 (`wsoptv_sync_config.yaml`)

업체 상태는 Slack/Gmail 패턴에 의해 자동 변경된다:
- 양방향 통신 감지 → "협상 중"으로 승격 (auto)
- 견적 수령 → "검토 중"으로 변경 (auto)
- 부정 상태 변경(제외, 보류) → 수동 승인 필요

---

## 문서 체계

### Phase별 핵심 문서

| 문서 | 위치 | 역할 |
|------|------|------|
| Vision | `docs/phase0/01-vision.md` | 용어 정의, 기능, 플랫폼 요구사항 |
| Business | `docs/phase0/02-business.md` | GG 생태계 전략, 구독 모델 |
| Vendor RFP | `docs/phase0/03-vendor-rfp.md` | 업체 평가 매트릭스 |
| MVP Spec | `docs/phase1/01-mvp-spec.md` | Vimeo 기반 NBA TV 스타일 UX |
| Content | `docs/phase1/02-content.md` | 콘텐츠 소싱 전략 |

### 자동 생성 문서 (`docs/management/`)

Sync 스크립트가 자동 생성/갱신하는 파일. 직접 수정하지 않는다.

---

## 프로젝트 규칙

- **경로**: 절대 경로만 사용 (`C:\claude\wsoptv_ott\...`)
- **언어**: 한글 출력, 기술 용어는 영어 유지
- **API 키**: 환경변수 직접 설정 금지, Browser OAuth만 사용
- **커밋 접두사**: 노드 식별 — `[docs] feat:`, `[sync] fix:` 형식
- **.claude/**: Junction 링크 (Global-Only Policy) — `C:\claude\.claude\`의 중앙 리소스를 참조
