# WSOPTV OTT Platform

**WSOP(World Series of Poker) 공식 OTT 스트리밍 플랫폼**

---

## 프로젝트 현황

| 항목 | 상태 |
|------|------|
| **단계** | 기획/문서화 (코드 개발 전) |
| **PRD 버전** | v8.6 |
| **문서 수** | 12개 (Tier 1: 5개, Tier 2: 7개) |

---

## 핵심 기능 (계획)

### Phase 1: MVP
- **5개 플랫폼**: Web, iOS, Android, Samsung TV, LG TV
- **라이브 스트리밍**: WSOP 이벤트 실시간 중계
- **VOD**: 완료된 이벤트 다시보기
- **Timeshift**: 라이브 중 되감기/건너뛰기

### Phase 2: Advanced
- **Advanced Mode**: 3계층 Multi-view (Table Strip → PGM → PlayerCAM)
- **StatsView**: 실시간 통계 오버레이
- **Hand Search**: 특정 핸드/선수 검색

---

## 문서 구조

```
docs/
├── README.md                    # 문서 인덱스
├── vible/                       # 원천 자료
├── strategies/                  # 전략 문서 (STRAT-*)
├── prds/                        # 제품 요구사항 (PRD-*)
├── adrs/                        # 설계 결정 (ADR-*)
├── reports/                     # 분석 리포트
├── mockups/                     # HTML 목업
├── images/                      # 스크린샷
└── archive/                     # 아카이브
```

**상세 인덱스**: [docs/README.md](docs/README.md)

---

## 핵심 문서 (Tier 1)

| 문서 | 역할 |
|------|------|
| [STRAT-0001](docs/strategies/STRAT-0001-viewer-experience-vision.md) | 시청자 경험 비전 |
| [PRD-0002](docs/prds/PRD-0002-wsoptv-concept-paper.md) | 플랫폼 Concept Paper |
| [PRD-0002-executive-summary](docs/prds/PRD-0002-executive-summary.md) | 경영진 보고용 요약 |
| [PRD-0006](docs/prds/PRD-0006-advanced-mode.md) | Advanced Mode (4-layer) |
| [STRAT-0007](docs/strategies/STRAT-0007-content-sourcing.md) | 콘텐츠 소싱 전략 |

---

## 기술 스택 (예정)

| 영역 | 기술 |
|------|------|
| Backend | TBD |
| Frontend | TBD |
| Streaming | LiveU Cloud, SRT/HLS |
| Database | PostgreSQL (Supabase) |
| Auth | GGPass SSO |

---

## 빠른 참조

### 목업 스크린샷 캡처
```powershell
npx playwright screenshot docs/mockups/PRD-0002/feature.html docs/images/PRD-0002/feature.png
```

### DB 스키마 위치
```
scripts/db/001_initial_schema.sql
scripts/db/002_additional_tables_and_constraints.sql
```

---

## 라이선스

Proprietary - GG Network

---

*Last Updated: 2026-01-28*
