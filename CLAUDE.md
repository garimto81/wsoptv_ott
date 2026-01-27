# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 프로젝트 개요

**WSOPTV OTT Platform** - WSOP(World Series of Poker) 공식 OTT 스트리밍 플랫폼

**현재 단계**: 기획/문서화 (코드 개발 전)

### 핵심 기능 (계획)

- 5개 플랫폼 (Web, iOS, Android, Samsung TV, LG TV)
- 라이브 스트리밍, VOD, Timeshift
- Advanced Mode (3계층 Multi-view, StatsView)
- GGPass SSO 연동

---

## 명령어

### 목업 스크린샷 캡처

```powershell
npx playwright screenshot docs/mockups/PRD-0002/feature-name.html docs/images/PRD-0002/feature-name.png
```

### Google Slides API (NBA TV 레퍼런스 분석용)

```powershell
python C:\claude\wsoptv_ott\scripts\read_google_slides.py
```

---

## 문서 체계

**메인 인덱스**: [docs/README.md](docs/README.md)

### Tier 1 핵심 문서

| 문서 | 역할 |
|------|------|
| [STRAT-0001](docs/strategies/STRAT-0001-viewer-experience-vision.md) | 시청자 경험 비전 (Vision) |
| [PRD-0002](docs/prds/PRD-0002-wsoptv-concept-paper.md) | Concept Paper |
| [PRD-0006](docs/prds/PRD-0006-advanced-mode.md) | Advanced Mode 상세 |
| [STRAT-0007](docs/strategies/STRAT-0007-content-sourcing.md) | 콘텐츠 소싱 전략 |

### 문서 명명 규칙

| 유형 | 접두사 | 예시 |
|------|--------|------|
| PRD | `PRD-NNNN` | `PRD-0002-wsoptv-concept-paper.md` |
| ADR | `ADR-NNNN` | `ADR-0001-multiview-3layer-rationale.md` |
| Strategy | `STRAT-NNNN` | `STRAT-0001-viewer-experience-vision.md` |

### 목업/이미지 위치

```
docs/mockups/[문서ID]/*.html   # HTML 목업
docs/images/[문서ID]/*.png     # 스크린샷
```

---

## DB 스키마

`scripts/db/` - PostgreSQL 스키마 (Supabase 대상)

- `001_initial_schema.sql`: 핵심 테이블 (series, tournaments, events, players)
- `002_additional_tables_and_constraints.sql`: 추가 테이블

**설계 문서**: [ADR-0002](docs/adrs/ADR-0002-database-schema-design.md)

---

## Google Docs Reference

| 문서 | Google Docs ID | 버전 | 동기화 날짜 |
|------|----------------|------|-------------|
| **PRD-0002** | `1Y5KMRFunHJEXmR0MrXbb_flmf-_88obGnJBe0AC94_A` | v8.5 | 2026-01-27 |

로컬 PRD: `docs/prds/PRD-0002-wsoptv-concept-paper.md`

---

## 상위 규칙 상속

`C:\claude\CLAUDE.md` 규칙 적용:

- 언어: 한글 출력, 기술 용어 영어 유지
- 경로: 절대 경로 (`C:\claude\wsoptv_ott\...`)
- Git: Conventional Commit
