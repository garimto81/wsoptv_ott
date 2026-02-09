# Phase 0-03: Vendor Selection (업체 선정)

| 항목 | 값 |
|------|---|
| **Phase** | 0 (준비 단계) |
| **Version** | 1.0.0 |
| **Updated** | 2026-02-05 |
| **Status** | 🔄 진행중 |
| **Depends** | [01-vision](01-vision.md), [02-business](02-business.md) |

---

## 용어 정의

> 모든 문서에서 동일한 용어를 사용합니다. 상세 정의: [01-vision](01-vision.md)

| 용어 | 정의 | MVP 포함 |
|------|------|:--------:|
| **Single Video** | 한 번에 하나의 비디오만 시청 | ✅ |
| **Selected View** | 보고 싶은 방송을 선택해서 볼 수 있는 기능 | ✅ |
| **Multi-video** | 여러 비디오 플레이어를 동시에 재생 | ❌ Phase 2+ |
| **Timeshift** | 라이브 중 되감기 기능 | ✅ |
| **StatsView** | 플레이어 통계 HUD 오버레이 | ❌ Phase 2+ |

> **핵심 구분**: Selected View(방송 선택)는 MVP, Multi-video(동시 재생)는 Phase 2+

---

## 1. 전략 변경 배경

### 기존 방향 vs 변경 방향

| 항목 | 기존 방향 | 현재 방향 |
|------|----------|----------|
| **솔루션** | Full-Custom 개발 (메가존) | Vimeo SaaS 기반 |
| **비용** | 48억 + 15억/년 | $42,500/년 (기본) |
| **접근법** | 모든 기능 동시 구현 | MVP 론칭 → 점진적 확장 |
| **기간** | 12개월+ | Q3 2026 론칭 |

### 결정 경위

- **결정자**: Michael
- **결정일**: 2026-02-03
- **핵심 지침**: Vimeo 솔루션 활용, $1만 이내 예산으로 신속 추진
- **추가 지침** (2026-02-05): Vimeo 기본 템플릿으로 시작, Multi-video는 선택적

> **원천**: [michael_note](../vible/michael_note.md)

---

## 2. 검토 업체 및 결과

### 전체 현황

| 업체 | 상태 | 견적 | 결론 |
|------|:----:|------|:----:|
| **Vimeo OTT** | 🟢 최우선 | $42,500/년 (기본) | 협상 중 |
| **Brightcove** | ⚠️ 2순위 | $1,735,949 (첫해) | 예산 초과 |
| **메가존** | 🟡 보류 | 48억 + 15억/년 | Vimeo 우선 |
| **맑음소프트** | 🔴 제외 | 1~2억 | P1 미충족 |

### 2.1 Vimeo OTT (최우선)

**1차 견적** (2026-02-04 수령):

| 옵션 | 구성 | 정가 (USD) | 할인가 (USD) |
|------|------|-----------|-------------|
| **기본** | OTT Starter + Enterprise | $42,500/년 | - |
| **옵션 1** | 기본 + 추가 기능 | $144,000/년 | $108,000/년 |
| **옵션 2** | 기본 + 다수 기능 | $564,000/년 | $282,000/년 |
| **옵션 3** | 풀옵션 | $863,000/년 | $388,000/년 |

**마이클 목표 예산**: $10,000~$40,000 → 기본 옵션($42,500) 근접

**강점**: OTT 앱 템플릿 제공, AWS S3 연동, SAML SSO, Bring Your Own Payment

**리스크**:
- 커스터마이징 제한 (플랫폼 기본 기능 범위)
- OTT 사업부 매각 진행 중 (단, Senior Engineer 배정)

### 2.2 Brightcove (2순위 대안)

- 첫해 총액 $1,735,949 (마이클 목표 대비 170배 초과)
- 기술적으로 검증됨 (Emmy Award, 글로벌 레퍼런스)
- Vimeo 협상 결렬 시 재검토

### 2.3 메가존클라우드 (보류)

- 48억 구축 + 15억/년 운영
- Vimeo 우선 진행 지침으로 대기 중

### 2.4 맑음소프트 (제외)

- P1 요구사항 미충족: Multi-view 미지원, Timeshift 10분 제한
- 총점 2.90 (C등급, 3.0 미만)

---

## 3. Vimeo OTT 기능 매핑

### MVP 기능 지원 여부

| 기능 | Vimeo 지원 | 비고 |
|------|:----------:|------|
| Live Streaming | ✅ | HLS 기반 |
| VOD | ✅ | 업로드 + 트랜스코딩 |
| Timeshift/DVR | ✅ | 라이브 중 되감기 |
| Subscription | ✅ | Bring Your Own Payment |
| Multi-platform Apps | ✅ | iOS, Android, TV 템플릿 |
| Selected View | ✅ | 기본 OTT 기능으로 충분 |
| SSO | ✅ | SAML 기반 |

### Phase 2+ (미지원, 커스텀 개발 필요)

| 기능 | 비고 |
|------|------|
| Multi-video | 커스텀 플레이어 필요 |
| StatsView | GGPoker HUD 연동 필요 |
| Hand Search | Elasticsearch 필요 |
| Custom Player UI | Vimeo 기본 플레이어 한계 |

---

## 4. 구독 가격 구조

> **권위 소스**: [02-business](02-business.md) 섹션 7

| 티어 | 가격 | 명칭 | 핵심 차별점 |
|------|------|------|-----------|
| Basic | **$9.99/월** | **WSOP Plus** | 라이브, VOD, Timeshift, 1기기 |
| Premium | **$49.99/월** | **WSOP Plus+** | 광고 없음, 3기기, 오프라인 다운로드, 편집/독점 콘텐츠 |

> Plus+ 차별화 핵심: **콘텐츠 차별화** (편집/독점 콘텐츠) + **OTT 기능 차별화** (3기기, 오프라인, 광고 제거)

---

## 5. 기술 검증 현황

### 트라이얼

- **사이트**: https://wsoptv.vhx.tv
- **계정**: aiden.kim@ggproduction.net
- **Site ID**: 264812

### 기술 논의 결과

| 항목 | 결과 |
|------|------|
| **AWS S3 연동** | 기존 S3 콘텐츠 Vimeo 마이그레이션 가능 |
| **SSO** | SAML 기반 SSO 연동 가능 |
| **결제** | Bring Your Own Payment (Stripe) 지원 |
| **OTT 앱** | iOS, Android, TV 앱 템플릿 제공 |

---

## 6. 다음 단계

| 우선순위 | 작업 | 담당 |
|:-------:|------|------|
| P0 | OTT 전용 수정 견적 최종 확인 | @Aiden |
| P0 | $10K~$40K 범위 옵션 협상 | @Aiden |
| P0 | 트라이얼 테스트 결과 정리 | @Aiden |
| P1 | SSO, 결제 연동 상세 협의 | @Aiden |
| P2 | Brightcove 재검토 여부 결정 | @Aiden |

---

## 7. 관련 문서

| 문서 | 설명 |
|------|------|
| [01-vision](01-vision.md) | 시청자 경험 비전 |
| [02-business](02-business.md) | GG 생태계 비즈니스 전략 |
| [VENDOR-DASHBOARD](../management/VENDOR-DASHBOARD.md) | 업체 관리 대시보드 |
| [04-vendor-rfp-si](04-vendor-rfp-si.md) | SI 업체 RFP 문서 ([PDF](WSOP-TV-OTT-RFP_0206.pdf)) |
| [Full-Custom RFP](../archive/PRD-0005-wsoptv-ott-rfp-fullcustom.md) | 이전 Full-Custom RFP (Archive) |

---

## Revision History

| 버전 | 날짜 | 작성자 | 내용 |
|------|------|--------|------|
| 1.0.0 | 2026-02-05 | Claude Code | Vimeo 기반 업체 선정 경과 문서로 전면 개정 (Full-Custom RFP → Archive 이동) |
