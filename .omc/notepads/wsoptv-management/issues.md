# WSOPTV 프로젝트 관리 시스템 - Issues

**Created**: 2026-02-02
**Last Updated**: 2026-02-02

---

## 알려진 이슈

### ISSUE-001: Windows cp949 인코딩 에러
**상태**: Workaround
**증상**: 콘솔 출력 시 특수문자(•, ✅ 등)에서 `'cp949' codec can't encode character` 에러
**원인**: Windows 기본 콘솔이 cp949 인코딩 사용
**시도한 해결책**:
- sys.stdout를 UTF-8 TextIOWrapper로 래핑 → Rich Console과 충돌
- 롤백 완료
**현재 상태**: 파일 쓰기는 UTF-8로 정상 작동, 콘솔 표시만 깨짐 (수용 가능)
**권장 해결책**: Windows Terminal 또는 VS Code 터미널 사용 (UTF-8 지원)

### ISSUE-002: Gmail 동기화 미완성
**상태**: Open
**증상**: `--gmail` 옵션 실행 시 "Gmail 동기화는 아직 구현되지 않았습니다" 메시지
**원인**: gmail_sync.py가 placeholder 상태
**다음 단계**: EmailLogEntry 모델 기반으로 EMAIL-LOG.md 쓰기 구현

---

## 해결된 이슈

### RESOLVED-001: lib.slack import 실패
**해결일**: 2026-02-02
**증상**: `ModuleNotFoundError: No module named 'lib.slack'`
**해결책**: sys.path에 `C:\claude` 추가
```python
_claude_root = _script_dir.parents[2]
sys.path.insert(0, str(_claude_root))
```

### RESOLVED-002: Slack 인증 테스트
**해결일**: 2026-02-02
**증상**: Slack API 연결 확인 필요
**해결책**: `SlackClient().auth_test()` 호출로 인증 상태 확인
**결과**: GGProduction 워크스페이스, bot user U080DDS8AQ7 정상
