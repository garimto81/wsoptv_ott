# Phase 0-02: Business (GG 생태계 비즈니스 전략)

| 항목 | 값 |
|------|---|
| **Phase** | 0 (준비 단계) |
| **Version** | 5.0.0 |
| **Updated** | 2026-02-04 |
| **Status** | ✅ 확정 |
| **Depends** | [01-vision](01-vision.md) |

---

## 용어 정의

> 모든 문서에서 동일한 용어를 사용합니다. 상세 정의: [01-vision](01-vision.md)

| 용어 | 정의 | Phase |
|------|------|:-----:|
| **Single Video** | 한 번에 하나의 비디오만 시청 | MVP |
| **Selected View** | 보고 싶은 방송을 선택해서 볼 수 있는 기능 | MVP |
| **Multi-video** | 여러 비디오 플레이어를 동시에 재생 | 2+ |
| **Timeshift** | 라이브 중 되감기 기능 | MVP |
| **StatsView** | 플레이어 통계 HUD 오버레이 | 2+ |

> **핵심 구분**: Selected View(방송 선택)는 MVP, Multi-video(동시 재생)는 Phase 2+

---

## 1. 개요

> **핵심**: WSOPTV는 독립 OTT가 아니라 **GG 생태계의 "콘텐츠 놀이터"**로서 GG POKER 구독의 핵심 혜택 역할을 수행합니다.

이 문서는 PRD-0002 섹션 -1 "GG 생태계 내 WSOPTV 역할"에서 분리된 비즈니스 전략 문서입니다.

---

## 2. GGPass 구독 구조

![GGPass 생태계 구조](../99-archive/images/PRD-0002/57-ggpass-ecosystem.png)

[HTML 원본](../99-archive/mockups/PRD-0002/57-ggpass-ecosystem.html)

| 구분 | 특징 | 서비스 |
|:----:|------|--------|
| **구독 전용 서비스** | 서비스 이용 시 구독 필수, Payment 구현 필수 | ClubbGG, WSOP Academy, **WSOP TV** |
| **구독 혜택 서비스** | 구독자에게 혜택 제공, Payment 구현 안함 | GGPoker, WSOP+, Pokerstake |

---

## 3. 쿠팡플레이 비교 (역순 구조)

> 📋 **MOSES**: 쿠팡플레이와 구조는 유사하지만 **위치가 반대**입니다.

| 구분 | 쿠팡플레이 | WSOPTV |
|:----:|-----------|--------|
| **구독 중심** | 쿠팡 로켓와우 | **WSOPTV** |
| **혜택 방향** | 로켓와우 → 쿠팡플레이 무료 | WSOPTV 구독 → ClubbGG, Academy, GGPoker 혜택 |
| **핵심 서비스** | e-commerce | **동영상 시청** |

### Reader App 전략 (앱스토어 수수료 회피)

| 서비스 | 앱스토어 수수료 | Reader App 판정 |
|--------|:-------------:|:---------------:|
| **WSOPTV** | **면제 가능** | ✅ 동영상 시청 위주 |
| WSOP Academy | 면제 시도 예정 | ⚠️ 교육 콘텐츠 |
| ClubbGG | 수수료 부담 | ❌ 게임 콘텐츠 |

> **Reader App이란?**: 디지털 콘텐츠(책, 잡지, 음악, 비디오 등)를 구독하는 앱으로, Apple/Google이 별도로 분류하여 인앱 결제 수수료를 면제하는 앱 유형. Netflix, Spotify 등이 해당.

**WSOPTV가 중심인 이유**:
- 동영상 시청 위주 비즈니스 모델 → Reader App 판정 용이
- WSOPTV 구독이 다른 GG 서비스 혜택의 게이트웨이 역할
- 앱스토어 수수료 부담 없이 구독 결제 가능

---

## 4. 포커 시청 특성과 "콘텐츠 놀이터" 개념

포커 대회 시청은 일반 스포츠와 근본적으로 다릅니다.

| 특성 | 일반 스포츠 (NBA 등) | 포커 대회 |
|------|---------------------|----------|
| **경기 시간** | 2-3시간 | 수 시간~수십 시간 |
| **구조** | 긴장감 유지 | 느슨한 구조 (핸드 간 대기) |
| **시청 패턴** | 집중 시청 | **탐색/검색/비교** |
| **몰입 방식** | 경기 자체에 몰입 | 플레이어 중심 관심 |

### "콘텐츠 놀이터" 철학

포커 플레이어는 영상 자체에 집중하기보다, WSOPTV를 **놀이터**처럼 이용합니다:
- GG POKER에서 게임 플레이 중 휴식
- WSOPTV로 이동하여 대회 시청
- 관심 있는 플레이어 발견 → Player Cam으로 집중 시청
- 해당 플레이어의 과거 핸드/하이라이트 탐색
- 다시 GG POKER로 돌아가 플레이

---

## 5. Dual Flywheel: 이중 선순환 구조

![Dual Flywheel](../99-archive/images/PRD-0002/58-dual-flywheel.png)

[HTML 원본](../99-archive/mockups/PRD-0002/58-dual-flywheel.html)

```
┌───────────────────────────────────────────────────────────────────┐
│                                                                   │
│   GG POKER 플레이 ════════════════════════▶ WSOPTV 시청           │
│         ▲                                        │                │
│         │                                        ▼                │
│         │                               플레이어 팬심 형성         │
│         │                                        │                │
│         │                                        ▼                │
│   플레이시간 증가 ◀════════════════════════ 체류시간 증가          │
│                                                                   │
│     [GG 생태계]                        [콘텐츠 놀이터]             │
└───────────────────────────────────────────────────────────────────┘
```

**이중 효과:**
1. **WSOPTV 체류시간 증가**: 플레이어 중심 콘텐츠 탐색
2. **GG POKER 플레이시간 증가**: 영감을 받아 다시 게임으로 복귀

---

## 6. 고급 기능의 생태계적 의미

기능을 **독립 OTT 관점**으로 판단하면 비효율적으로 보입니다. 하지만 **GG 생태계 관점**에서는 핵심적인 의미를 갖습니다.

### 6.1 MVP vs Phase 2+ 기능 분류 (2026-02-04 업데이트)

> **전략 변경**: Vimeo 기본 템플릿 기반 MVP 론칭 → 고급 기능은 Phase 2+ 검토

| 기능 | MVP | Phase 2+ | 생태계 가치 |
|------|:---:|:--------:|------------|
| **Single Video** | ✅ | - | 기본 시청 경험 제공 |
| **Selected View** | ✅ | - | 다중 생방송 중 선택 시청 |
| **Multi-video (Table)** | ❌ | ⚠️ 검토 | 여러 테이블 동시 재생 (구현 난이도 높음) |
| **Multi-video (Player Cam)** | ❌ | ⚠️ 검토 | 선수 직캠 동시 표시 (추가 인프라 필요) |
| **Hand Search** | ⚠️ | ✅ | 명장면 컬렉션 (메타데이터 태깅) |
| **StatsView** | ❌ | ⚠️ 검토 | 학습/분석 (커스텀 개발 필요) |

> **핵심 인사이트**: Selected View(선택 시청)는 기본 OTT로 구현 가능하여 MVP 포함. Multi-video(동시 재생)는 커스텀 개발 필요하여 Phase 2+.

### 6.2 MVP 우선 전략의 배경

| 기존 접근 | 변경된 접근 |
|----------|-----------|
| Full-Custom 개발 (50억+) | **Vimeo SaaS 활용 (~1억)** |
| 모든 기능 동시 구현 | **MVP 론칭 → 피드백 기반 확장** |
| 높은 초기 투자, 긴 개발 기간 | **빠른 시장 진입, 낮은 리스크** |

> **핵심 인사이트**: Multi-video/Player Cam의 생태계 가치는 인정하나, **구현 난이도 대비 ROI가 불확실**하여 MVP 필수 요건에서 제외. 사용자 데이터 수집 후 Phase 2에서 재검토.

---

## 7. 프리미엄 구독 혜택 전략

> **전략 변경 (2026-02-02)**: Multi-video는 MVP에서 제외. **대안 프리미엄 혜택**으로 Plus+ 가치 제안.

### 프리미엄 vs 스탠다드 가격 비교

| 티어 | 가격 | 배수 | MVP 기대 가치 |
|:----:|:----:|:----:|--------------|
| WSOP Plus | $9.99/월 | 1x | 기본 시청, 광고 포함 |
| WSOP Plus+ | $49.99/월 | **5x** | 대안 혜택 + 프리미엄 경험 |

### MVP 프리미엄 혜택 (Multi-video 없이)

> **핵심**: 기술적 고급 기능 대신 **콘텐츠 차별화**로 Plus+ 가치 제안

| 카테고리 | 혜택 | 설명 | MVP |
|----------|------|------|:---:|
| **편집 콘텐츠** | DNEG 하이라이트 | Daniel Negreanu 명장면 모음 | ✅ |
| | Ivey 하이라이트 | Phil Ivey 명장면 모음 | ✅ |
| | Top 10 Bad Beat | WSOP 역대 Bad Beat 순위 | ✅ |
| **독점 콘텐츠** | Making Film | 대회 비하인드 씬 | ✅ |
| | Player's Commentary | 선수 직접 해설 | ⚠️ |
| | Poker News | 포커 뉴스/인터뷰 | ✅ |
| **OTT 기능** | 동시 시청 기기 | 최대 3개 (Plus+) vs 1개 (Plus) | ✅ |
| | 오프라인 다운로드 | 모바일 동영상 저장 | ✅ |
| | 광고 제거 | Plus+ 전용 | ✅ |
| **Phase 2+** | Multi-video | 여러 테이블 동시 시청 | ❌ |
| | Player Cam | 플레이어 직캠 | ❌ |
| | StatsView | 통계 오버레이 | ❌ |

> **참고**: 일반 OTT의 4K 화질 제공 혜택은 불가능 (소스 제약)

---

## 8. GGPoker 트래픽 연동

> 📋 **MOSES**: WSOPTV 론칭 시 GGPoker 내 관련 영역이 WSOPTV로 연결되어 트래픽을 유입시킵니다.

### 현재: GGPoker.TV (YouTube 연동)

![GGPoker.TV 섹션](../99-archive/images/PRD-0002/59-ggpoker-tv-section.png)

현재 GGPoker 앱 로비에는 **"GGPoker.TV"** 섹션이 있으며, YouTube 콘텐츠를 직접 앱 내에서 보여주고 있습니다.

| 현재 상태 | 내용 |
|----------|------|
| **섹션명** | GGPoker.TV |
| **콘텐츠 소스** | YouTube |
| **표시 콘텐츠** | Super High Roller Poker, GGMillion$ 등 라이브 대회 |
| **조회수** | 17K~24K views |
| **위치** | GGPoker 로비 중앙 (배너 아래) |

### WSOPTV 론칭 후: 트래픽 전환

| 현재 (GGPoker.TV) | WSOPTV 론칭 후 |
|------------------|----------------|
| YouTube 콘텐츠 임베드 | **WSOPTV 딥링크** |
| 무료 시청만 가능 | 프리미엄 기능 안내 |
| GGPoker 앱 내 시청 | WSOPTV 앱 전환 또는 앱 내 플레이어 |

**트래픽 전환 시나리오**:
1. GGPoker.TV 섹션 → **"WSOPTV"**로 브랜드 변경
2. YouTube 링크 → WSOPTV 딥링크로 교체
3. 무료 하이라이트 제공 + "풀버전은 WSOPTV에서" CTA
4. Plus 구독자 → 앱 내 WSOPTV 플레이어에서 바로 시청

> **예상 효과**: 기존 GGPoker.TV 시청자(월 수십만 views)가 자연스럽게 WSOPTV로 유입

---

## 9. 관련 문서

| 문서 | 설명 |
|------|------|
| [PRD-0002](../99-archive/PRD-0002-wsoptv-concept-paper.md) | 앱 기획서 (Archive) |
| [01-vision](01-vision.md) | 시청자 경험 비전 |
| [STRAT-0003](../99-archive/STRAT-0003-cross-promotion.md) | 크로스 프로모션 전략 (Archive) |

---

## Revision History

| 버전 | 날짜 | 작성자 | 내용 |
|------|------|--------|------|
| 2.0 | 2026-02-04 | Claude Code | Selected View vs Multi-video 명확 구분 |
| 1.1 | 2026-02-02 | Claude Code | Vimeo 기반 MVP 전략 반영, Multi-video Phase 2+ 이동 |
| 1.0 | 2026-01-30 | Claude Code | PRD-0002 섹션 -1에서 분리하여 최초 작성 |
