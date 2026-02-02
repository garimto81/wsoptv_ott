# WSOPTV 기획 문서 추적기

**최종 업데이트**: 2026-02-02 15:00

---

## Tier 1: 핵심 문서 (7개)

| 문서 | 버전 | 상태 | 최종 수정 | Google Docs | 동기화 |
|------|:----:|:----:|----------|:-----------:|:------:|
| PRD-0002 | v10.0 | ✅ Active | 2026-01-30 | [Link](https://docs.google.com/document/d/1Y5KMRFunHJEXmR0MrXbb_flmf-_88obGnJBe0AC94_A) | ✅ |
| PRD-0002-executive-summary | v6.4 | ✅ Active | 2026-01-30 | [Link](https://docs.google.com/document/d/1Y_GmF6AYOEkj7TEX3CptimlFVDEGZdssRysdzXHIQDs) | ✅ |
| PRD-0006 | v2.0 | ✅ Active | 2026-01-28 | - | - |
| STRAT-0001 | v1.0 | ✅ Active | 2026-01-20 | - | - |
| STRAT-0007 | v1.0 | ✅ Active | 2026-01-22 | - | - |
| STRAT-0009 | v1.0 | ✅ Active | 2026-01-30 | - | - |
| TECH-0001 | v1.0 | ✅ Active | 2026-01-30 | - | - |

---

## 업데이트 필요 문서

### 🟡 PRD-0002 - MVP 범위 변경 반영 필요
- **현재 버전**: v10.0
- **필요 버전**: v10.1
- **변경 사유**: DEC-2026-0201-001 (MVP = Single-Stream 확정)
- **담당**: @Aiden
- **기한**: 2026-02-05

---

## 버전 히스토리

### PRD-0002 (Concept Paper)

| 버전 | 날짜 | 변경 내용 | 작성자 |
|:----:|------|----------|--------|
| v10.0 | 2026-01-30 | 용어 재정의, STRAT-0009/TECH-0001 분리 | @Aiden |
| v9.0 | 2026-01-28 | WSOPTV Station 아키텍처 추가 | @Aiden |
| v8.0 | 2026-01-25 | Advanced Mode 4-layer 확정 | @Aiden |
| v7.0 | 2026-01-22 | Multi-view 3-layer 확정 | @Aiden |
| v6.0 | 2026-01-20 | 핵심 차별점 재정의 | @Aiden |
| v5.0 | 2026-01-18 | Player Cam 개념 추가 | @Aiden |
| v4.0 | 2026-01-15 | Timeshift 기능 명세 | @Aiden |
| v3.0 | 2026-01-12 | 아키텍처 다이어그램 추가 | @Aiden |
| v2.0 | 2026-01-10 | 경쟁사 분석 추가 | @Aiden |
| v1.0 | 2026-01-08 | 초기 버전 | @Aiden |

### PRD-0002-executive-summary

| 버전 | 날짜 | 변경 내용 | 작성자 |
|:----:|------|----------|--------|
| v6.4 | 2026-01-30 | WSOPTV Station 아키텍처 목업 추가 | @Aiden |
| v6.3 | 2026-01-28 | 비용 추정치 업데이트 | @Aiden |
| v6.2 | 2026-01-25 | 경쟁사 분석 추가 | @Aiden |
| v6.1 | 2026-01-22 | Executive Summary 독립 문서화 | @Aiden |
| v6.0 | 2026-01-20 | 실제 UI 이미지로 교체 | @Aiden |
| v5.0 | 2026-01-18 | 경영진 보고용 요약 작성 | @Aiden |

---

## 문서 의존성 트리

```
                    ┌─────────────────────────────┐
                    │    STRAT-0001 (Vision)      │  ← 시청자 경험 비전
                    └──────────────┬──────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        ▼                          ▼                          ▼
┌────────────┐              ┌────────────┐              ┌────────────┐
│ STRAT-0009 │              │ PRD-0002   │              │ TECH-0001  │
│ 비즈니스   │─────────────▶│ 앱 기획서  │◀─────────────│ 기술 인프라│
└────────────┘              └──────┬─────┘              └────────────┘
                                   │
                ┌──────────────────┼──────────────┐
                ▼                  ▼              ▼
         ┌────────────┐     ┌────────────┐ ┌────────────┐
         │ PRD-0006   │     │ Exec.Sum   │ │ STRAT-0007 │
         │ Advanced   │     │ 경영진용   │ │ Content    │
         └────────────┘     └────────────┘ └────────────┘
```

**의존성 설명:**
- **STRAT-0001** (Vision): 모든 문서의 최상위 전략 문서
- **PRD-0002** (Concept Paper): 앱 기획의 핵심 문서
  - **PRD-0002-executive-summary**: 경영진 보고용 요약본
  - **PRD-0006** (Advanced Mode): PRD-0002의 고급 기능 상세 명세
- **STRAT-0009** (GG Ecosystem): 비즈니스 모델 및 수익화 전략
- **STRAT-0007** (Content Sourcing): 콘텐츠 소싱 및 라이선스 전략
- **TECH-0001** (Streaming Infrastructure): 기술 인프라 및 아키텍처

---

## 상태 정의

| 상태 | 설명 | 아이콘 |
|------|------|:------:|
| Active | 현재 유효한 최신 버전 | ✅ |
| Update Required | 변경 사항 반영 필요 | 🟡 |
| Draft | 작성 중, 검토 필요 | ⚠️ |
| Deprecated | 더 이상 유효하지 않음 | 🔴 |
| Archived | 아카이브됨 (참조용) | 📦 |

---

## Google Docs 동기화 가이드

### 동기화 상태

| 상태 | 설명 | 아이콘 |
|------|------|:------:|
| 동기화됨 | 로컬과 Google Docs 일치 | ✅ |
| 동기화 필요 | 로컬 변경 사항 미반영 | ⚠️ |
| Google Docs 없음 | 로컬 전용 문서 | - |

### 동기화 절차

1. 로컬 문서 수정 (`.md` 파일)
2. 변경 내용 검토 및 버전 증가
3. Google Docs 수동 업데이트
4. DOCUMENT-TRACKER.md에 동기화 상태 업데이트

### Google Docs URL

| 문서 | Google Docs ID | URL |
|------|----------------|-----|
| PRD-0002 | 1Y5KMRFunHJEXmR0MrXbb_flmf-_88obGnJBe0AC94_A | [열기](https://docs.google.com/document/d/1Y5KMRFunHJEXmR0MrXbb_flmf-_88obGnJBe0AC94_A/edit) |
| PRD-0002-executive-summary | 1Y_GmF6AYOEkj7TEX3CptimlFVDEGZdssRysdzXHIQDs | [열기](https://docs.google.com/document/d/1Y_GmF6AYOEkj7TEX3CptimlFVDEGZdssRysdzXHIQDs/edit) |

---

## 버전 관리 규칙

### 버전 번호 체계 (Semantic Versioning)

```
vX.Y

X (Major): 구조 변경, 새 섹션 추가, 근본적인 전략 변경
Y (Minor): 내용 수정, 업데이트, 목업 추가
```

### 버전 증가 가이드

| 변경 유형 | 버전 증가 | 예시 |
|-----------|----------|------|
| 새 섹션 추가 | Major (X.0) | v9.0 → v10.0 |
| 구조 재편성 | Major (X.0) | v8.0 → v9.0 |
| 내용 수정 | Minor (X.Y) | v10.0 → v10.1 |
| 목업 추가 | Minor (X.Y) | v6.3 → v6.4 |
| 오타 수정 | Minor (X.Y) | v6.1 → v6.2 |

---

## 문서 변경 프로세스

### 1. 변경 요청
- 출처: 슬랙 의사결정 (DEC-YYYY-MMDD-NNN)
- 담당자 지정
- 기한 설정

### 2. 문서 업데이트
- 로컬 `.md` 파일 수정
- 버전 번호 증가
- 변경 내용 기록

### 3. 검토 및 승인
- 내부 검토
- 관련 문서 의존성 확인

### 4. 동기화 (Google Docs 연동 문서만)
- Google Docs 수동 업데이트
- 동기화 상태 업데이트

### 5. DOCUMENT-TRACKER 업데이트
- 버전 히스토리 추가
- 상태 업데이트
- "업데이트 필요 문서" 섹션 정리

---

## 운영 규칙

### 주간 리뷰 (매주 월요일)
- [ ] "업데이트 필요 문서" 섹션 점검
- [ ] 슬랙 의사결정 로그에서 문서 변경 요청 확인
- [ ] Google Docs 동기화 상태 확인

### 월간 아카이브 (매월 말일)
- [ ] Deprecated 문서 아카이브 폴더로 이동
- [ ] 버전 히스토리 정리 (6개월 이상 경과 시)

### 의존성 관리
- 상위 문서 변경 시 하위 문서 업데이트 필요 여부 검토
- 예: STRAT-0001 변경 → PRD-0002, STRAT-0009, TECH-0001 영향도 분석

---

## 참조 문서

- 프로젝트 개요: `C:\claude\wsoptv_ott\CLAUDE.md`
- 문서 인덱스: `C:\claude\wsoptv_ott\docs\README.md`
- 문서 계층 구조: CLAUDE.md 참조
