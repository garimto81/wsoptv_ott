# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 프로젝트 개요

**WSOPTV OTT Platform** - WSOP(World Series of Poker) 공식 OTT 스트리밍 플랫폼

**현재 단계**: 기획/문서화 (코드 개발 전)

### 핵심 차별점 (vs YouTube)

| 기능 | YouTube | WSOPTV |
|------|---------|--------|
| **Timeshift** | 불가 | 라이브 중 되감기 |
| **아카이브** | 비공개 | 영구 보존 |
| **Advanced Mode** | 없음 | Multi-view + StatsView |
| **검색** | 없음 | 핸드/선수 기반 검색 |

---

## 명령어

### 목업 스크린샷 캡처

```powershell
# 최초 설치 (1회)
npx playwright install chromium

# 개별 목업 캡처
npx playwright screenshot docs/mockups/PRD-0002/feature-name.html docs/images/PRD-0002/feature-name.png

# 여러 목업 일괄 캡처 예시
npx playwright screenshot docs/mockups/PRD-0006/multiview-3layer.html docs/images/PRD-0006/multiview-3layer.png
```

### Google API 스크립트

```powershell
# Google Slides 읽기 (NBA TV 레퍼런스)
python C:\claude\wsoptv_ott\scripts\read_google_slides.py

# Google Slides 쓰기
python C:\claude\wsoptv_ott\scripts\write_google_slides.py

# 흑백 와이어프레임 생성
python C:\claude\wsoptv_ott\scripts\wsoptv_bw_wireframe.py
```

> **인증**: Google OAuth (Browser 기반). `C:\claude\json\desktop_credentials.json` 필요.

---

## 문서 체계

### 문서 계층 구조

```
            ┌─────────────────────────────┐
            │    STRAT-0001 (Vision)      │  ← 시청자 경험 비전
            └──────────────┬──────────────┘
                           │
       ┌───────────────────┼───────────────────┐
       ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  PRD-0002   │◀───│  PRD-0006   │    │ STRAT-0007  │
│ Concept     │    │ Advanced    │    │ Content     │
│ Paper       │    │ Mode        │    │ Sourcing    │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Tier 1 핵심 문서

| 문서 | 역할 | 파일 |
|------|------|------|
| **STRAT-0001** | 시청자 경험 비전 | `docs/strategies/STRAT-0001-viewer-experience-vision.md` |
| **PRD-0002** | Concept Paper (Google Docs 동기화) | `docs/prds/PRD-0002-wsoptv-concept-paper.md` |
| **PRD-0002-executive-summary** | 경영진 보고용 요약 | `docs/prds/PRD-0002-executive-summary.md` |
| **PRD-0006** | Advanced Mode 4-layer | `docs/prds/PRD-0006-advanced-mode.md` |
| **STRAT-0007** | 콘텐츠 소싱 전략 | `docs/strategies/STRAT-0007-content-sourcing.md` |

### 메인 인덱스

`docs/README.md` - 전체 문서 목록 및 상태 관리

---

## 목업 워크플로우

### 디렉토리 구조

```
docs/mockups/PRD-NNNN/*.html   # HTML 목업 소스
docs/images/PRD-NNNN/*.png     # 캡처된 스크린샷
```

### 주요 목업 (PRD-0002)

| 목업 | 설명 |
|------|------|
| `01-three-pillars.html` | 4대 원천 다이어그램 |
| `04-multiview.html` | Multi-view 레이아웃 |
| `16-ovp-stream-architecture.html` | OVP/STREAM 이원화 아키텍처 |
| `27-streaming-architecture-v7.html` | Video Streaming Architecture v7 |

### 주요 목업 (PRD-0006)

| 목업 | 설명 |
|------|------|
| `multiview-3layer.html` | 3계층 Multi-view |
| `statsview-hud.html` | StatsView HUD 오버레이 |
| `4layer-standard.html` | 4계층 레이아웃 |

---

## DB 스키마

**위치**: `scripts/db/`

| 파일 | 내용 |
|------|------|
| `001_initial_schema.sql` | 핵심 테이블 (series, tournaments, events, players) |
| `002_additional_tables_and_constraints.sql` | 추가 테이블 및 제약조건 |

**설계 문서**: `docs/adrs/ADR-0002-database-schema-design.md`

---

## Google Docs 동기화

| 문서 | Google Docs ID | 버전 |
|------|----------------|------|
| **PRD-0002** (Concept Paper) | `1Y5KMRFunHJEXmR0MrXbb_flmf-_88obGnJBe0AC94_A` | v9.1 |
| **PRD-0002-executive-summary** | `1Y_GmF6AYOEkj7TEX3CptimlFVDEGZdssRysdzXHIQDs` | v6.1 |

**동기화 방법**: Google Docs 변경 시 로컬 PRD 수동 업데이트

**URL**:
- PRD-0002: https://docs.google.com/document/d/1Y5KMRFunHJEXmR0MrXbb_flmf-_88obGnJBe0AC94_A/edit
- Executive Summary: https://docs.google.com/document/d/1Y_GmF6AYOEkj7TEX3CptimlFVDEGZdssRysdzXHIQDs/edit

---

## 문서 명명 규칙

| 유형 | 접두사 | 예시 |
|------|--------|------|
| PRD | `PRD-NNNN` | `PRD-0002-wsoptv-concept-paper.md` |
| ADR | `ADR-NNNN` | `ADR-0001-multiview-3layer-rationale.md` |
| Strategy | `STRAT-NNNN` | `STRAT-0001-viewer-experience-vision.md` |
| Report | `REPORT-YYYY-MM-DD` | `REPORT-2026-01-19-nbatv-reference-analysis.md` |

---

## 상위 규칙 상속

`C:\claude\CLAUDE.md` 규칙 적용:

- 언어: 한글 출력, 기술 용어 영어 유지
- 경로: 절대 경로 (`C:\claude\wsoptv_ott\...`)
- Git: Conventional Commit
