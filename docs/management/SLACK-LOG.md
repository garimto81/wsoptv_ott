# WSOPTV 슬랙 관리 로그

**최종 업데이트**: 2026-02-02 09:00

---

## 요약 대시보드

| 구분 | 미완료 | 진행 중 | 완료 |
|------|:------:|:------:|:----:|
| 의사결정 | 1 | 0 | 1 |
| 액션 아이템 | 2 | 1 | 3 |

---

## 미완료 액션 아이템

### 🔴 @Aiden - PRD-0002 v10.1 업데이트 (D+1)
- **출처**: #wsoptv-dev, 2026-02-01
- **요청자**: @Michael
- **기한**: 2026-02-05
- **상태**: 진행 중
- **내용**: MVP 범위 변경(Single-Stream) 반영

### 🟡 @Aiden - 메가존 SLA 강화 조항 검토
- **출처**: #wsoptv-biz, 2026-02-01
- **요청자**: @Tony
- **기한**: 2026-02-08
- **상태**: 미시작
- **내용**: 계약 시 SLA 99.9% → 99.95% 강화 가능성 검토

---

## 최근 의사결정

### DEC-2026-0201-001: MVP 범위 확정 (Single-Stream)
- **일시**: 2026-02-01 14:30
- **참여자**: @Michael, @Tony, @Aiden
- **결정 사항**:
  - MVP = Single-Stream (Multi-view 제외)
  - Phase 2에서 Multi-view 추가
- **근거**:
  - 일정 리스크 감소 (3개월 단축)
  - 초기 비용 50% 절감 (구축비 약 25억 절감)
  - 핵심 가치(Timeshift, 아카이브) 우선 검증
- **후속 조치**:
  - [x] 스프린트 계획 재조정
  - [ ] PRD-0002 v10.1 업데이트
  - [ ] 메가존에 수정 견적 요청

---

## 슬랙 로그 (최신순)

### 2026-01-26

#### 16:23 - #C09TX3M1J2W
<!-- ts: 1769412236.271329 -->
> @aiden.kim: *[ Vimeo 미팅 스케줄 협의 ]*
사전에 예정되어 있던 비메오와의 미팅 스케줄을 확정하려고 합니다
1/29 15:00 에 진행하려고 하는데 다들 시간이 어떠신지요?
<@U09HF1166LQ> <@U0NPV0M29> <@U05U07C1HND> <@U22GJU5JT> <@U05CSNCKS4V>

**결정**: ✅ (요약 필요)

#### 16:14 - #C09TX3M1J2W
<!-- ts: 1769411699.894589 -->
> @aiden.kim: *[ WSOPTV 핵심 시스템 설계 방향 및 의사결정 요청 }*

WSOPTV OTT 업체 선정과정에서 미비된 기획으로 인해 생기는 혼선을 방지하고자 Concept Paper 를 작성하였습니다
컨셉 문서치고는 무척 긴데 파편화된 아이디어들을 제거하고,
최대한 명확한 정의만을 정리하려고하보니 길어지게 되었습니다
<https://docs.google.com/document/d/1Y5KMRFunHJEXmR0MrXbb_flmf-_88obGnJBe0AC94_A/edit?tab=t.0|[WSOPTV Concept Paper]>
첨부자료 <https://docs.google.com/document/d/1VE0StXfXN5-cUGXSLFTNp280VgTHxEHgRHaDrNUtBBo/edit?tab=t.0|[NBATV OTT 분석 자료]>

1.  OVP (Online Video Platform 서비스)
• *현황:* 업체별 기술 차이 미미함.
• *핵심:* POKERGO → WSOP 스토리지 이전 및 클라우드 업로드 절차 관리에 집중.
2.  Multi-View
구현 범위에 따라 *현장 인프라 비용*이 결정됩니다.
• *Option 1. 테이블 중심 :* 현재 제작 방식 유지. 테이블 단위 멀티뷰 제공.
• *Option 2. 키 플레이어 :* 인물 중심 추적 송출. 제작팀 지향 방식이나 전송 시스템 수정 필요.
• *Option 3. 개인 직캠 :* 전 플레이어 개별 캠 제공. 제작 및 전용 회선 인프라 전체 재설계 필요.
3. Stats View
노출 방식에 따라 개발 주체(플랫폼 vs 제작팀)가 달라집니다.
• *Option 1. 페이지형:* 별도 정보 레이어 활용. 기술적 구현 가장 용이.
• *Option 2. 오버레이:* 영상 내 자막 삽입. 프로덕션 제작팀의 자막 기능 추가 필요.
• *Option 3. HUD 동기화:* 플레이어와 실시간 수치 동기화. 비디오 플레이어의 대대적인 커스텀 필요.
<@U09HF1166LQ> <@U0NPV0M29> <@U22GJU5JT> <@U05U07C1HND> <@U05CSNCKS4V>

**결정**: ✅ (요약 필요)


### 2026-01-27

#### 17:43 - #C09TX3M1J2W
<!-- ts: 1769503398.227719 -->
> @aiden.kim: [ GGPRDUCTION 방송 아키텍처 ]


### 2026-01-28

#### 18:58 - #C09TX3M1J2W
<!-- ts: 1769594282.438219 -->
> @aiden.kim: [ WSOPTV 아이디어 목업 디자인 ]

#### 18:44 - #C09TX3M1J2W
<!-- ts: 1769593490.661109 -->
> @tony.park: <@U09HF1166LQ>
(아실거라 생각하지만) 마이클님 한국에 오셨습니다
방금 저희 팀과 회의 진행하셨어요

#### 18:42 - #C09TX3M1J2W
<!-- ts: 1769593354.159169 -->
> @ken.ahn: 구독 페이먼트 형태는 넷플릭스 처럼 외부 웹페이지에서 구독 결재를 하는 형태로 시도해 보기로 했습니다.


### 2026-01-29

#### 20:10 - #C09TX3M1J2W
<!-- ts: 1769685032.689109 -->
> @ken.ahn: Vimeo 쪽은 뭔가 방향을 잘 못 잡고 온 것이 아닌가 싶어요

#### 16:40 - #C09TX3M1J2W
<!-- ts: 1769672406.593229 -->
> @ken.ahn: 딱히 채널이 없어서 요기에 공유합니다.
*[Microsoft Office OLE 보안 기능 우회 취약점 - CVE-2026-21509]*

안녕하세요. CTI 팀입니다.
Microsoft Office에서 CVSS 7.8 High 등급의 보안 기능 우회(Security Feature Bypass) 취약점이 발견되어 실제 공격에 악용되고 있어 긴급 패치가 배포되었습니다.

이와 관련하여 취약점 관련 내용을 공유드리며, M365 Apps를 사용하시는 분은 아래 조치사항을 참고하여 조치하시기 바랍니다.

*[취약점 개요]*
• *Severity*: High (CVSS 7.8) 
• *Description*
• 
    ◦ Microsoft Office가 보안 결정 시 신뢰할 수 없는 입력에 의존하여 발생하는 보안 기능 우회 취약점.  
    ◦ 공격자가 악의적인 OLE(Object Linking and Embedding) 객체가 포함된 Office 문서(Word, Excel, PowerPoint)를 사용자에게 전송하여 파일을 열도록 유도.
    ◦ 파일 실행 시 Office의 OLE 보안 완화 기능을 우회하여 Shell.Explorer.1 COM 객체(내장 Internet Explorer)를 통해 로컬 파일 접근, 스크립트 실행, 원격 서버 연결 가능. 
    ◦ 매크로 경고나 "콘텐츠 사용" 프롬프트 없이 악성 코드가 자동 실행됨.
• *Affected Versions*  
• 
    ◦ Microsoft Office 2016  
    ◦ Microsoft Office 2019  
    ◦ Microsoft Office LTSC 2021  
    ◦ Microsoft Office LTSC 2024  
    ◦ *Microsoft 365 Apps for Enterprise* 
• *Patched Versions*  
    ◦ Office 2021 이상: 서비스 측 업데이트 자동 적용 (Office 애플리케이션 재시작 필요)  
    ◦ Office 2016/2019: 보안 업데이트 설치 필요 (KB5002713)  
    ◦ *Microsoft 365 Apps: 자동 업데이트 후 재시작* 
• *References*  
• 
    ◦ NVD: <https://nvd.nist.gov/vuln/detail/CVE-2026-21509>  
    ◦ Microsoft Security Advisory: <https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-21509>  
    ◦ BleepingComputer Analysis: <https://www.bleepingcomputer.com/news/microsoft/microsoft-patches-actively-exploited-office-zero-day-vulnerability/>  
*[조치사항]*
우리 회사는 M365 Apps를 사용하고 있으므로 대상자 분들은 아래 방법으로 조치 완료해 주시기 바랍니다.
• 현재 열려있는 모든 Office 애플리케이션(Word, Excel, PowerPoint, Outlook 등) 종료
• *Office 애플리케이션을 재시작 하여 패치 적용*


**결정**: ✅ (요약 필요)

#### 16:23 - #C09TX3M1J2W
<!-- ts: 1769671418.177309 -->
> @aiden.kim: <https://docs.google.com/document/d/1Y_GmF6AYOEkj7TEX3CptimlFVDEGZdssRysdzXHIQDs/edit?usp=sharing|[ WSOPTV : Executive Summary ]>
<@U0NPV0M29> <@U22GJU5JT> <@U09HF1166LQ>

#### 13:38 - #C09TX3M1J2W
<!-- ts: 1769661504.256769 -->
> @ggpnotice: <@U080DDS8AQ7> has joined the channel

#### 11:15 - #C09TX3M1J2W
<!-- ts: 1769652959.099329 -->
> @aiden.kim: [ WSOPTV 결제 방식 문의 ]
<@U0NPV0M29> <@U22GJU5JT>


### 2026-02-01

#### 14:30 - #wsoptv-dev
**의사결정**: MVP 범위 확정
> @Michael: MVP에서 Multi-view 빼고 Single-Stream으로 가는 게 맞을 것 같아요. 초기 검증에 집중하고 싶습니다.
> @Tony: 동의합니다. Multi-view는 복잡도가 높아서 Phase 2에서 추가해도 늦지 않아요.
> @Aiden: 확정합니다. PRD 업데이트하고 메가존에 수정 견적 요청하겠습니다.

**결정**: ✅ Single-Stream MVP로 확정 (DEC-2026-0201-001)
**후속**: PRD-0002 v10.1 업데이트, 메가존 견적 요청

#### 11:20 - #wsoptv-biz
**논의**: 메가존 견적 검토
> @Tony: 48억이면 예산 범위 내인데, SLA가 99.9%로 충분한가요? 라이브 스트리밍 특성상 중요할 것 같은데요.
> @Michael: 라이브 스트리밍 특성상 99.95%가 이상적이지만, 업계 표준이 99.9%라 협상 가능할 것 같습니다.
> @Aiden: 계약 시 SLA 강화 조항 추가하도록 검토하겠습니다. penalty 조건도 함께 검토하겠습니다.

**상태**: 🟡 추가 협상 필요
**담당**: @Aiden
**액션**: SLA 강화 조항 검토 (2026-02-08)

#### 09:45 - #wsoptv-tech
**기술 논의**: Player Cam 동기화 방식
> @Aiden: 8개 카메라 스트림을 동기화하려면 어떤 방식이 최선일까요?
> @Michael: HLS는 기본 15-30초 레이턴시라 동기화 어려워요. WebRTC 또는 RTMP 기반 고려해야 합니다.
> @Tony: 메가존에 구체적인 동기화 솔루션 문의 필요하겠네요.

**상태**: ✅ 메가존에 기술 문의 발송 (2026-02-01)
**후속**: 회신 대기 중 (2026-02-08)

---

### 2026-01-31

#### 16:00 - #wsoptv-dev
**릴리스 계획**: 문서 시스템 1.0.0
> @Aiden: PRD-0002 v10.0, Executive Summary v6.4, STRAT-0009 v1.0 완료했습니다.
> @Michael: 고생하셨습니다. 내일 메가존과 미팅에서 활용하겠습니다.

**상태**: ✅ 완료
**산출물**: PRD-0002 v10.0, PRD-0002-executive-summary v6.4, STRAT-0009 v1.0

#### 10:30 - #wsoptv-biz
**업체 평가**: Brightcove vs 메가존
> @Tony: Brightcove에서 견적 요청에 답이 없는데, 메가존으로 진행하는 게 맞을까요?
> @Michael: 메가존이 AWS 기반이라 안정적이고, 경험도 풍부합니다. Brightcove는 2순위 대안으로 두죠.
> @Aiden: 동의합니다. Brightcove에 한 번 더 리마인더 보내고 답이 없으면 제외하겠습니다.

**결정**: 🟢 메가존 최우선, Brightcove 2순위
**액션**: Brightcove 리마인더 발송 (2026-02-03)

---

### 2026-01-30

#### 14:00 - #wsoptv-dev
**문서 업데이트**: PRD-0002 v10.0
> @Aiden: 용어 재정의 완료했습니다. "Player Cam", "Table Multi-view", "StatsView" 통일했어요.
> @Michael: 훨씬 명확해졌네요. Executive Summary도 업데이트 부탁드립니다.

**상태**: ✅ 완료
**산출물**: PRD-0002 v10.0

---

#### 11:34 - #C09TX3M1J2W
<!-- ts: 1769740499.823079 -->
> @aiden.kim: [ GG 생태계에서의 WSOPTV 역할 ]

#### 11:00 - #C09TX3M1J2W
<!-- ts: 1769738410.610069 -->
> @aiden.kim: [ WSOPTV 외부 협력사 리마인더 ]

## 완료된 액션 아이템 (최근 7일)

### ✅ @Aiden - PRD-0002 v10.0 업데이트
- **완료일**: 2026-01-30
- **출처**: #wsoptv-dev
- **내용**: 용어 재정의 및 문서 분리

### ✅ @Aiden - vendor-evaluation-matrix.md 템플릿 작성
- **완료일**: 2026-01-29
- **출처**: #wsoptv-biz
- **내용**: 업체 평가 기준 표준화

### ✅ @Michael - 메가존 미팅 자료 준비
- **완료일**: 2026-01-28
- **출처**: #wsoptv-biz
- **내용**: Executive Summary 기반 발표 자료

---

## 의사결정 이력

### DEC-2026-0201-001: MVP 범위 확정 (Single-Stream)
- **일시**: 2026-02-01 14:30
- **상태**: ✅ 확정
- **영향 범위**: PRD-0002, 스프린트 계획, 예산

---

## 운영 규칙

### 기록 대상
- ✅ 의사결정 (제품/기술/비즈니스)
- ✅ 액션 아이템 (담당자 지정된 작업)
- ✅ 중요 논의 (기술 이슈, 업체 협상)
- ❌ 일반 대화 (인사, 잡담)

### 업데이트 주기
- **즉시**: 의사결정 발생 시 24시간 내 기록
- **일일**: 액션 아이템 상태 업데이트
- **주간**: 매주 금요일 미완료 항목 리뷰
- **월간**: 매월 말일 아카이브 이동

### 의사결정 번호 규칙
- 형식: `DEC-YYYY-MMDD-NNN`
- 예시: `DEC-2026-0201-001`
- 3자리 일련번호, 같은 날 여러 결정 시 증가

### 상태 코드
| 코드 | 설명 | 사용 시점 |
|:----:|------|----------|
| 🔴 | 긴급 | 기한 경과 또는 블로킹 이슈 |
| 🟡 | 주의 | 기한 3일 이내 |
| 🟢 | 정상 | 진행 중 |
| ✅ | 완료 | 작업 종료 |

---

**마지막 동기화**: 2026-02-02 09:00
**담당자**: @Aiden
