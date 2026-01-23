# PRD-0002: WSOPTV OTT Platform MVP

| 항목 | 값 |
|------|---|
| **Version** | 5.0 |
| **Status** | Draft |
| **Priority** | P0 |
| **Created** | 2026-01-07 |
| **Updated** | 2026-01-22 |
| **Author** | Claude Code |
| **Launch Target** | Q3 2026 |

---

## 0. 3대 원천 기반 설계 원칙

### 0.1 3대 원천 (Three Pillars)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        WSOP TV 설계 3대 원천                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐           │
│  │   📜 VIBLE      │   │   📋 MOSES      │   │   📖 KORAN      │           │
│  │  (Michael Note) │   │  (Tony Note)    │   │   (NBA TV)      │           │
│  ├─────────────────┤   ├─────────────────┤   ├─────────────────┤           │
│  │ 운영 계획의 근간 │   │ 첨언 및 확장    │   │ UI/UX 참조      │           │
│  │ 비즈니스 요구사항│   │ 태깅/검색 기능  │   │ 1:1 복제 대상   │           │
│  │ 콘텐츠 소싱 전략 │   │ 고급 검색 예시  │   │ 레이아웃 표준   │           │
│  └─────────────────┘   └─────────────────┘   └─────────────────┘           │
│                                                                             │
│  우선순위: VIBLE > MOSES > KORAN (충돌 시 상위 원천 우선)                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

| 원천 | 명칭 | 출처 | 역할 | 우선순위 |
|:----:|------|------|------|:--------:|
| 📜 | **VIBLE** | michael_note.md | 운영 계획의 근간, 비즈니스 요구사항 | 1 (최고) |
| 📋 | **MOSES** | tony_note.md | 첨언 및 확장, 태깅/검색 기능 | 2 |
| 📖 | **KORAN** | NBA TV League Pass | UI/UX 참조, 1:1 복제 대상 | 3 |

### 0.2 충돌 해결 원칙

> **VIBLE이 말씀하시면, MOSES가 해석하고, KORAN이 구현한다.**

| 상황 | 해결 방법 |
|------|----------|
| VIBLE ↔ MOSES 충돌 | VIBLE 우선 |
| VIBLE ↔ KORAN 충돌 | VIBLE 우선 |
| MOSES ↔ KORAN 충돌 | MOSES 우선 |
| 모두 언급 없음 | KORAN 기본 패턴 적용 |

### 0.3 기능 분류

| 분류 | 원천 | 정의 | 예시 |
|------|:----:|------|------|
| **Core-Vible** | 📜 | VIBLE에서 명시한 필수 기능 | Advanced Mode, GGPass, 구독 모델 |
| **Core-Moses** | 📋 | MOSES에서 제안한 확장 기능 | 핸드 태깅, 검색, 멀티 재생 |
| **Core-Koran** | 📖 | KORAN 1:1 대응 기능 | Ticker, MultiView, Info Tabs |
| **Extension** | - | 3대 원천에 없는 확장 기능 | Equity Calculator, Hand Range |

---

## 1. Executive Summary

### 1.1 프로젝트 개요

WSOP 공식 OTT 스트리밍 플랫폼. **3대 원천을 기반**으로 설계한 프리미엄 포커 방송 서비스.

| 항목 | 내용 | 원천 |
|------|------|:----:|
| **런칭 목표** | Q3 2026 (2027년 3월 1일 전) | 📜 |
| **플랫폼** | Web, iOS, Android, Samsung TV, LG TV | 📜 |
| **구독 모델** | $10 WSOP Plus / $50 WSOP Plus+ | 📜 |
| **화질** | 1080p Full HD | 📖 |
| **자막** | 20개국 다국어 지원 | 📖 |

### 1.2 YouTube 대비 핵심 차별점

> **출처**: 📜 VIBLE - "라이브 설정: 뒤로 가게도 할수 있게 하고, 끝나면 영상 남아있고"

| # | 차별점 | YouTube | WSOPTV | 원천 |
|:-:|--------|---------|--------|:----:|
| 1 | **Timeshift** | 뒤로 가기 불가 | 라이브 중 되감기 지원 | 📜 |
| 2 | **아카이브** | 종료 시 비공개 | 영구 보존 + VOD 전환 | 📜 |
| 3 | **Advanced Mode** | 없음 | Multi-view + StatsView | 📜 |
| 4 | **검색** | 없음 | 핸드/선수 기반 정밀 검색 | 📋 |

---

## 2. 콘텐츠 소싱 전략 `[Core-Vible]`

> **출처**: 📜 VIBLE - "Bracelet 대회가 1년에 대략 200개 있어요. 50개 정도 방송을 할거 같다."

### 2.1 콘텐츠 3단계 구조

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    연간 50개 방송 콘텐츠 소싱                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ESPN (10개/년)          PokerGO (10개/년)        WSOP 직접 (30개/년)   │
│  ┌───────────────┐       ┌───────────────┐       ┌───────────────┐     │
│  │ ESPN 방영 →   │       │ PokerGO 방영 →│       │ YouTube 라이브 │     │
│  │ 1년 후 WSOPTV │       │ 계약 후 WSOPTV│       │ + WSOPTV 동시  │     │
│  └───────────────┘       └───────────────┘       └───────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

| 소스 | 수량 | 특징 | 독점 기간 |
|------|:----:|------|----------|
| **ESPN** | 10개/년 | Main Event 등 → 1년 후 WSOPTV | 1년 |
| **PokerGO** | 10개/년 | High Roller 등 → 계약에 따라 | 계약 기간 |
| **WSOP 직접** | 30개/년 | YouTube + WSOPTV 동시 중계 | 없음 |

### 2.2 YouTube vs WSOPTV 설정 비교

> **출처**: 📜 VIBLE - "Youtube 로 라이브 중계 (라이브 설정: 뒤로 스크롤 안되기 + 끝나면 영상 비공개)"

| 설정 | YouTube | WSOPTV |
|------|---------|--------|
| DVR (Timeshift) | ❌ 비활성화 | ✅ 활성화 |
| 종료 후 | 비공개 전환 | 영구 보존 |
| 역할 | 맛보기/유입 채널 | 본 서비스 |

---

## 3. 구독 모델 `[Core-Vible]`

> **출처**: 📜 VIBLE - "$10, $50 두개 있음. Plus 라는건 구독이름."

### 3.1 2티어 구독

| 티어 | 가격 | 명칭 | 주요 기능 |
|------|------|------|----------|
| Basic | $10/월 | **WSOP Plus** | 라이브, VOD, Timeshift, 자막 |
| Premium | $50/월 | **WSOP Plus+** | Plus 기능 + Advanced Mode |

> **참고** (📜 VIBLE): "Exclusive Content (behind-the-scenes)는 굳이 WSOPTV 용으로 따로 제작하지 말자."

### 3.2 프로모션 전략

| Flow | 설명 |
|------|------|
| GG POKER → WSOPTV | $10 칩 구매 → WSOPTV Plus 구독권 자동 발급 |
| WSOPTV → GG POKER | Plus $10 구독 → GG POKER $10 칩 제공 |

---

## 4. Advanced Mode `[Core-Vible]`

> **출처**: 📜 VIBLE - "Multi-view 영상: 메인화면이 중앙에 있고, 각 유저들의 얼굴을 잡고 있는 화면이 옆에 또 있는 방식 (아이돌 직캠 카메라)"

### 4.1 Multi-view (📜 VIBLE + 📖 KORAN)

```
┌─────────────────────────────────────────────────────────────┐
│  ┌───────────────────────┐  ┌───────────────────────────┐   │
│  │  WSOP Main Event      │  │  $100K High Roller        │   │
│  │  Final Table          │  │  Day 2                    │   │
│  │  POT: $2.4M           │  │  POT: $890K               │   │
│  │  🔊 AUDIO             │  │                           │   │
│  └───────────────────────┘  └───────────────────────────┘   │
│  ┌───────────────────────┐  ┌───────────────────────────┐   │
│  │  Add a Table from     │  │  Super Circuit #12        │   │
│  │  Tournament Ticker    │  │  Heads Up                 │   │
│  │                       │  │  POT: $420K               │   │
│  └───────────────────────┘  └───────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  [Active Tables] [MultiView] [Featured Hands]  [1][2][4]    │
└─────────────────────────────────────────────────────────────┘
```

| 원천 | 기능 |
|:----:|------|
| 📜 | 메인화면 + 유저별 얼굴 화면 (아이돌 직캠 방식) |
| 📋 | 한 테이블 각 선수별 화면 재생 + 다른 대회/테이블 재생 |
| 📖 | 1x1, 1:2, 2x2 레이아웃 (NBA TV 동일) |

### 4.2 StatsView (📜 VIBLE)

> **출처**: 📜 VIBLE - "StatsView 영상: 허드같이 그 유저의 수치라든가, 플랍에서 베팅할 확률같은거, 이런게 띄어져있는 영상"

| 요소 | 표시 정보 |
|------|----------|
| 플레이어 통계 | VPIP, PFR, 3-Bet%, AF |
| 베팅 확률 | 플랍 베팅 확률, Pot Odds |
| 스택 정보 | 칩 카운트, BB 기준 스택 |

---

## 5. 핸드 태깅 & 검색 `[Core-Moses]`

> **출처**: 📋 MOSES - "대회 영상이나 Script를 기반으로 영상 태깅"

### 5.1 핸드 단위 태깅

| 태그 항목 | 설명 | 원천 |
|----------|------|:----:|
| Hand 기준 | 핸드 번호, 타임스탬프 | 📋 |
| 참여 플레이어 | 해당 핸드에 참여한 선수 목록 | 📋 |
| 각 플레이어 Hands | 홀카드 정보 | 📋 |
| Community Card | 보드 카드 (플롭/턴/리버) | 📋 |
| 최종 Winner | 핸드 승자 | 📋 |

### 5.2 검색 기능

> **출처**: 📋 MOSES - "특정 선수가 참여한 Pot 만 재생, 특정 핸드로 이기거나 진 핸드"

**검색 예제** (📋 MOSES):
- A 선수와 B 선수가 함께 했던 대회/동영상 검색
- 포카드(Four of a Kind)를 쥔 플레이어가 로열 스트레이트 플러시에게 패한 핸드
- 특정 핸드(AA, KK 등)로 이기거나 진 상황

---

## 6. 메인 스트리밍 UI - 7단 레이아웃 `[Core-Koran]`

> **출처**: 📖 KORAN - NBA TV League Pass 1:1 대응

### 6.1 레이아웃 구조

| 레이어 | NBA TV 컴포넌트 | WSOP TV 컴포넌트 |
|:------:|-----------------|------------------|
| ① | Scoreboard Ticker | Tournament Ticker |
| ② | Ad Banner | Ad Banner |
| ③ | Game Header | Tournament Header |
| ④ | Video Player | Video Player + POT/BOARD |
| ⑤ | Stream Tabs | Stream Tabs |
| ⑥ | Timeline | Timeline |
| ⑦ | Controls | Controls |

### 6.2 용어 매핑 (📖 KORAN)

| NBA TV | WSOP TV | 비고 |
|--------|---------|------|
| Scoreboard Ticker | Tournament Ticker | 상단 스코어/대회 표시 |
| Q3 3:05 | L38 LIVE | Quarter→Level |
| Clippers 77 / Bulls 90 | Negreanu 1.3M | 점수→칩 리더 |
| Key Plays | Featured Hands | 주요 플레이/핸드 |
| Box Score | Player Stats | 통계 탭 |
| Play-By-Play | Hand History | 액션 로그 |

---

## 7. Info Tabs `[Core-Koran]`

### 7.1 탭 구조 (📖 KORAN 동일)

| 탭 | NBA TV | WSOP TV |
|----|--------|---------|
| 1 | Summary | Summary |
| 2 | Box Score | Player Stats |
| 3 | Game Charts | Hand Charts |
| 4 | Play-By-Play | Hand History |

### 7.2 Player Stats 컬럼 매핑

| NBA TV | WSOP TV | 설명 |
|--------|---------|------|
| MIN | HANDS | 플레이 시간/핸드 |
| FGM | WINS | 성공 횟수 |
| FG% | WIN% | 성공률 |
| 3PM | VPIP | 팟 참여율 |
| REB | CHIPS | 칩 카운트 |

---

## 8. Player Controls `[Core-Koran]`

### 8.1 Core 컨트롤 (📖 KORAN 동일)

| 컨트롤 | 툴팁 | 단축키 |
|--------|------|--------|
| Play/Pause | Play/Pause | Space |
| Rewind | Rewind 10s | ← |
| Forward | Forward 10s | → |
| Volume | Volume | - |
| CC | Subtitles | c |
| MultiView | MultiView | Shift+m |
| PIP | Picture in Picture | p |
| Fullscreen | Fullscreen | f |
| Live | Jump to Live | Shift+→ |

### 8.2 Extension 컨트롤 (포커 전용)

| 컨트롤 | 기능 | 비고 |
|--------|------|------|
| [CARDS] | 홀카드 표시 토글 | 📜 VIBLE StatsView 확장 |
| [STACK] | 스택 오버레이 토글 | 📜 VIBLE StatsView 확장 |
| [EQUITY] | 에퀴티 미터 토글 | Extension |

---

## 9. 플랫폼 요구사항 `[Core-Vible]`

> **출처**: 📜 VIBLE - "WSOP TV B2B Requirement"

### 9.1 필수 요구사항

| 요구사항 | 상세 | 원천 |
|----------|------|:----:|
| **GGPass 로그인** | OAuth2 SSO 연동 | 📜📋 |
| **구독 모델** | $10 Plus / $50 Plus+ | 📜 |
| **역대 영상 업로드** | 모든 WSOP 영상 아카이브 | 📜 |
| **5개 스토어 배포** | App Store, Play Store, Samsung TV, LG TV, Web | 📜 |
| **Web 제공** | WSOP.TV 도메인 | 📜 |
| **View Mode 전환** | Normal ↔ Advanced Mode | 📜 |

### 9.2 제외 항목

| 항목 | 사유 | 원천 |
|------|------|:----:|
| 광고 시스템 | "굳이 고려할 필요없음" | 📜 |
| Exclusive Content | "따로 제작하지 말자" | 📜 |

---

## 10. 기술 요구사항

### 10.1 스트리밍 프로토콜

| 항목 | 스펙 |
|------|------|
| 프로토콜 | HLS, DASH |
| 화질 | 1080p (기본), 4K (프리미엄) |
| 비트레이트 | 3-15 Mbps 어댑티브 |
| 지연 | 30초 (라이브), 30분 (홀카드) |

### 10.2 비기능 요구사항

| 항목 | 목표치 |
|------|-------|
| 동시접속 | 50만 사용자 |
| 초기 버퍼링 | < 3초 |
| 재버퍼링 비율 | < 1% |
| DRM | Widevine, FairPlay, PlayReady |
| 서비스 가용성 | 99.9% |

---

## 11. 구현 우선순위 (Phase)

### Phase 1: Core-Vible (MVP) - 📜 VIBLE 필수

> **마감**: 2027년 3월 1일 전

| 기능 | 원천 | 우선순위 |
|------|:----:|:--------:|
| GGPass SSO 연동 | 📜 | P0 |
| $10/$50 구독 모델 | 📜 | P0 |
| 라이브 스트리밍 + Timeshift | 📜 | P0 |
| VOD 아카이브 | 📜 | P0 |
| 5개 플랫폼 배포 | 📜 | P0 |
| Advanced Mode (Multi-view + StatsView) | 📜 | P0 |

### Phase 2: Core-Moses (검색 강화) - 📋 MOSES 확장

| 기능 | 원천 | 우선순위 |
|------|:----:|:--------:|
| 핸드 단위 태깅 시스템 | 📋 | P1 |
| 선수/핸드 검색 | 📋 | P1 |
| 멀티 재생 (다른 대회/테이블) | 📋 | P1 |
| 특수 검색 (배드 비트, 쿨러 등) | 📋 | P2 |

### Phase 3: Core-Koran (UX 완성) - 📖 KORAN 1:1

| 기능 | 원천 | 우선순위 |
|------|:----:|:--------:|
| Tournament Ticker | 📖 | P1 |
| Info Tabs (Summary/Stats/Charts/History) | 📖 | P1 |
| Featured Hands 모달 | 📖 | P1 |
| Streaming Options (Camera/Commentary) | 📖 | P2 |

### Phase 4: Extension (확장)

| 기능 | 우선순위 |
|------|:--------:|
| Equity Calculator | P3 |
| Hand Range Display | P3 |
| 3x3 MultiView (파이널 데이용) | P3 |
| 4K 화질 | P3 |

---

## 12. Scope

### In Scope (MVP)

| 항목 | 설명 | 원천 |
|------|------|:----:|
| 플랫폼 | Web, iOS, Android, Samsung TV, LG TV | 📜 |
| 화질 | 1080p Full HD | 📖 |
| Multi-view | 1x1, 1:2, 2x2 | 📜📖 |
| 자막 | 20개국 | 📖 |
| 메뉴 | Watch + Collections | - |

### Out of Scope

| 항목 | 사유 | 원천 |
|------|------|:----:|
| 광고 시스템 | VIBLE 제외 | 📜 |
| Exclusive Content | VIBLE 제외 | 📜 |
| 4K 지원 | Phase 4 | - |
| Roku/Fire TV | Phase 4 | - |

---

## 13. 앱 배포 계획 `[Core-Vible]`

> **출처**: 📜 VIBLE - "WSOP 회사 애플 계정 (Bracelet IP, Ireland 회사) 으로 앞으로 올릴 것들"

### 13.1 배포 앱 목록

| 앱 | 설명 | 마감 |
|----|------|------|
| WSOP Live | WSOP+에서 이름 변경 필요 | 2027.03.01 |
| **WSOP TV** | 본 서비스 | 2027.03.01 |
| WSOP Academy | 교육 콘텐츠 | TBD |
| PokerStake | 스테이킹 서비스 | TBD |

### 13.2 배포 스토어

- Apple App Store
- Google Play Store
- Samsung TV Store
- LG TV Store
- Web (WSOP.TV)

---

## 14. Open Questions

1. TV 미러링/캐스팅 지원 여부
2. 블랙아웃 정책 (사이트 단위 vs 영상 단위)
3. 핸드 태깅 자동화 vs 수동 입력 비율

---

## 15. References

### 3대 원천 문서
- 📜 **VIBLE**: [michael_note.md](../vible/michael_note.md) - 운영 계획의 근간
- 📋 **MOSES**: [tony_note.md](../vible/tony_note.md) - 첨언 및 확장
- 📖 **KORAN**: [WSOP-TV-PRD.md](C:\claude\wsoptv_nbatv_clone\docs\guides\WSOP-TV-PRD.md) - NBA TV 1:1 대응

### 기능 문서
- [PRD-0006 Advanced Mode](PRD-0006-advanced-mode.md) - Advanced Mode 상세 스펙
- [PRD-0009 Hand Tagging & Search](PRD-0009-hand-tagging-search.md) - 핸드 태깅 및 검색

### 전략 문서
- [STRAT-0001 Viewer Experience Vision](../strategies/STRAT-0001-viewer-experience-vision.md) - 시청자 경험 비전
- [STRAT-0007 Content Sourcing](../strategies/STRAT-0007-content-sourcing.md) - 콘텐츠 소싱

---

## Revision History

| 버전 | 날짜 | 작성자 | 내용 |
|------|------|--------|------|
| 1.0 | 2026-01-07 | Claude Code | 최초 작성 |
| 2.0 | 2026-01-16 | Claude Code | Problem Statement 수정, 3계층 구조 |
| 3.0 | 2026-01-19 | Claude Code | STRAT-0001 참조, YouTube 대비 차별점 |
| 4.0 | 2026-01-22 | Claude Code | NBA TV 1:1 구조로 개편 |
| **5.0** | **2026-01-22** | **Claude Code** | **3대 원천 기반 전면 개편**: VIBLE(Michael) > MOSES(Tony) > KORAN(NBA TV) 우선순위 체계, 원천별 기능 분류, Phase 재정렬 |
