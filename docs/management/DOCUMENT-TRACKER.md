# WSOPTV 기획 문서 추적기

**최종 업데이트**: 2026-02-05

---

## 핵심 문서 (5개)

| Phase | 문서 | 버전 | 상태 | 최종 수정 |
|:-----:|------|:----:|:----:|----------|
| 0 | [01-vision](../phase0/01-vision.md) | v5.0 | ✅ 확정 | 2026-02-04 |
| 0 | [02-business](../phase0/02-business.md) | v5.0 | ✅ 확정 | 2026-02-05 |
| 0 | [03-vendor-rfp](../phase0/03-vendor-rfp.md) | v1.0 | 🔄 진행중 | 2026-02-05 |
| 1 | [01-mvp-spec](../phase1/01-mvp-spec.md) | v5.1 | ⭐ Active | 2026-02-05 |
| 1 | [02-content](../phase1/02-content.md) | v5.1 | Active | 2026-02-05 |

---

## Archived 문서

아래 문서들은 Phase 기반 문서 체계로 전환하면서 `docs/archive/`로 이동되었습니다.

| 이전 코드 | 현재 위치 | 원래 역할 | Archive 사유 |
|----------|----------|----------|-------------|
| PRD-0002 | [archive/](../archive/PRD-0002-wsoptv-concept-paper.md) | 앱 기획서 | Phase 문서로 분리됨 |
| PRD-0002-executive-summary | [archive/](../archive/PRD-0002-executive-summary.md) | 경영진 요약 | Phase 문서로 분리됨 |
| PRD-0005 (Full-Custom RFP) | [archive/](../archive/PRD-0005-wsoptv-ott-rfp-fullcustom.md) | 위탁 운영사 RFP | Vimeo SaaS 전환 |
| PRD-0006 | [archive/](../archive/PRD-0006-advanced-mode.md) | Advanced Mode | Phase 2+ 기능 |
| STRAT-0001 | 01-vision.md에 통합 | 시청자 경험 비전 | Phase 문서로 통합 |
| STRAT-0007 | 02-content.md에 통합 | 콘텐츠 소싱 | Phase 문서로 통합 |
| STRAT-0009 | 02-business.md에 통합 | GG 생태계 전략 | Phase 문서로 통합 |
| TECH-0001 | [archive/](../archive/TECH-0001-streaming-infrastructure.md) | 스트리밍 인프라 | Vimeo SaaS 전환 |

> 전체 archive 목록: [archive/README.md](../archive/README.md) (23개)

---

## 문서 의존성 트리

```
01-vision (Phase 0) ← 최상위 전략
├── 02-business (Phase 0) ← GG 생태계 비즈니스
├── 03-vendor-rfp (Phase 0) ← 업체 선정
├── 01-mvp-spec (Phase 1) ← MVP 기획서
└── 02-content (Phase 1) ← 콘텐츠 소싱
```

**의존성 규칙**: 01-vision 변경 시 하위 4개 문서 검토 필요

---

## Google Docs 동기화

| 문서 | Google Docs ID | 동기화 |
|------|----------------|:------:|
| PRD-0002 (Archive) | [1Y5KMR...](https://docs.google.com/document/d/1Y5KMRFunHJEXmR0MrXbb_flmf-_88obGnJBe0AC94_A/edit) | 📦 Archive |
| PRD-0002-executive-summary (Archive) | [1Y_GmF...](https://docs.google.com/document/d/1Y_GmF6AYOEkj7TEX3CptimlFVDEGZdssRysdzXHIQDs/edit) | 📦 Archive |

> Phase 문서는 로컬 전용입니다. Google Docs 동기화 불필요.

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
| [docs/README.md](../README.md) | 문서 인덱스 |
| [CLAUDE.md](../../CLAUDE.md) | 프로젝트 설정 |
| [archive/README.md](../archive/README.md) | Archive 전체 목록 |
| [VENDOR-DASHBOARD.md](./VENDOR-DASHBOARD.md) | 업체 관리 |

---

## Revision History

| 버전 | 날짜 | 작성자 | 내용 |
|------|------|--------|------|
| 2.0 | 2026-02-05 | Claude Code | Phase 기반 체계로 전면 개편, PRD/STRAT 코드 → Phase 문서 전환, Archive 섹션 추가 |
| 1.0 | 2026-02-02 | Claude Code | 최초 작성 - PRD/STRAT 코드 기반 추적 |
