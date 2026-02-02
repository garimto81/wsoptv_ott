# WSOPTV OTT 문서 인덱스

**Version**: 6.1.0
**Last Updated**: 2026-02-02
**Major Update**: 프로젝트 관리 시스템 추가 (메일/슬랙/업체/기획 관리)

---

## 문서 계층 구조

```
                    ┌─────────────────────────────┐
                    │         Vible (원천)         │
                    │  michael_note + tony_note   │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │    STRAT-0001 ★ (Vision)    │
                    │   시청자 경험 비전            │
                    └──────────────┬──────────────┘
                                   │
    ┌──────────────────────────────┼──────────────────────────────┐
    │                              │                              │
    ▼                              ▼                              ▼
┌────────────┐              ┌────────────┐              ┌────────────┐
│ STRAT-0009 │              │ PRD-0002 ★ │              │ TECH-0001  │
│ 비즈니스   │─────────────▶│ 앱 기획서  │◀─────────────│ 기술 인프라│
│ 전략       │              └──────┬─────┘              └────────────┘
└────────────┘                     │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
             ┌────────────┐ ┌────────────┐ ┌────────────┐
             │ PRD-0006 ★ │ │ Exec.Sum   │ │ STRAT-0007 │
             │ Advanced   │ │ 경영진용   │ │ Content    │
             └────────────┘ └────────────┘ └────────────┘

★ = Tier 1 핵심 문서 (반드시 최신 유지)
```

---

## Tier 1: 핵심 문서 (7개)

반드시 최신 상태로 유지해야 하는 문서

| 문서 | 역할 | 상태 |
|------|------|:----:|
| [STRAT-0001](strategies/STRAT-0001-viewer-experience-vision.md) | **Vision** - 시청자 경험 비전 | Active |
| [PRD-0002](prds/PRD-0002-wsoptv-concept-paper.md) | **Concept Paper** - 앱 기획서 (v10.0) | Active |
| [PRD-0002-executive-summary](prds/PRD-0002-executive-summary.md) | **Executive Summary** - 경영진 보고용 (v6.4) | Active |
| [PRD-0006](prds/PRD-0006-advanced-mode.md) | **Feature** - Advanced Mode (4-layer) | Active |
| [STRAT-0007](strategies/STRAT-0007-content-sourcing.md) | **Content** - 콘텐츠 소싱 | Active |
| [STRAT-0009](strategies/STRAT-0009-gg-ecosystem-strategy.md) | **Business** - GG 생태계 비즈니스 전략 | Active |
| [TECH-0001](tech/TECH-0001-streaming-infrastructure.md) | **Tech** - Streaming 기술 인프라 | Active |
| [TECH-0002](tech/TECH-0002-production-vs-wsoptv-scope.md) | **Tech** - 프로덕션 vs WSOPTV 영역 구분 ⭐ NEW | Draft |

### YouTube 대비 핵심 차별점 (STRAT-0001)

| # | 차별점 | YouTube | WSOPTV |
|:-:|--------|---------|--------|
| 1 | **Timeshift** | 불가 | 라이브 중 되감기 |
| 2 | **아카이브** | 비공개 | 영구 보존 |
| 3 | **Advanced Mode** | 없음 | Player Cam + StatsView (VIBLE 확정) |
| 4 | **검색** (Phase 2) | 없음 | 핸드/선수 검색 |

### 용어 재정의 (v10.1)

| 용어 | 정의 | 출처 | 상태 |
|------|------|:----:|:----:|
| **Selected View** | 사용자가 원하는 테이블/스트림을 **직접 선택**하여 시청 (기본 인터랙션) | 일반 OTT | ✅ 확정 |
| **Player Cam** | 한 테이블의 메인 방송 + 각 플레이어 직캠 (아이돌 직캠) | 📜 VIBLE | ✅ 확정 |
| **Table Multi-view** | 서로 다른 테이블 동시 시청 (2x2 그리드) | 📋 MOSES | ✅ 확정 |
| **StatsView** | 플레이어 통계가 표시된 **영상** (View Mode) | 📜 VIBLE | ✅ 확정 |

> **⚠️ 주의**: VIBLE 원문의 "Multi-view"는 현재 문서의 "Player Cam"에 해당합니다.

---

## Tier 2: 보조 문서 (7개)

필요 시 참조하는 문서

| 문서 | 역할 | 상태 |
|------|------|:----:|
| [PRD-0005](prds/PRD-0005-wsoptv-ott-rfp.md) | RFP 문서 | Active |
| [PRD-0009](prds/PRD-0009-hand-tagging-search.md) | Hand Tagging (Phase 2) | Draft |
| [PRD-0010](prds/PRD-0010-nbatv-ux-solutions.md) | NBA TV UX 솔루션 적용 | Draft |
| [PRD-0011](prds/PRD-0011-daily-management-automation.md) | **일일 관리 자동화** ⭐ NEW | Draft |
| [ADR-0001](adrs/ADR-0001-multiview-3layer-rationale.md) | Multi-view 설계 근거 | Draft |
| [ADR-0002](adrs/ADR-0002-database-schema-design.md) | DB 스키마 설계 | Proposed |
| [STRAT-0003](strategies/STRAT-0003-cross-promotion.md) | 프로모션 전략 | Proposal |
| [STRAT-0008](strategies/STRAT-0008-content-sourcing-architecture.md) | 콘텐츠 소싱 아키텍처 | Draft |

---

## Tier 3: 참조 문서 (4개)

읽기 전용 원천 자료

| 문서 | 역할 |
|------|------|
| [michael_note.md](vible/michael_note.md) | Michael 아이디어 원본 (Vible) |
| [tony_note.md](vible/tony_note.md) | Tony 아이디어 원본 (Moses Commentary) |
| [NBA TV 분석](reports/REPORT-2026-01-19-nbatv-reference-analysis.md) | UX 참조 (4분할 Multi-view) |
| [NFL/MLB/ESPN+ 분석](reports/REPORT-2026-02-02-nfl-mlb-ott-reference.md) | OTT 가격/기능 벤치마크 ⭐ NEW |

---

## 문서 관리 원칙

1. **단일 진실 소스**: STRAT-0001이 시청자 관점의 유일한 진실
2. **계층 준수**: Tier 1 → Tier 2 → Tier 3 순서로 참조
3. **통합 우선**: 신규 문서보다 기존 문서 통합 선호
4. **아카이브 활용**: 불필요한 문서는 즉시 archive/로 이동

---

## 아카이브 (8개)

초기 기획 단계에서 과도하게 상세화된 문서들

| 문서 | 사유 |
|------|------|
| PRD-0006-advanced-mode-v4-3layer | 4-layer로 대체됨 |
| PRD-0002-ascii-archive | ASCII 다이어그램 백업 |
| STRAT-0009~0011 | 타임라인/KPI/법규/API 미확정 |
| ADR-0003 | 기술 스택 미확정 |
| PRD-0008 | UX 방향 미확정 |
| REPORT-strategy | 전략 재검토 필요 |

**위치**: [archive/](archive/)

---

## 프로젝트 관리 시스템 ★ NEW

프로젝트 진행 상태를 추적하고 관리하는 시스템

| 시스템 | 파일 | 용도 |
|--------|------|------|
| 📧 메일 관리 | [EMAIL-LOG.md](management/EMAIL-LOG.md) | 업체별 이메일 커뮤니케이션 추적 |
| 💬 슬랙 관리 | [SLACK-LOG.md](management/SLACK-LOG.md) | 의사결정/액션 아이템 추적 |
| 🏢 업체 관리 | [VENDOR-DASHBOARD.md](management/VENDOR-DASHBOARD.md) | RFP 진행 상태/평가 대시보드 |
| 📄 기획 관리 | [DOCUMENT-TRACKER.md](management/DOCUMENT-TRACKER.md) | 문서 버전/동기화 관리 |

**인덱스**: [management/README.md](management/README.md)

---

## 폴더 구조

```
docs/
├── README.md                    # 이 문서
├── vible/                       # 원천 자료
│   ├── michael_note.md
│   └── tony_note.md
├── strategies/                  # 전략 문서
│   ├── STRAT-0001-viewer-experience-vision.md  ★
│   ├── STRAT-0003-cross-promotion.md
│   ├── STRAT-0007-content-sourcing.md
│   ├── STRAT-0008-content-sourcing-architecture.md
│   └── STRAT-0009-gg-ecosystem-strategy.md     ★ NEW (PRD-0002에서 분리)
├── tech/                        # 기술 문서 (NEW)
│   └── TECH-0001-streaming-infrastructure.md   ★ NEW (PRD-0002에서 분리)
├── prds/                        # PRD
│   ├── PRD-0002-wsoptv-concept-paper.md        ★ v10.0
│   ├── PRD-0002-executive-summary.md           ★ v6.4
│   ├── PRD-0005-wsoptv-ott-rfp.md
│   ├── PRD-0006-advanced-mode.md               ★ (4-layer)
│   ├── PRD-0009-hand-tagging-search.md
│   └── PRD-0010-nbatv-ux-solutions.md
├── adrs/                        # ADR
│   ├── ADR-0001-multiview-3layer-rationale.md
│   └── ADR-0002-database-schema-design.md
├── reports/                     # 리포트
├── templates/                   # 템플릿
│   ├── vendor-evaluation-matrix.md
│   └── rfp-feedback-request-templates.md
├── management/                  # 프로젝트 관리 시스템 ★ NEW
│   ├── README.md                # 관리 시스템 인덱스
│   ├── EMAIL-LOG.md             # 메일 관리
│   ├── SLACK-LOG.md             # 슬랙 관리
│   ├── VENDOR-DASHBOARD.md      # 업체 관리 대시보드
│   └── DOCUMENT-TRACKER.md      # 기획 문서 추적기
├── archive/                     # 아카이브
├── images/                      # 이미지
└── mockups/                     # HTML 목업
```

---

## 명명 규칙

| 유형 | 접두사 | 예시 |
|------|--------|------|
| PRD | `PRD-NNNN` | PRD-0002-wsoptv-ott-platform-mvp.md |
| ADR | `ADR-NNNN` | ADR-0001-multiview-3layer-rationale.md |
| Strategy | `STRAT-NNNN` | STRAT-0001-viewer-experience-vision.md |
| Report | `REPORT-YYYY-MM-DD` | REPORT-2026-01-19-nbatv-reference-analysis.md |

---

*Last Updated: 2026-02-02 (프로젝트 관리 시스템 추가)*
