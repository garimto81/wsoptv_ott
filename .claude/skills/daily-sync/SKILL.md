---
name: daily-sync
description: >
  WSOPTV 프로젝트 일일 동기화 스킬. Gmail/Slack 데이터를 Claude Code가 직접 분석하여
  업체 상태, 견적, 회신 필요 여부를 추론하고 Slack Lists를 업데이트합니다.
  별도 API 호출 없이 Claude Code 세션 내에서 분석합니다.
version: 1.1.0

triggers:
  keywords:
    - "daily-sync"
    - "일일 동기화"
    - "업체 현황"
    - "vendor status"
    - "협상 현황"
    - "견적 분석"
    - "wsoptv sync"
    - "회신 필요"
    - "pending replies"
    - "업체 분석"
  patterns:
    - "/daily-sync"
    - "daily-sync (run|status|analyze)"
    - "업체.*(현황|분석|상태)"
    - "(견적|quote).*(분석|추출|확인)"
  file_patterns:
    - "**/wsoptv_ott/**"
    - "**/docs/management/**"
  context:
    - "WSOPTV OTT 프로젝트"
    - "업체 관리"
    - "RFP 진행"

capabilities:
  - gmail_analysis
  - slack_analysis
  - quote_extraction_hybrid
  - status_inference_ai
  - slack_lists_update
  - attachment_analysis

model_preference: sonnet
auto_trigger: true
---

# Daily Sync Skill - WSOPTV 일일 동기화

WSOPTV 프로젝트의 업체 관리를 위한 AI 분석 기반 일일 동기화 스킬입니다.
Gmail/Slack 데이터를 Claude Code가 직접 분석하여 업체 현황을 파악합니다.

## 핵심 기능

| 기능 | 방식 | 설명 |
|------|------|------|
| **이메일 분석** | AI | 업체 메일에서 견적, 협상 상태, 긴급도 추론 |
| **Slack 분석** | AI | 팀 논의에서 의사결정, 액션 아이템 추출 |
| **견적 추출** | 하이브리드 | 정규식 → AI 폴백으로 비정형 금액 처리 |
| **첨부파일 분석** | 하이브리드 | Claude Read(≤20p) + pdfplumber(>20p) |
| **상태 추론** | AI | 이메일 톤 기반 협상 단계 판단 |
| **보고서 생성** | AI | 상황에 맞는 자연어 보고서 |

---

## 사용 방법

### 1. 기본 실행

```
/daily-sync
```

또는 자연어로:

```
업체 현황 분석해줘
견적 분석해줘
회신 필요한 메일 알려줘
```

### 2. 옵션

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--vendor <name>` | 특정 업체만 분석 | `/daily-sync --vendor megazone` |
| `--days <n>` | 분석 기간 (기본 30일) | `/daily-sync --days 14` |
| `--quick` | 빠른 요약만 | `/daily-sync --quick` |

---

## 워크플로우

### Phase 1: Data Collection

Claude가 다음 명령을 실행하여 데이터를 수집합니다:

**Step 1: 라벨 기반 수집 (기존)**
```powershell
# Gmail 수집 (wsoptv 라벨)
cd C:\claude && python -m lib.gmail search "label:wsoptv" --limit 50
```

**Step 2: 도메인 기반 보완 수집 (NEW - 라벨 누락 방지)**
```powershell
# 업체 도메인으로 직접 검색 (라벨 없는 메일 포착)
cd C:\claude && python -m lib.gmail search "from:vimeo.com OR from:brightcove.com OR from:megazone.com OR from:jrmax.co.kr OR from:amazon.com newer_than:7d" --limit 50
```

**Step 3: 키워드 기반 보완 수집 (NEW - 새 스레드 포착)**
```powershell
# 견적/제안 관련 키워드 검색
cd C:\claude && python -m lib.gmail search "견적 OR quote OR pricing OR proposal newer_than:7d" --limit 20
```

**Step 4: Slack 메시지 수집**
```powershell
cd C:\claude && python -m lib.slack history C09TX3M1J2W --limit 100
```

수집 데이터:
- Gmail: wsoptv 라벨 이메일 (Step 1)
- Gmail: 업체 도메인 직접 검색 (Step 2) - **라벨 누락 방지**
- Gmail: 견적/제안 키워드 검색 (Step 3) - **새 스레드 포착**
- Slack: #wsoptv 채널의 최근 7일 메시지

**⚠️ 중요**: Step 1만으로는 업체가 새 스레드로 보낸 이메일을 놓칠 수 있음.
반드시 Step 2, 3을 병행하여 라벨이 없는 이메일도 포착해야 함.

### Phase 1.5: Attachment Download & Parse

Gmail 이메일에 첨부된 견적 관련 파일을 분석합니다.

#### Step 0: 인증 확인 (권장)

```powershell
# Gmail 인증 상태 확인
cd C:\claude && python -m lib.gmail status
```

#### Step 1: 견적 첨부파일 식별

이메일 목록에서 첨부파일 메타데이터 확인:
- PDF 파일 (mime_type: application/pdf)
- Excel 파일 (.xlsx, .xls)
- 파일명에 "견적", "quote", "proposal" 포함

#### Step 2: 첨부파일 다운로드

```powershell
# AttachmentDownloader 활용 (캐시 자동 적용)
cd C:\claude\wsoptv_ott && python -c "
from scripts.sync.collectors.attachment_downloader import AttachmentDownloader
from pathlib import Path
import json

downloader = AttachmentDownloader(cache_dir=Path('./attachments'))
attachments = downloader.get_quote_attachments('EMAIL_ID')
print(json.dumps([a.model_dump() for a in attachments], default=str))
"
```

#### Step 3: PDF 분석

**Case A: 20페이지 이하 PDF**
- Claude Read tool로 직접 읽기 (레이아웃 보존)
- Claude가 시각적으로 금액, 테이블 분석

**Case B: 20페이지 초과 PDF**
```powershell
cd C:\claude\wsoptv_ott && python -c "
from scripts.sync.parsers.pdf_parser import get_pdf_parser
from pathlib import Path
import json

parser = get_pdf_parser()
result = parser.extract_all(Path('PATH_TO_PDF'))
print(json.dumps({
    'page_count': result['page_count'],
    'text': result['text'][:5000],  # 토큰 절약
    'table_count': len(result['tables']),
}, ensure_ascii=False))
"
```

#### Step 4: Excel 분석

```powershell
cd C:\claude\wsoptv_ott && python -c "
from scripts.sync.parsers.excel_parser import get_excel_parser
from scripts.sync.extractors.quote_extractor import get_quote_extractor
from pathlib import Path
import json

parser = get_excel_parser()
sheets = parser.parse(Path('PATH_TO_EXCEL'))
extractor = get_quote_extractor()
quotes = extractor.extract_from_excel(sheets)
print(json.dumps([q.model_dump() for q in quotes], default=str))
"
```

#### Step 5: 결과 통합

- 본문에서 추출한 견적 + 첨부파일에서 추출한 견적 병합
- 중복 제거 (동일 금액)
- 신뢰도 높은 것 우선 (첨부파일 > 본문)

### Phase 2: AI Analysis

Claude Code가 수집된 JSON 데이터를 직접 분석합니다.

#### 2.1 이메일 분석

각 업체별 이메일 스레드에서:

1. **견적 정보 추출**
   - 정규식으로 1차 시도 (48억원, 6,600만원 등)
   - 실패 시 AI가 비정형 금액 추론 (약 50억 내외, 40~50억 사이 등)
   - **첨부파일 분석 결과 통합** (Phase 1.5에서 추출한 견적 포함)

2. **협상 상태 추론**
   - 이메일 내용과 톤 분석
   - 현재 단계 판단: initial_contact → rfp_sent → quote_waiting → quote_received → reviewing → negotiating → contract_review
   - 업체 관심도 평가 (HIGH/MEDIUM/LOW)

3. **회신 긴급도 판단**
   - 날짜 기반: 마지막 업체 메일로부터 경과 일수
   - 내용 기반: "ASAP", "빠른 답변", "마감일" 등 키워드
   - 종합 긴급도: CRITICAL (7일+), HIGH (3-7일), MEDIUM (1-3일), LOW (<1일)

#### 2.2 Slack 메시지 분석

팀 논의에서:
- 의사결정 사항 추출
- 액션 아이템 식별
- 업체 관련 언급 요약

### Phase 3: Output Generation

분석 결과를 자연어 보고서로 생성:

```
📊 **WSOPTV 일일 동기화 보고서** (2026-02-04)

### 🚨 즉시 조치 필요

**1. Brightcove** - RE: WSOPTV RFP Follow-up
- 긴급도: CRITICAL (12일 무응답)
- 업체 관심도: HIGH (상세 질문 제기)
- 권장 액션: 금일 중 회신 필요

### 💰 견적 현황

| 업체 | 금액 | 상태 |
|------|------|------|
| MegazoneCloud | 48억 + 15억/년 | 검토 중 |
| Brightcove | 미수령 | 견적 대기 |

### 📈 협상 진행 상황

**MegazoneCloud** - 최우선 검토 중
- 현재: reviewing → negotiating 예상
- 관심도: HIGH
- 평가: 기술적 적합성 높음, 가격 협상 여지

### 🔄 Slack Lists 업데이트 제안

다음 변경사항을 반영할까요?
1. MegazoneCloud: 견적 → "48억 + 15억/년"
2. Brightcove: 상태 → quote_waiting

[업데이트 적용] [건너뛰기]
```

---

## AI 분석 프롬프트

스킬 실행 시 Claude는 다음 프롬프트를 참조합니다:

### 이메일 분석 프롬프트

`.claude/skills/daily-sync/prompts/email_analysis.md` 참조

분석 항목:
- quotes: 금액, 통화, 옵션, 조건
- negotiation_status: 현재 단계, 신뢰도, 근거
- urgency: 긴급도, 요인, 권장 액션
- vendor_interest: 관심도, 지표, 응답 품질

### 상태 추론 프롬프트

`.claude/skills/daily-sync/prompts/status_inference.md` 참조

협상 단계:
- initial_contact: 초기 접촉 (인사, 소개)
- rfp_sent: RFP 발송됨 (요구사항 전달)
- quote_waiting: 견적 대기 (응답 대기)
- quote_received: 견적 수령 (금액 확인)
- reviewing: 검토 중 (내부 검토)
- negotiating: 협상 중 (가격/조건 조율)
- contract_review: 계약 검토 (법무 검토)
- on_hold: 보류 (일시 중단)
- excluded: 제외 (탈락)

---

## 견적 추출 하이브리드 전략

### Step 1: 정규식 추출 (기존 로직)

```python
# 처리 가능한 패턴
"48억원" → 4,800,000,000원
"6,600만원" → 66,000,000원
"50억" → 5,000,000,000원
```

### Step 2: AI 추론 (정규식 실패 시)

```
# AI가 처리하는 패턴
"40~50억 사이" → 범위: 40억~50억
"기본 30억, 풀옵션 시 50억" → 옵션A: 30억, 옵션B: 50억
"대략 50억 내외" → 약 50억 (±10%)
"초기 20억 + 연간 유지비 3억" → 초기: 20억, 연간: 3억
```

---

## 업체 매핑

wsoptv_sync_config.yaml에 정의된 업체:

| 업체 | 주 도메인 | 관련 도메인 | Slack Lists Row |
|------|----------|------------|-----------------|
| MegazoneCloud | @megazone.com | @mz.co.kr | row_001 |
| Brightcove | @brightcove.com | - | row_002 |
| Vimeo OTT | @vimeo.com | @jrmax.co.kr (한국 대리점) | row_003 |
| MalgumSoft | @malgum.com | - | row_004 |
| AWS (파트너 연결) | @amazon.com | - | - (직접 관리 아님) |

**⚠️ 주의**: 업체가 새 스레드로 이메일을 보내면 `wsoptv` 라벨이 없을 수 있음.
반드시 Phase 1의 3단계 검색(라벨 → 도메인 → 키워드)을 모두 수행해야 함.

---

## Slack Lists 업데이트

분석 후 Slack Lists 업데이트를 제안합니다.
사용자 확인 후 기존 `scripts/sync/lists_sync.py`를 통해 업데이트합니다.

```powershell
# 사용자 확인 후 실행
cd C:\claude\wsoptv_ott && python scripts/sync/lists_sync.py update --vendor "MegazoneCloud" --field "견적" --value "48억 + 15억/년"
```

---

## 토큰 효율성

### 증분 분석

- 이전 분석 결과를 `.sync_state.json`에 캐시
- 새로운 이메일/메시지만 분석
- 2회차부터 약 70% 토큰 절감

### 배치 그룹핑

- 업체별로 이메일을 그룹화
- 한 번의 분석으로 업체당 모든 정보 추출

---

## 관련 파일

| 파일 | 용도 |
|------|------|
| `wsoptv_sync_config.yaml` | 업체 매핑, 설정 |
| `docs/management/.sync_state.json` | 동기화 상태 |
| `scripts/sync/lists_sync.py` | Slack Lists 업데이트 |
| `lib/gmail/` | Gmail API 래퍼 |
| `lib/slack/` | Slack API 래퍼 |

---

## 트러블슈팅

### Gmail 인증 오류

```powershell
cd C:\claude && python -m lib.gmail login
```

### Slack 토큰 만료

```powershell
cd C:\claude && python -m lib.slack login
```

### 분석 결과가 부정확한 경우

1. `--days 7`로 짧은 기간 테스트
2. 특정 업체만 `--vendor <name>`으로 분석
3. 원본 이메일 확인 후 피드백

---

## 변경 로그

### v1.1.0 (2026-02-04)

- Phase 1.5 첨부파일 분석 추가
- PDF 분석: Claude Read (≤20p) + pdfplumber (>20p) 하이브리드
- Excel 분석: QuoteExtractor 통합
- 견적 추출 신뢰도 향상: 첨부파일 > 본문 우선

### v1.0.0 (2026-02-04)

- 초기 릴리스
- Gmail/Slack 데이터 수집
- AI 기반 견적 추출 (하이브리드)
- AI 기반 협상 상태 추론
- AI 기반 긴급도 판단
- 자연어 보고서 생성
- Slack Lists 업데이트 제안
