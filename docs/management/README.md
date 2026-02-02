# WSOPTV 프로젝트 관리 시스템

**버전**: 1.0.0
**최종 업데이트**: 2026-02-02

## 빠른 링크

| 시스템 | 파일 | 용도 |
|--------|------|------|
| 📧 메일 관리 | [EMAIL-LOG.md](./EMAIL-LOG.md) | 업체별 이메일 추적 |
| 💬 슬랙 관리 | [SLACK-LOG.md](./SLACK-LOG.md) | 의사결정/액션 아이템 |
| 🏢 업체 관리 | [VENDOR-DASHBOARD.md](./VENDOR-DASHBOARD.md) | RFP 진행 상태 |
| 📄 기획 관리 | [DOCUMENT-TRACKER.md](./DOCUMENT-TRACKER.md) | 문서 버전 관리 |

## 오늘의 요약 (2026-02-02)

### 🔴 긴급 (Action Required)
- Brightcove 견적서 미회신 (D+5) → 리마인더 발송 필요

### 🟡 주의
- PRD-0002 v10.1 업데이트 필요 (MVP 범위 변경)
- 메가존 기술 문의 회신 대기 중

### ✅ 완료
- 메가존 수정 견적 수령 (48억)
- vendor-evaluation-matrix.md 템플릿 완성

## 자동 동기화

Gmail과 Slack 메시지를 자동으로 로그 파일에 동기화합니다.

### 명령어

```powershell
# 전체 동기화
python scripts/sync_management.py sync

# Slack만 (최근 7일)
python scripts/sync_management.py sync --slack --days 7

# Gmail만 (wsoptv 라벨)
python scripts/sync_management.py sync --gmail

# Dry-run (미리보기)
python scripts/sync_management.py sync --dry-run

# 상태 확인
python scripts/sync_management.py status
```

### 연동 설정

| 항목 | 값 | 용도 |
|------|-----|------|
| Gmail 라벨 | `wsoptv` | 업체 이메일 필터링 |
| Slack 채널 | `C09TX3M1J2W` | WSOPTV 프로젝트 채널 |

### 자동 감지 기능

- **의사결정**: "확정", "결정", "동의", "승인" 등 패턴 감지
- **액션 아이템**: "@멘션 + 해주세요/부탁/처리" 패턴 감지
- **중복 방지**: ts(timestamp) / email_id 기반

---

## 관리 원칙

1. **즉시 기록**: 이벤트 발생 시 24시간 내 기록
2. **단일 소스**: 각 정보는 한 곳에서만 관리
3. **상호 참조**: 시스템 간 링크로 연결
4. **정기 리뷰**: 주간(금), 월간(말일) 정리
5. **자동 동기화**: `python scripts/sync_management.py sync` 정기 실행
