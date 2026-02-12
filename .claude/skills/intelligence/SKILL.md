---
name: intelligence
description: Project Intelligence - 자동/수동 응답 초안 생성 및 관리
triggers:
  keywords:
    - intelligence
    - pending
    - drafts
    - 미매칭
    - 초안
    - undrafted
  commands:
    - /intelligence
---

# Project Intelligence 스킬

프로젝트별 컨텍스트를 수집하고, 수신 메시지에 대한 응답 초안을 생성/관리합니다.

## 아키텍처

```
Gateway 수신 → ContextMatcher 매칭 → Ollama 자동 draft → DraftStore (파일+DB+Toast)
                                      │ (Ollama 불가 시)
                                      └→ DB 저장 (awaiting_draft) → 이 스킬로 수동 처리
```

- **자동 모드**: Gateway가 메시지 수신 시 Ollama 로컬 LLM이 즉시 draft 생성
- **수동 모드**: Ollama가 꺼져있으면 `awaiting_draft` 상태로 저장 → 이 스킬로 처리

## 실행 방법

### 1. Draft 생성 (수동 모드 - Ollama 불가 시)

Gateway가 매칭한 메시지 중 draft가 아직 없는 항목을 조회하고 응답 초안을 생성합니다.

```bash
# undrafted 메시지 조회
cd C:\claude\secretary && python scripts/intelligence/cli.py undrafted --json
```

각 메시지에 대해:
1. 프로젝트 컨텍스트와 원본 메시지를 읽음
2. 한국어로 적절한 응답 초안 작성
3. CLI로 저장:

```bash
cd C:\claude\secretary && python scripts/intelligence/cli.py save-draft <id> --text "생성한 응답"
```

### 2. Pending 메시지 확인 및 분류

```bash
cd C:\claude\secretary && python scripts/intelligence/cli.py pending --json
```

결과를 확인하고, 각 pending 메시지를 적절한 프로젝트에 매칭:

```bash
cd C:\claude\secretary && python scripts/intelligence/cli.py review <message_id> <project_id>
```

### 3. 응답 초안 관리

```bash
# 초안 목록 확인
cd C:\claude\secretary && python scripts/intelligence/cli.py drafts --status pending

# 초안 승인
cd C:\claude\secretary && python scripts/intelligence/cli.py drafts approve <id>

# 초안 거부
cd C:\claude\secretary && python scripts/intelligence/cli.py drafts reject <id>
```

### 4. 증분 분석 실행

```bash
# 전체 프로젝트 분석
cd C:\claude\secretary && python scripts/intelligence/cli.py analyze

# 특정 프로젝트만
cd C:\claude\secretary && python scripts/intelligence/cli.py analyze --project secretary

# 특정 소스만
cd C:\claude\secretary && python scripts/intelligence/cli.py analyze --source slack
```

### 5. 통계 조회

```bash
cd C:\claude\secretary && python scripts/intelligence/cli.py stats
```

## 설정

- 프로젝트 정의: `C:\claude\secretary\config\projects.json`
- Gateway 설정: `C:\claude\secretary\config\gateway.json` (intelligence.ollama 섹션)
- DB: `C:\claude\secretary\data\intelligence.db`
- Draft 파일: `C:\claude\secretary\data\drafts/`

### Ollama 설정 (gateway.json)

```json
{
  "intelligence": {
    "enabled": true,
    "ollama": {
      "enabled": true,
      "endpoint": "http://localhost:11434",
      "model": "qwen2.5",
      "timeout": 90,
      "max_context_chars": 12000,
      "rate_limit_per_minute": 10
    }
  }
}
```
