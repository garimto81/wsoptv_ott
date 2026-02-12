# WSOPTV 기획 문서 추적기

**최종 업데이트**: 2026-02-10

---

## 핵심 문서 (7개)

| Phase | 문서 | 버전 | 상태 | 최종 수정 |
|:-----:|------|:----:|:----:|----------|
| 0 | [01-vision](../phase0/01-vision.md) | v5.0 | ✅ 확정 | 2026-02-04 |
| 0 | [02-business](../phase0/02-business.md) | v5.0 | ✅ 확정 | 2026-02-05 |
| 0 | [03-vendor-rfp](../phase0/03-vendor-rfp.md) | v1.0 | 🔄 진행중 | 2026-02-05 |
| 0 | [04-vendor-rfp-si](../phase0/04-vendor-rfp-si.md) | v3.0 | 🔄 진행중 | 2026-02-06 |
| 0 | [06-ott-solutions-analysis](../../01_Phase0/06-ott-solutions-analysis.md) | v1.0 | ⭐ Active | 2026-02-10 |
| 1 | [01-mvp-spec](../../02_Phase1/01-mvp-spec.md) | v5.1 | ⭐ Active | 2026-02-05 |
| 1 | [02-content](../../02_Phase1/02-content.md) | v5.1 | Active | 2026-02-05 |

---

## Archived 문서

아래 문서들은 Phase 기반 문서 체계로 전환하면서 `docs/archive/`로 이동되었습니다.

| 이전 코드 | 현재 위치 | 원래 역할 | Archive 사유 |
|----------|----------|----------|-------------|
| PRD-0002 | [archive/](../PRD-0002-wsoptv-concept-paper.md) | 앱 기획서 | Phase 문서로 분리됨 |
| PRD-0002-executive-summary | [archive/](../PRD-0002-executive-summary.md) | 경영진 요약 | Phase 문서로 분리됨 |
| PRD-0005 (Full-Custom RFP) | [archive/](../PRD-0005-wsoptv-ott-rfp-fullcustom.md) | 위탁 운영사 RFP | Vimeo SaaS 전환 |
| PRD-0006 | [archive/](../PRD-0006-advanced-mode.md) | Advanced Mode | Phase 2+ 기능 |
| STRAT-0001 | 01-vision.md에 통합 | 시청자 경험 비전 | Phase 문서로 통합 |
| STRAT-0007 | 02-content.md에 통합 | 콘텐츠 소싱 | Phase 문서로 통합 |
| STRAT-0009 | 02-business.md에 통합 | GG 생태계 전략 | Phase 문서로 통합 |
| TECH-0001 | [archive/](../TECH-0001-streaming-infrastructure.md) | 스트리밍 인프라 | Vimeo SaaS 전환 |
| rfp-feedback-request-templates | [archive/](../rfp-feedback-request-templates.md) | RFP 피드백 요청 템플릿 | PRD-0005 기반, outdated |
| vendor-evaluation-matrix | [archive/](../vendor-evaluation-matrix.md) | 업체 평가 매트릭스 | PRD-0005 기반, outdated |
| REPORT-2026-02-02-nfl-mlb | [01_Phase0/](../../01_Phase0/05-competitor-ott-analysis.md) | NFL/MLB OTT 레퍼런스 | Phase 0으로 이동됨 |

> 전체 archive 목록: 참조용 보관 (26개)

---

## 산출물

| 산출물 | 원본 문서 | 형식 | 경로 |
|--------|----------|------|------|
| WSOP TV OTT RFP | 04-vendor-rfp-si.md | PDF (A4) | [WSOP-TV-OTT-RFP_0206.pdf](../phase0/WSOP-TV-OTT-RFP_0206.pdf) |

---

## 문서 의존성 트리

```
01-vision (Phase 0) ← 최상위 전략
├── 02-business (Phase 0) ← GG 생태계 비즈니스
├── 03-vendor-rfp (Phase 0) ← 업체 선정 경과
│   └── 04-vendor-rfp-si (Phase 0) ← SI 업체 RFP 문서
├── 06-ott-solutions-analysis (Phase 0) ← OTT 솔루션 시장 분석
├── 01-mvp-spec (Phase 1) ← MVP 기획서
└── 02-content (Phase 1) ← 콘텐츠 소싱
```

**의존성 규칙**: 01-vision 변경 시 하위 6개 문서 검토 필요

---

## Google Drive 연동

**Drive Registry**: [DRIVE-REGISTRY.md](./DRIVE-REGISTRY.md) (전체 폴더/파일 ID 매핑)

### Drive 폴더

| 폴더 | Drive ID | 용도 |
|------|----------|------|
| WSOPTV (Primary) | `1U0D2y1TxiY5uaYfImrvewEPk_2Dr6RwC` | 프로젝트 공식 문서 |
| WSOPTV (Team Drive) | `19Sbq1_K-fJOEN2LnMEaMTE9fYjAEFoou` | 팀 공유 드라이브 |

### 현재 유효 문서

| 문서 | Google Docs ID | Drive 위치 | 동기화 |
|------|----------------|------------|:------:|
| PRD-0002 Concept Paper | `1CHOWLGOB_...Z0oY` | prds/PRD-0002/ | ✅ |
| PRD-0002 MVP | `1C7eYlwk...Umw` | prds/PRD-0002/ | ✅ |
| PRD-0005 RFP | `1JVFnhK5...BDgA` | prds/PRD-0005/ | ✅ |
| PRD-0005 RFP (English) | `1b6U1KuF...KGnQ` | prds/PRD-0005/ | ✅ |
| PRD-0006 Advanced Mode | `1f60Fw3T...XsI` | prds/PRD-0006/ | ✅ |
| Executive Summary | `1Y_GmF6A...QDs` | executive/ | ✅ |
| STRAT-0007 Content Sourcing | `1wSBLlo8...LGQQ` | strategy/ | ✅ |
| NBATV Analyze | `1VE0StXf...BBo` | analysis/ | ✅ |

### Archive 문서

| 문서 | Google Docs ID | 동기화 |
|------|----------------|:------:|
| PRD-0002 (old) | [1Y5KMR...](https://docs.google.com/document/d/1Y5KMRFunHJEXmR0MrXbb_flmf-_88obGnJBe0AC94_A/edit) | 📦 Archive |
| PRD-0002-executive-summary (old) | [1Y_GmF...](https://docs.google.com/document/d/1Y_GmF6AYOEkj7TEX3CptimlFVDEGZdssRysdzXHIQDs/edit) | 📦 Archive |

### 변환 명령

```bash
# MD → Google Docs 변환
python -m lib.google_docs convert docs/phase1/01-mvp-spec.md --folder 1K8xgFNKhLePfLMmJ4CzZ5Fx7SGx-GoKk

# Drive 상태 확인
python -m lib.google_docs drive status --folder 1U0D2y1TxiY5uaYfImrvewEPk_2Dr6RwC
```

---

## 상태 정의

| 상태 | 설명 | 아이콘 |
|------|------|:------:|
| 확정 | 론칭 전 결정 완료 | ✅ |
| 진행중 | 작업 중 | 🔄 |
| Active | 현재 유효한 최신 버전 | ⭐ |
| Archive | 참조용 보관 | 📦 |

---

## 버전 관리 규칙

### Phase 문서 버전 체계

```
vX.Y.Z

X (Major): 구조 변경, 전략 변경
Y (Minor): 내용 수정, 섹션 추가
Z (Patch): 오타, 링크 수정
```

---

## 문서 변경 프로세스

1. **변경 요청**: Slack 의사결정 또는 Michael 지침
2. **문서 수정**: 로컬 `.md` 파일 수정 + 버전 번호 증가
3. **의존성 확인**: 상위 문서 변경 시 하위 문서 검토
4. **DOCUMENT-TRACKER 업데이트**: 버전/상태/날짜 갱신

---

## 참조 문서

| 문서 | 용도 |
|------|------|
| 문서 인덱스 | 프로젝트 루트 참조 |
| [CLAUDE.md](../../CLAUDE.md) | 프로젝트 설정 |
| Archive 전체 목록 | 참조용 보관 |
| [VENDOR-DASHBOARD.md](./VENDOR-DASHBOARD.md) | 업체 관리 |
| [DRIVE-REGISTRY.md](./DRIVE-REGISTRY.md) | Drive 폴더/파일 ID 매핑 |

---

## Revision History

| 버전 | 날짜 | 작성자 | 내용 |
|------|------|--------|------|
| 3.1 | 2026-02-10 | Claude Code | 06-ott-solutions-analysis 추가, Phase1/Archive 경로 수정 (99_Archive_ngd 기준), 의존성 트리 갱신 (6개 문서) |
| 3.0 | 2026-02-06 | Claude Code | 04-vendor-rfp-si.md(v3.0) 추가, 의존성 트리 갱신, PDF 산출물 섹션 추가, outdated 템플릿/리포트 archive 이동 반영 |
| 2.1 | 2026-02-06 | Claude Code | Google Drive Registry 연동, Drive 폴더/파일 ID 매핑 추가, DRIVE-REGISTRY.md 참조 |
| 2.0 | 2026-02-05 | Claude Code | Phase 기반 체계로 전면 개편, PRD/STRAT 코드 → Phase 문서 전환, Archive 섹션 추가 |
| 1.0 | 2026-02-02 | Claude Code | 최초 작성 - PRD/STRAT 코드 기반 추적 |
