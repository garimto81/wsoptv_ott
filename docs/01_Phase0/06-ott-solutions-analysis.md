# Phase 0-06: OTT 솔루션 시장 분석

| 항목 | 값 |
|------|---|
| **Phase** | 0 (준비 단계) |
| **Version** | v2.0.0 |
| **Status** | Active |
| **Date** | 2026-02-10 |
| **Author** | Claude Code |
| **Depends** | [01-vision](../99_Archive_ngd/phase0/01-vision.md), [03-vendor-rfp](../99_Archive_ngd/phase0/03-vendor-rfp.md) |

---

## 분석 목적

WSOPTV Phase 0 업체 선정을 위해 2026년 현재 업계 주요 스포츠 OTT 솔루션의 장단점을 비교 분석한다. Phase 1 MVP Vimeo 선택의 타당성을 검증하고, Phase 2+ 확장 전략의 근거 자료를 제공한다.

### WSOPTV 조건

| 항목 | 값 |
|------|---|
| 예산 | 연 $100K 이내 |
| 론칭 목표 | Q3 2026 |
| UX 레퍼런스 | NBA TV 스타일 |
| 핵심 기능 | 라이브 + VOD + 선수 프로필 |
| Phase 1 결정 | Vimeo SaaS 기반 |

---

## Bending Spoons 리스크 (CRITICAL)

> **2025~2026년 Vimeo와 Brightcove가 동일 기업에 인수되었으며, 대규모 인력 감축이 진행되었다.**

| 사건 | 날짜 | 내용 |
|------|------|------|
| Brightcove 인수 | 2025-02 | Bending Spoons이 $233M에 인수 완료 |
| Brightcove 정리해고 | 2025-03 | 600명 중 198명 감원 (미국 직원 2/3) |
| Vimeo 인수 | 2025-11 | Bending Spoons이 $1.38B에 인수, Nasdaq 상장폐지 |
| Vimeo 정리해고 | 2026-01 | 1,000명+ 감원, **비디오 엔지니어링팀 전원 해고** |
| Vimeo 잔여 인력 | 2026-02 | 약 15명 엔지니어 + 임시 유지보수 인력 (4월까지) |

**Bending Spoons 패턴**: WeTransfer(75% 감원), Filmic(전원 해고), Meetup(유럽 이전)

### WSOPTV 영향 평가

| 항목 | 리스크 | 대응 |
|------|--------|------|
| Vimeo OTT 서비스 지속성 | **HIGH** — 유지보수 모드 전환 가능성 | 계약 시 SLA/Exit 조항 필수 |
| Vimeo 기술 지원 | **HIGH** — 엔지니어링팀 해체 | Senior Engineer 배정 재확인 |
| Brightcove 대안 가치 | **MEDIUM** — 동일 모기업 리스크 | 독립 대안 확보 필요 |
| Phase 2+ 마이그레이션 | **LOW** — 어차피 전환 계획 | 오히려 전환 동기 강화 |

> **권고**: Vimeo 계약 시 **12개월 이내 데이터 이관 보장 조항** 및 **서비스 중단 시 위약금 조항** 협상 필수. 동시에 **ViewLift, Uscreen**을 대안으로 사전 검토.

---

## 1차 그룹: 스포츠 OTT 전문

### 1.1 Vimeo OTT (현재 선택)

**포지션**: SaaS 올인원 | **주요 고객**: 소규모~중규모 스포츠 리그

**가격**: 구독자당 $1/월 + 거래당 10% + $0.50. WSOPTV 1차 견적: $42.5K ~ $388K

| 강점 | 약점 |
|------|------|
| 턴키 솔루션 (Web/iOS/Android/TV 자동) | **Bending Spoons 인수 후 엔지니어링팀 해체** |
| 빠른 출시 (개발 최소화) | 구독자 증가 시 비용 급증 |
| 4K/HDR + Google Cloud CDN | 스포츠 특화 기능 부족 |
| SVOD/TVOD/AVOD 지원 | API 제한 |
| 저렴한 초기 비용 | 플랫폼 종속성 + 서비스 지속성 불확실 |

**WSOPTV 적합도**: **HIGH** (Phase 1) — 빠른 론칭, 예산 충족. 단, **Bending Spoons 리스크 주시 필수**

### 1.2 Brightcove

**포지션**: 엔터프라이즈 PaaS | **주요 고객**: 대형 스포츠 리그, 방송사

**가격**: WSOPTV 견적 $1,735,949 (예산 17배 초과)

| 강점 | 약점 |
|------|------|
| 대규모 동시 시청자 처리 검증 | 매우 높은 비용 |
| 라이브 스트리밍 + 이벤트 자동화 | **Bending Spoons 인수 → 미국 직원 2/3 감원** |
| 글로벌 CDN 스케일링 | Vimeo와 동일 모기업 리스크 |
| 심층 분석 대시보드 | WSOP 초기 규모에 오버스펙 |

**WSOPTV 적합도**: **LOW** — 비용 초과 + Bending Spoons 리스크 이중 부담

### 1.3 Deltatre + Endeavor Streaming (VESPER)

**포지션**: 글로벌 스포츠 OTT 1위 | **플랫폼**: VESPER

> Deltatre가 2025년 중반 Endeavor Streaming을 인수하여 통합. Endeavor Streaming은 2018년 NeuLion($250M)을 인수하여 형성.

**주요 고객**: NFL, NBA, MLB, UFC, WWE, WNBA, LIV Golf, ICC, World Rugby, UEFA, Sky, Rogers, BritBox, Bell Media

| 강점 | 약점 |
|------|------|
| **세계 최대 스포츠 스트리밍 고객 포트폴리오** | 엔터프라이즈 전용 (소규모 부적합) |
| UFC Fight Pass, WNBA League Pass 직접 운영 | 가격 불투명 (대형 계약 위주) |
| VESPER + D3 VOLT + FORGE + AXIS 통합 플랫폼 | 커스텀 구축 기간 6개월+ |
| PPV + SVOD + AVOD 하이브리드 검증 | 포커 특화 경험 없음 (격투기/팀스포츠 중심) |
| **PokerGO가 NeuLion/Endeavor 사용 (직접 레퍼런스)** | - |

**WSOPTV 적합도**: **LOW** (Phase 1 예산 초과), **HIGH** (Phase 3 — PokerGO 전례)

### 1.4 StreamAMG

**포지션**: 스포츠 전문 에이전시 | **주요 고객**: UEFA, Premier League 클럽

**가격**: 커스텀 견적 (비공개)

| 강점 | 약점 |
|------|------|
| 10년+ 스포츠 OTT 전문 | 가격 비공개 |
| 풀스택 서비스 (기술+운영+전략) | 유럽 중심, 미국 레퍼런스 부족 |
| UEFA 레퍼런스 | 에이전시 모델 종속성 |
| DRM/보안 전문 | 소규모 프로젝트 대응 불명확 |

**WSOPTV 적합도**: **MEDIUM** — 스포츠 전문성 우수, 가격/지역 불확실

### 1.5 ViewLift (v2.0 신규)

**포지션**: 스포츠 특화 OTT SaaS | **주요 고객**: NHL, LIV Golf, 16개 미국 프로 스포츠팀, 6개 RSN

> Monumental Sports & Entertainment(워싱턴 위저즈/캐피탈즈) 등 미국 프로 스포츠 최다 고객 보유

**가격**: 커스텀 견적 (엔터프라이즈급, 비공개)

| 강점 | 약점 |
|------|------|
| NHL, LIV Golf 등 **미국 프로 스포츠 최다 고객** | 가격 비공개 (엔터프라이즈급 추정) |
| 멀티앵글, 실시간 통계, 소셜 통합 내장 | Vimeo 대비 초기 비용 높을 가능성 |
| 12+ 수익화 모델 (AVOD/SVOD/TVOD/하이브리드) | WSOPTV 규모에 오버스펙 가능 |
| AI 개인화 추천 | 포커 특화 경험 없음 |
| AppCMS + 커스텀 앱 빌더 | - |

**WSOPTV 적합도**: **MEDIUM** (Phase 1 — Vimeo 대안 후보), **HIGH** (Phase 2+)

### 1.6 Kiswe (v2.0 신규)

**포지션**: 멀티뷰 스트리밍 전문 | **플랫폼**: Kiswe Core + Kiswe Connect

**주요 고객**: NBA팀 (Utah Jazz, Phoenix Suns, New Orleans Pelicans), BTS, The Rolling Stones

| 강점 | 약점 |
|------|------|
| **멀티뷰 스트리밍 전문** (WSOPTV Phase 2+ 직접 관련) | 풀스택 OTT 솔루션 아님 (멀티뷰 특화) |
| NBA팀 RSN 탈피 → D2C 전환 검증 | 자체 앱/CMS 없음 (다른 플랫폼과 조합 필요) |
| Kiswe Core: 멀티 플랫폼 동시 배포 | 라이브 이벤트 중심 (VOD 약함) |
| 극장 멀티앵글 송출 실적 (KBO) | - |

**WSOPTV 적합도**: **LOW** (Phase 1), **HIGH** (Phase 2+ 멀티뷰 구현 시 핵심 파트너 후보)

---

## 2차 그룹: SaaS 대안 (Vimeo OTT 리스크 대응)

### 2.1 Uscreen (v2.0 신규)

**포지션**: Vimeo OTT 직접 대안 SaaS

**가격**: $149/월 (Growth) ~ $499/월 (Plus) + 구독자당 $1/월 또는 거래당 10%

| 강점 | 약점 |
|------|------|
| Vimeo OTT와 거의 동일한 기능셋 | 대규모 스포츠 레퍼런스 부족 |
| iOS/Android/TV 앱 템플릿 제공 | 엔터프라이즈 스케일 미검증 |
| 커뮤니티 기능 (라이브 챗, 포럼) | 스포츠 특화 기능 없음 |
| SVOD/TVOD/PPV 지원 | Vimeo 대비 커스터마이징 유연성 낮음 |
| **Bending Spoons 리스크 없음** (독립 기업) | - |

**WSOPTV 적합도**: **MEDIUM** — Vimeo 리스크 현실화 시 **최우선 대안**

### 2.2 Muvi One (v2.0 신규)

**포지션**: 화이트라벨 OTT 올인원 | **포커 공식 지원**

**가격**: Standard $399/월 ($4.8K/년) | Professional $1,499/월 ($18K/년, 4K+라이브) | Enterprise $3,900/월 ($47K/년)

> **Muvi는 포커 토너먼트 스트리밍을 공식 마케팅하는 유일한 OTT 플랫폼**

| 강점 | 약점 |
|------|------|
| **포커 토너먼트 스트리밍 공식 지원** (가이드 문서 존재) | Vimeo 대비 브랜드 인지도 낮음 |
| Professional $18K/년 (Vimeo $42.5K 대비 57% 저렴) | 대규모 스포츠 레퍼런스 부족 |
| 1,000+ 기능, 4K, DRM, 글로벌 결제 | 앱 UI 커스터마이징 깊이 미확인 |
| iOS/Android/TV 앱 + 웹 빌더 | 엔터프라이즈 스케일 미검증 |
| 30일 무료 트라이얼 | - |

**WSOPTV 적합도**: **HIGH** — 포커 공식 지원 + 예산 내 ($18K) + 앱 포함. **Vimeo 리스크 대안 최유력 후보**

### 2.3 Dacast

**포지션**: 라이브 스트리밍 + VOD 호스팅 SaaS

**가격**: $39/월 (Starter) ~ $188/월 (Scale), 엔터프라이즈 별도

| 강점 | 약점 |
|------|------|
| 저렴한 가격 ($468/년~) | OTT 앱 없음 (웹 플레이어 위주) |
| CDN 멀티 네트워크, PPV 지원 | 스포츠 특화 기능 없음 |
| 화이트라벨 지원 | 커스텀 앱 별도 개발 필요 |

**WSOPTV 적합도**: **LOW** — 앱 미지원으로 MVP 요건 미충족

---

## 3차 그룹: 인프라/부분 솔루션

### 3.1 AWS IVS

**포지션**: 클라우드 PaaS | **기술 기반**: Twitch 기반

| 강점 | 약점 |
|------|------|
| WebRTC 0.5초 이하 저지연 | 프론트/백엔드 직접 구축 필수 |
| AWS 자동 스케일링 | 앱 개발 비용 별도 |
| API/SDK 완전 개방 | 24/7 운영팀 필요 |
| 사용량 기반 과금 | UI/UX 자체 구축 |

**WSOPTV 적합도**: **LOW** (Phase 1), **HIGH** (Phase 3 자체 개발)

### 3.2 AWS Elemental (MediaLive + MediaPackage)

**포지션**: 방송급 인프라 | **주요 고객**: FOX SPORTS

| 강점 | 약점 |
|------|------|
| TV 표준 인코딩 품질 | 아키텍처 설계 비용 높음 |
| 대규모 스포츠 중계 검증 | 방송 엔지니어링 지식 필요 |
| DRM 내장, DVR 자동 | 여러 AWS 서비스 조합 필수 |

**WSOPTV 적합도**: **LOW** (Phase 1), **MEDIUM** (Phase 2 백엔드 보강)

### 3.3 Bitmovin

**포지션**: 인코딩/플레이어 전문

| 강점 | 약점 |
|------|------|
| Nvidia GPU 가속 인코딩 | 부분 솔루션 (CMS/앱 별도) |
| 저지연 라이브 최적화 | 다른 서비스와 통합 필수 |
| 스토리지/대역폭 절감 | 스포츠 특화 기능 없음 |

**WSOPTV 적합도**: **LOW** (Phase 1), **MEDIUM** (Phase 3 성능 최적화 부분 도입)

### 3.4 MUX (v2.0 신규)

**포지션**: 비디오 API 플랫폼 (개발자 친화적)

| 강점 | 약점 |
|------|------|
| 개발자 친화적 API/SDK | 풀스택 OTT 아님 |
| 실시간 분석 + 모니터링 | 앱/CMS 자체 구축 필요 |
| 사용량 기반 과금 (소규모 적합) | 스포츠 특화 기능 없음 |

**WSOPTV 적합도**: **LOW** — AWS IVS와 유사 포지션, Phase 3 부분 검토

### 3.5 JWP Connatix (합병)

**포지션**: 비디오 플레이어 + 광고 수익화

| 강점 | 약점 |
|------|------|
| AVOD 최적화 (월 300억+ 광고) | 광고 중심, SVOD 부적합 |
| 업계 표준 비디오 플레이어 | 풀스택 OTT 아님 |

**WSOPTV 적합도**: **LOW** — SVOD 중심 WSOPTV와 모델 불일치

### 3.6 Wowza

**포지션**: 커스텀 스트리밍 서버

| 강점 | 약점 |
|------|------|
| WebRTC 0.5초 이하 저지연 | 앱/CMS/CDN 모두 자체 구축 |
| 온프레미스 + 클라우드 하이브리드 | 스트리밍 엔지니어 필수 |

**WSOPTV 적합도**: **LOW** — 자체 기술팀 보유 시에만 고려

---

## 벤치마크: 직접 경쟁사 + 대형 스포츠 OTT

### PokerGO (직접 경쟁사 — v2.0 신규)

> **WSOPTV의 가장 직접적인 비교 대상**. 유일한 포커 전용 OTT 스트리밍 서비스.

| 항목 | 값 |
|------|---|
| **연 매출** | $7.5M (2025년 기준) |
| **구독료** | $14.99/월, $24.99/분기, $99.99/연 |
| **기술 스택** | NeuLion → Endeavor Streaming → Deltatre VESPER |
| **시청 디바이스** | 모바일 38%, 데스크톱 37%, 태블릿 13%, 커넥티드 TV 12% |
| **콘텐츠** | 연 100일+ 라이브 (WSOP 독점 스트리밍 권리 보유) |
| **방송 파트너** | CBS Sports (다년 계약 — Main Event 15시간 + 골드 브레슬릿 36시간) |
| **인프라** | ARIA Resort 내 10,000 sq ft 전용 스튜디오 (300명 수용) |
| **최근 동향** | 2024년 PokerGFX 인수, FAST 채널(Pluto TV) 확장 |

**시사점**:
- 포커 OTT도 **모바일 퍼스트** 설계 필수 (38% 모바일)
- FAST 채널 전략으로 무료 노출 → 유료 전환 유도
- 실시간 그래픽/통계 내재화 (PokerGFX 인수)가 차별화 핵심
- **TV + OTT 하이브리드**: CBS Sports 파트너십으로 대중 노출 확보
- 구독자 수 비공개 → 포커 OTT 시장 규모 추정 어려움
- **WSOPTV 가격 참고**: PokerGO $9.99~$14.99 vs WSOP Plus $9.99 (유사 가격대)

### DAZN

- AWS Lambda 서버리스 + Step Functions
- React + Mobx 프론트엔드
- 써드파티 의존 → 자체 플랫폼 전환 완료
- **시사점**: 구독자 규모 성장 시 자체 개발이 비용 효율적

### ESPN DTC (2025년 8월 론칭)

- ESPN Unlimited: NFL Network 통합, 멀티게임 동시 시청
- AI 앵커: 개인화 콘텐츠
- 멀티뷰: 커스터마이징 가능한 멀티게임 레이아웃
- Disney+ 앱 내 ESPN 허브 통합
- **시사점**: 멀티뷰, 통계 동기화가 스포츠 OTT UX 표준

### NBA League Pass (Amazon Prime Video)

- AWS 인프라 기반
- FanDuel 실시간 베팅 통합
- **시사점**: 리그 직영 → 대형 플랫폼 파트너십 전환 트렌드

### UFC Fight Pass

- Endeavor Streaming VESPER 기반
- PPV + SVOD 하이브리드 수익 모델
- **시사점**: 니치 격투기 스포츠 OTT 성공 모델, WSOPTV와 유사한 팬덤 기반

---

## 종합 비교

| 솔루션 | 라이브 | VOD | 수익화 | 가격 | 스포츠 | 커스텀 | 안정성 | WSOPTV P1 |
|--------|:------:|:---:|:------:|:----:|:------:|:------:|:------:|:---------:|
| **Vimeo OTT** | 4 | 4 | 4 | 5 | 2 | 2 | ⚠️ 2 | **HIGH** |
| **ViewLift** | 5 | 4 | 5 | 2 | 5 | 4 | 4 | **MEDIUM** |
| **Muvi One** | 4 | 4 | 4 | 5 | 3 | 3 | 4 | **HIGH** |
| **Uscreen** | 4 | 4 | 4 | 4 | 2 | 2 | 4 | **MEDIUM** |
| Deltatre/Endeavor | 5 | 5 | 5 | 1 | 5 | 5 | 5 | LOW |
| Brightcove | 5 | 5 | 5 | 1 | 3 | 4 | ⚠️ 2 | LOW |
| StreamAMG | 5 | 4 | 4 | 2 | 5 | 3 | 4 | MEDIUM |
| Kiswe | 5 | 2 | 3 | 3 | 4 | 4 | 4 | LOW |
| AWS IVS | 5 | 3 | 3 | 4 | 2 | 5 | 5 | LOW |
| AWS Elemental | 5 | 5 | 4 | 3 | 3 | 5 | 5 | LOW |
| Bitmovin | 5 | 4 | 3 | 3 | 3 | 4 | 4 | LOW |
| MUX | 4 | 3 | 3 | 4 | 2 | 5 | 4 | LOW |
| JWP Connatix | 3 | 4 | 5 | 3 | 2 | 3 | 4 | LOW |
| Wowza | 5 | 4 | 3 | 3 | 3 | 5 | 4 | LOW |

> 점수: 1(최저) ~ 5(최고). 가격은 WSOPTV 예산 $100K 기준 충족도. **안정성** 열 추가 (v2.0).

---

## Phase별 추천 전략 (v2.0 수정)

### Phase 1 MVP (Q3 2026) — Vimeo + 대안 준비

**Vimeo OTT** 유지하되 리스크 대응 필수.

| 조치 | 우선순위 | 상세 |
|------|:--------:|------|
| Vimeo 계약 시 Exit 조항 | P0 | 12개월 이내 데이터 이관 보장, 서비스 중단 위약금 |
| Muvi One 트라이얼 (30일 무료) | P1 | **포커 공식 지원**, $18K/년, Vimeo 대안 최유력 |
| ViewLift 사전 RFP | P1 | Vimeo 대안 2순위, 스포츠 특화 기능 우수 |
| Uscreen 트라이얼 | P2 | 라이브 시간 제한 ($15/시간 초과) 확인 필요 |
| Vimeo 분기별 서비스 상태 점검 | P2 | Bending Spoons 후속 조치 모니터링 |

### Phase 2 Advanced (2027 H1) — 멀티뷰 + 하이브리드

| 시나리오 | 전략 | 추정 비용 |
|----------|------|----------|
| A: Vimeo 안정 시 | Vimeo + Kiswe(멀티뷰) 하이브리드 | +$50K~100K |
| B: Vimeo 불안정 시 | ViewLift 전환 + Kiswe 멀티뷰 | RFP 필요 |
| C: 자체 개발 착수 | AWS IVS(라이브) + Vimeo(VOD) | +$200K |
| D: StreamAMG 컨설팅 | 스포츠 특화 기능 자문 | RFP 필요 |

### Phase 3 글로벌 (2028+) — 장기 계획

구독자 5만+ 도달 시 PokerGO 모델 참고:
- **Deltatre VESPER** 기반 전환 검토 (PokerGO 전례)
- 또는 DAZN 모델 자체 플랫폼: AWS 서버리스 + React + CloudFront
- 예상 개발: $2M~$3M (18개월)
- ROI 분기점: 24개월

---

## 포커 OTT 시장 현황

| 항목 | 값 |
|------|---|
| **PokerGO** | 유일한 포커 전용 OTT, $7.5M 매출, WSOP 독점 권리 |
| **GGPoker TV** | OTT 없음, YouTube/Twitch 의존, Streamer Mode 출시 (2025) |
| **888poker** | OTT 없음, WSOP US 소프트웨어 제공 (2026 만료) |
| **Twitch 포커** | 시청률 **44.2% 급락** (2025 vs 2024) — 온라인 포커 스트리밍 침체 |
| **온라인 포커 시장** | $6.27B (2025) → $22.40B (2034), CAGR 15.2% |
| **토너먼트 수익 비중** | 전체 포커 플랫폼 수익의 45% (스폰서십, 광고, 프리미엄 멤버십) |

> **핵심**: 포커 OTT 시장에서 PokerGO 외 경쟁자가 없는 상태. Twitch 포커 시청률 급락은 **라이브 토너먼트 중계의 프리미엄 가치**가 높아짐을 의미. 온라인 포커 시장 자체는 CAGR 15.2%로 고성장 중.

### 니치 스포츠 OTT 진화 패턴

| 단계 | 전략 | 사례 |
|------|------|------|
| **초기 (MVP)** | SaaS 활용 (Vimeo, Dacast) | WSOPTV (현재) |
| **성장기** | 전문 플랫폼 전환 | UFC Fight Pass (NeuLion → Endeavor) |
| **성숙기** | 대형 플랫폼 파트너십 | PGA Tour (ESPN+), WWE (Peacock) |
| **전환 결정** | "콘텐츠 회사 vs 기술 회사" 정체성 선택 | WWE: "우리는 콘텐츠 회사" → Peacock 전환으로 시청률 42% 증가 |

> **주의**: 검색 결과에서 **포커/니치 스포츠가 Vimeo OTT를 사용하는 사례는 발견되지 않음**. Vimeo OTT는 독립 크리에이터/중소 미디어 위주.

---

## 2026년 시장 트렌드

1. **저지연 표준화**: WebRTC 0.5초 이하 보편화
2. **멀티뷰**: 동시 시청 기능 표준화 (ESPN+, DAZN, Kiswe)
3. **실시간 통계**: 스코어/선수 데이터 오버레이
4. **AI 개인화**: 추천 + 하이라이트 자동 생성
5. **베팅 통합**: FanDuel/DraftKings 파트너십 확산
6. **하이브리드 수익화**: SVOD + AVOD + PPV + FAST 채널 동시 운영
7. **플랫폼 통합**: Bending Spoons(Vimeo+Brightcove), Deltatre(+Endeavor) 등 M&A 가속
8. **D2C 전환**: NBA팀 RSN 탈피 → Kiswe/ViewLift 기반 자체 스트리밍
9. **TV+OTT 하이브리드**: PokerGO+CBS, PGA+ESPN+ 등 전통 TV 파트너십 병행

**시장 규모**: 2024년 $33.9B → 2025년 $31.9B~$33.9B → 2030년 $68.3B~$75.2B (CAGR 12.6%~15%)

> 출처: Grand View Research, Research and Markets (2025)

---

## 관련 문서

| 문서 | 역할 |
|------|------|
| [03-vendor-rfp](../99_Archive_ngd/phase0/03-vendor-rfp.md) | 업체 선정 경과 |
| [05-competitor-ott-analysis](05-competitor-ott-analysis.md) | NFL/MLB/ESPN+ 레퍼런스 |
| [01-mvp-spec](../02_Phase1/01-mvp-spec.md) | Vimeo 기반 MVP 스펙 |
| [VENDOR-DASHBOARD](../99_Archive_ngd/management/VENDOR-DASHBOARD.md) | 업체 현황 대시보드 |

---

## 변경 이력

| 버전 | 날짜 | 작성자 | 내용 |
|------|------|--------|------|
| v2.0.0 | 2026-02-10 | Claude Code | Web research 3건 병렬 검증. 14개 플랫폼 + 5개 벤치마크. Bending Spoons 리스크 CRITICAL. Muvi One(포커 공식 지원, $18K/년) 발견. ViewLift/Kiswe/Uscreen/Dacast/MUX/Muvi 6개 신규. PokerGO 상세($7.5M, CBS, Deltatre). 포커 시장 데이터($6.27B→$22.4B). Phase 전략 전면 수정 |
| v1.0.0 | 2026-02-10 | Claude Code | 9개 솔루션 + 3개 벤치마크 분석, Phase별 추천 전략 |
