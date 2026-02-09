# WSOPTV OTT 프로젝트 폴더 정리 계획서

**버전**: 1.0.0
**작성일**: 2026-02-09
**상태**: 계획 수립 완료, 실행 대기

---

## 요약

현재 프로젝트 총 2,209개 파일 중 약 550개가 불필요한 파일로 식별되었다. 가장 큰 문제는 프로젝트 전체 복제본인 `claudewsoptv_ott-vimeo-comparison/` 디렉토리(467파일)이며, 이 외에도 빈 디렉토리, 임시 스크린샷, untracked 파일 정리가 필요하다.

**예상 효과**: 약 550개 파일 제거, 프로젝트 크기 25% 감소

---

## 정리 우선순위

| 순위 | 항목 | 파일 수 | 위험도 | 난이도 |
|:----:|------|:-------:|:------:|:------:|
| 1 | 프로젝트 복제본 제거 | 467 | Critical | 낮음 |
| 2 | 임시 스크린샷 정리 | 16 | High | 낮음 |
| 3 | 빈 디렉토리 제거 | 5 | Medium | 낮음 |
| 4 | Untracked 파일 Git 반영 | 12 | High | 낮음 |
| 5 | 캐시/임시 디렉토리 정리 | ~93 | Low | 낮음 |
| 6 | .gitignore 업데이트 | - | Medium | 낮음 |
| 7 | docs/ 구조 최적화 | - | Low | 중간 |

---

## 실행 전 필수 확인사항

### 백업

```powershell
# 1. Git stash로 현재 변경사항 보호
cd C:\claude\wsoptv_ott
git stash

# 2. 중요 데이터 백업 (복제본 디렉토리에 고유 파일이 있는지 확인)
# diff 결과가 비어있으면 복제본에 고유 파일 없음 = 안전하게 삭제 가능
git diff --no-index --stat docs/ claudewsoptv_ott-vimeo-comparison/docs/ 2>$null

# 3. 임시 스크린샷 중 필요한 것이 있는지 사용자 확인
# docs/images/aiden_temporary/ 의 16개 파일 목록 확인
Get-ChildItem C:\claude\wsoptv_ott\docs\images\aiden_temporary\ | Select-Object Name, LastWriteTime
```

### 확인 체크리스트

- [ ] `claudewsoptv_ott-vimeo-comparison/`에 고유 파일이 없는지 diff 확인
- [ ] `docs/images/aiden_temporary/` 스크린샷 중 보존할 파일 식별
- [ ] Git stash 또는 commit으로 현재 작업 보호
- [ ] 현재 작업 중인 다른 Claude 세션 없음 확인

---

## 단계별 실행 계획

### 1단계: 프로젝트 복제본 제거 (Critical)

**현상**: `claudewsoptv_ott-vimeo-comparison/` 디렉토리에 프로젝트 전체 복제본이 467개 파일로 존재한다. `.claude/` 228파일, `docs/` 201파일, `scripts/` 26파일이 포함되어 있으며, `.git` 파일이 있어 git worktree 또는 submodule 흔적이 남아 있다.

**문제점**:
- Global-Only Policy 위반 (`.claude/` 디렉토리 복제)
- 프로젝트 크기 21% 불필요 증가
- Untracked 상태로 Git에 추가되지 않았지만, 실수로 `git add .` 시 전체 복제본이 커밋될 위험
- 용도인 Vimeo 비교 분석 결과는 이미 `docs/` 내 `vendor-comparison/` 파일들로 존재

**권장 조치**: 전체 삭제

```powershell
# 삭제 전 고유 파일 확인
Get-ChildItem -Path C:\claude\wsoptv_ott\claudewsoptv_ott-vimeo-comparison\ -Recurse -File |
  Where-Object { $_.FullName -notmatch '\\\.claude\\|\\\.git\\' } |
  Select-Object FullName, Length, LastWriteTime

# 고유 파일 없음 확인 후 삭제
Remove-Item -Path C:\claude\wsoptv_ott\claudewsoptv_ott-vimeo-comparison -Recurse -Force

# 삭제 확인
Test-Path C:\claude\wsoptv_ott\claudewsoptv_ott-vimeo-comparison
# 결과: False
```

**예상 효과**: 467개 파일 제거

---

### 2단계: 임시 스크린샷 정리 (High)

**현상**: `docs/images/aiden_temporary/`에 2026-02-02 날짜의 스크린샷 16개가 "스크린샷 2026-02-02 HHMMSS.png" 형식으로 저장되어 있다.

**문제점**:
- 파일명에 한글과 공백 포함 (자동화 스크립트 호환성 저하)
- 임시 폴더명(`aiden_temporary`)이 프로젝트 구조에 부적합
- 용도가 불명확하여 어떤 PRD/문서와 관련되는지 추적 불가

**권장 조치**: 필요한 파일은 해당 PRD 이미지 폴더로 이동, 불필요한 파일은 삭제

```powershell
# 파일 목록 확인 (사용자가 보존 여부 판단)
Get-ChildItem C:\claude\wsoptv_ott\docs\images\aiden_temporary\ |
  Format-Table Name, Length, LastWriteTime -AutoSize

# 방안 A: 전체 삭제 (불필요 확인 후)
Remove-Item -Path C:\claude\wsoptv_ott\docs\images\aiden_temporary -Recurse -Force

# 방안 B: 특정 PRD 폴더로 이동 (필요한 파일이 있는 경우)
# Move-Item "C:\claude\wsoptv_ott\docs\images\aiden_temporary\스크린샷*.png" `
#   C:\claude\wsoptv_ott\docs\images\PRD-XXXX\
# Remove-Item C:\claude\wsoptv_ott\docs\images\aiden_temporary -Force
```

**예상 효과**: 16개 파일 제거 또는 재배치, 임시 디렉토리 1개 제거

---

### 3단계: 빈 디렉토리 제거 (Medium)

**현상**: 5개의 빈 디렉토리가 존재한다.

| 디렉토리 | 원인 추정 |
|----------|----------|
| `.claude/skills/_archive` | 스킬 정리 후 빈 archive |
| `.claude/skills/ultimate-debate/scripts/.claude/debates/test_debate_001` | 테스트 잔여물 |
| `docs/images/ADR-0001` | ADR 문서 미작성 |
| `docs/mockups/ADR-0001` | ADR 목업 미작성 |
| `docs/mockups/STRAT-0003` | 전략 문서 목업 미작성 |

**권장 조치**: 전체 삭제 (Git은 빈 디렉토리를 추적하지 않으므로 커밋에 영향 없음)

```powershell
# 빈 디렉토리 삭제
$emptyDirs = @(
  "C:\claude\wsoptv_ott\.claude\skills\_archive",
  "C:\claude\wsoptv_ott\.claude\skills\ultimate-debate\scripts\.claude\debates\test_debate_001",
  "C:\claude\wsoptv_ott\docs\images\ADR-0001",
  "C:\claude\wsoptv_ott\docs\mockups\ADR-0001",
  "C:\claude\wsoptv_ott\docs\mockups\STRAT-0003"
)

foreach ($dir in $emptyDirs) {
  if (Test-Path $dir) {
    Remove-Item $dir -Recurse -Force
    Write-Host "Removed: $dir"
  }
}
```

**예상 효과**: 빈 디렉토리 5개 제거, 구조 정돈

---

### 4단계: Untracked 파일 Git 반영 (High)

**현상**: 유의미한 파일 12개가 untracked 상태로 Git에 반영되지 않았다.

**권장 조치**: 파일별 분류 후 git add 또는 .gitignore 추가

| 파일 | 조치 | 이유 |
|------|------|------|
| `claudewsoptv_ott-vimeo-comparison/` | 1단계에서 삭제 | 복제본 |
| `docs/images/vendor-comparison/*.png` | `git add` | 비교 문서 이미지 |
| `docs/images/vendor-comparison/*.pdf` | `git add` | 비교 문서 PDF |
| `docs/mockups/vendor-comparison/*.html` | `git add` | 비교 목업 |
| `.claude/commands/work-wsoptv.md` | `git add` | 프로젝트 커맨드 |
| `.claude/skills/agent-teamworks/SKILL.md` | `git add` | 신규 스킬 (Junction) |
| `docs/management/DRIVE-REGISTRY.md` | `git add` | 관리 문서 |
| `test-results/.last-run.json` | `.gitignore` 추가 | 테스트 결과 캐시 |

```powershell
cd C:\claude\wsoptv_ott

# Git에 추가할 파일
git add docs/images/vendor-comparison/vimeo-vs-brightcove-onepage-v2.pdf
git add docs/images/vendor-comparison/vimeo-vs-brightcove-onepage-v2.png
git add docs/images/vendor-comparison/vimeo-vs-brightcove-onepage-v3.png
git add docs/mockups/vendor-comparison/vimeo-vs-brightcove-onepage.html
git add docs/mockups/vendor-comparison/vimeo-vs-brightcove-onepage-v2.html
git add docs/mockups/vendor-comparison/vimeo-vs-brightcove-onepage-v3.html
git add .claude/commands/work-wsoptv.md
git add .claude/skills/agent-teamworks/
git add docs/management/DRIVE-REGISTRY.md

# test-results/는 .gitignore에 추가 (6단계에서 처리)
```

**예상 효과**: 프로젝트 파일 추적 정상화

---

### 5단계: 캐시/임시 디렉토리 정리 (Low)

**현상**: .gitignore로 제외된 캐시 디렉토리들이 로컬에 존재한다. Git에 영향 없으나 디스크 공간을 차지한다.

| 디렉토리 | 파일 수 | 용도 | 조치 |
|----------|:-------:|------|------|
| `attachments/` | 56 | Gmail 첨부파일 캐시 | 유지 (재다운로드 비용) |
| `.omc/` | 23 | OMC 세션 상태 | 유지 (자동 관리) |
| `stitch/` | 3 | Stitch API 캐시 | 삭제 가능 |
| `.ruff_cache/` | 3 | 린트 캐시 | 삭제 가능 |
| `docs/.pdca-snapshots/` | 10 | PDCA 스냅샷 | 유지 (이력 보존) |
| `test-results/` | 1 | 테스트 결과 | 유지 |

**권장 조치**: `stitch/`과 `.ruff_cache/`만 선택적 삭제 (자동 재생성됨)

```powershell
# 선택적 캐시 정리 (자동 재생성되는 것만)
Remove-Item -Path C:\claude\wsoptv_ott\stitch -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path C:\claude\wsoptv_ott\.ruff_cache -Recurse -Force -ErrorAction SilentlyContinue
```

**예상 효과**: 6개 파일 제거 (디스크 절약, 기능 영향 없음)

---

### 6단계: .gitignore 업데이트 (Medium)

**현상**: 현재 .gitignore에 `test-results/`가 없고, 깨진 파일명 패턴(`C\357\200\272*`)이 남아 있다.

**권장 조치**: 아래 항목 추가/수정

```powershell
# .gitignore에 추가할 내용
```

```gitignore
# Test results
test-results/

# Ruff cache
.ruff_cache/
```

깨진 파일명 패턴(`C\357\200\272*`)은 해당 파일이 실제로 존재하는지 확인 후, 없으면 제거한다.

```powershell
# 깨진 파일명 패턴 확인
Get-ChildItem C:\claude\wsoptv_ott\ -Filter "C*" -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -match '^\xEF\x80\xBA' }
# 결과 없으면 .gitignore에서 해당 라인 제거
```

---

### 7단계: docs/ 구조 최적화 (Low)

**현상**: docs/ 내 221개 파일이 산재해 있으며, 구조 개선 여지가 있다.

**현재 구조**:
```
docs/
  archive/          (19) - deprecated 문서
  images/           (102) - 스크린샷, 이미지
    PRD-0002/       (64) - MVP 스펙 이미지
    PRD-0012/       (12)
    aiden_temporary/ (16) - 2단계에서 정리
    brightcove-proposal/ (6)
    vendor-comparison/ (4)
    ADR-0001/       (0) - 3단계에서 제거
  management/       (10) - 프로젝트 관리
  mockups/          (63) - HTML 목업
    PRD-0002/       (47)
    PRD-0012/       (12)
    vendor-comparison/ (4)
    ADR-0001/       (0) - 3단계에서 제거
    STRAT-0003/     (0) - 3단계에서 제거
  phase0/           (5) - Vision, Business, RFP
  phase1/           (2) - MVP Spec, Content
  poc/              (4) - Vimeo POC 문서
  reports/          (3) - 보고서
  templates/        (1) - 템플릿
  .pdca-snapshots/  (10) - .gitignore됨
```

**권장 조치**: 현 구조는 PRD 번호 기반으로 잘 정리되어 있으므로 대규모 재구성은 불필요하다. 1~6단계 정리 후 아래만 검토한다.

- `docs/reports/`와 `docs/poc/`의 파일이 적으므로 `docs/phase1/` 하위로 통합 검토
- `docs/templates/`에 파일 1개만 있으면 활용도 재검토

이 단계는 긴급하지 않으며, 다른 단계 완료 후 필요 시 진행한다.

---

## 디렉토리 구조 비교

### Before (현재)

```
C:\claude\wsoptv_ott\              총 2,209개 파일
├── .git/                          (1,187) Git 내부
├── claudewsoptv_ott-vimeo-comparison/  (467) 복제본
├── docs/                          (221)
│   ├── images/aiden_temporary/    (16) 임시 스크린샷
│   ├── images/ADR-0001/           (0) 빈 디렉토리
│   ├── mockups/ADR-0001/          (0) 빈 디렉토리
│   └── mockups/STRAT-0003/        (0) 빈 디렉토리
├── .claude/                       (201) Junction
│   └── skills/_archive/           (0) 빈 디렉토리
├── scripts/                       (47)
├── attachments/                   (56) 캐시
├── .omc/                          (23) 상태
├── stitch/                        (3) 캐시
├── .ruff_cache/                   (3) 캐시
├── test-results/                  (1)
└── Root files                     (5)
```

### After (정리 후)

```
C:\claude\wsoptv_ott\              총 ~1,720개 파일 (약 490개 감소)
├── .git/                          (1,187) 변경 없음
├── docs/                          (~195) 정리됨
│   ├── archive/                   (19)
│   ├── images/                    (~86) 임시 제거, 빈폴더 제거
│   ├── management/                (11) FOLDER-CLEANUP-PLAN.md 추가
│   ├── mockups/                   (~63) 빈폴더 제거
│   ├── phase0/                    (5)
│   ├── phase1/                    (2)
│   ├── poc/                       (4)
│   ├── reports/                   (3)
│   └── templates/                 (1)
├── .claude/                       (~200) Junction, 빈폴더 제거
├── scripts/                       (47) 변경 없음
├── attachments/                   (56) 유지 (.gitignore)
├── .omc/                          (23) 유지 (.gitignore)
└── Root files                     (5) 변경 없음
```

---

## 예상 효과

| 항목 | 제거 파일 수 | 비율 |
|------|:-----------:|:----:|
| 복제본 디렉토리 | 467 | 85% |
| 임시 스크린샷 | 16 | 3% |
| 빈 디렉토리 | 5 | 1% |
| 캐시 파일 | 6 | 1% |
| **합계** | **~494** | **프로젝트 총 파일의 22% 감소** |

추가 효과:
- Untracked 파일 12개 정상 반영 (git add 또는 gitignore)
- .gitignore 정비로 향후 캐시 파일 자동 제외
- 디렉토리 구조 일관성 확보

---

## 실행 일정 권장

| 단계 | 소요 시간 | 의존성 |
|:----:|:---------:|:------:|
| 1단계 (복제본 제거) | 5분 | 없음 |
| 2단계 (임시 스크린샷) | 5분 | 사용자 확인 필요 |
| 3단계 (빈 디렉토리) | 2분 | 없음 |
| 4단계 (Git 반영) | 5분 | 1~3단계 완료 |
| 5단계 (캐시 정리) | 2분 | 없음 |
| 6단계 (.gitignore) | 3분 | 없음 |
| 7단계 (구조 최적화) | 추후 결정 | 1~6단계 완료 |
| **총 소요** | **~25분** | |

1~6단계는 한 번에 실행 가능하며, 커밋 1개로 묶어 반영한다.

```powershell
# 전체 정리 후 커밋
cd C:\claude\wsoptv_ott
git add -A
git commit -m "chore: 프로젝트 폴더 정리 - 복제본 제거, 빈 디렉토리 삭제, .gitignore 정비"
```

---

## 변경 이력

| 날짜 | 버전 | 내용 |
|------|------|------|
| 2026-02-09 | 1.0.0 | 최초 작성 |
