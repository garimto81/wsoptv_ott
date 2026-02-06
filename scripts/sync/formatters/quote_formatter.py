"""
QuoteFormatter - Slack Lists 견적 표시 최적화

Usage:
    python quote_formatter.py --test   # 인라인 테스트 실행
    python quote_formatter.py          # 4개 업체 데모 출력
"""
import sys
from decimal import Decimal
from typing import Dict, List, Optional

# QuoteOption import (여러 경로 지원)
try:
    from ..models_v2 import QuoteOption
except (ImportError, ValueError):
    try:
        from models_v2 import QuoteOption
    except ImportError:
        # Standalone 실행용 최소 호환 클래스
        from pydantic import BaseModel

        class QuoteOption(BaseModel):
            option_id: str = ""
            option_name: str = ""
            total_amount: Optional[Decimal] = None
            currency: str = "KRW"
            source_file: Optional[str] = None


class QuoteFormatter:
    """업체별 상황에 맞는 자동 포맷 전략을 적용하는 견적 포맷터."""

    EXCHANGE_RATE = 1375  # 고정 환율: 1 USD = 1,375 KRW

    def format_quote(
        self,
        vendor_name: str,
        options: List[QuoteOption],
        revision_options: Optional[List[QuoteOption]] = None,
        budget_target_usd: Optional[float] = None,
    ) -> str:
        """
        업체 견적을 간결한 문자열로 포맷.

        Returns: 최대 3줄의 포맷된 견적 문자열
        """
        if not options:
            return "N/A"

        # currency는 options[0].currency에서 감지
        currency = options[0].currency if options else "USD"

        # 전략 자동 선택
        strategy = self._select_strategy(options, revision_options)

        if strategy == "negotiation":
            result = self._format_negotiation(options, revision_options, currency)
        elif strategy == "hybrid":
            result = self._format_hybrid(options, revision_options, currency)
        else:
            result = self._format_decision(options, currency)

        return result

    def _select_strategy(self, options, revision_options) -> str:
        """전략 선택 로직."""
        has_revision = revision_options is not None and len(revision_options) > 0
        if has_revision:
            if len(options) >= 3:
                return "hybrid"
            return "negotiation"
        if len(options) >= 3:
            return "hybrid"
        return "decision"

    def _format_decision(self, options: list, currency: str) -> str:
        """Format 1: 의사결정 중심 - 단일 또는 범위 금액."""
        amounts = self._sorted_amounts(options, currency)
        if not amounts:
            return "금액 미감지"

        if len(amounts) == 1:
            formatted = self._format_usd(amounts[0])
            krw_note = self._krw_note_if_needed(options, currency)
            return f"{formatted}{krw_note}"

        min_usd = self._format_usd(amounts[0])
        max_usd = self._format_usd(amounts[-1])
        krw_note = self._krw_note_if_needed(options, currency)
        return f"{min_usd}~{max_usd}{krw_note}"

    def _format_negotiation(self, options, revision_options, currency) -> str:
        """Format 3: 협상 단계 중심 - 1차 + 수정."""
        line1 = self._format_decision(options, currency)

        if revision_options:
            rev_currency = revision_options[0].currency if revision_options else currency
            rev_amounts = self._sorted_amounts(revision_options, rev_currency)
            if rev_amounts:
                if len(rev_amounts) == 1:
                    line2 = f"수정: {self._format_usd(rev_amounts[0])}"
                else:
                    line2 = f"수정: {self._format_usd(rev_amounts[0])}~{self._format_usd(rev_amounts[-1])}"
                return f"{line1}\n{line2}"

        return line1

    def _format_hybrid(self, options, revision_options, currency) -> str:
        """Format 1+3: 범위 + 옵션 수 + 수정 견적."""
        amounts = self._sorted_amounts(options, currency)
        if not amounts:
            return "금액 미감지"

        # 1행: 범위 + 옵션 수
        if len(amounts) == 1:
            line1 = self._format_usd(amounts[0])
        else:
            krw_note = self._krw_note_if_needed(options, currency)
            line1 = f"{self._format_usd(amounts[0])}~{self._format_usd(amounts[-1])} ({len(amounts)}옵션){krw_note}"

        # 2행: 수정 견적 (있으면)
        if revision_options:
            rev_currency = revision_options[0].currency if revision_options else currency
            rev_amounts = self._sorted_amounts(revision_options, rev_currency)
            if rev_amounts:
                if len(rev_amounts) == 1:
                    line2 = f"수정: {self._format_usd(rev_amounts[0])}"
                else:
                    line2 = f"수정: {self._format_usd(rev_amounts[0])}~{self._format_usd(rev_amounts[-1])}"
                return f"{line1}\n{line2}"

        return line1

    def _sorted_amounts(self, options: list, currency: str) -> list:
        """options에서 USD 금액 리스트 추출 및 정렬."""
        amounts = []
        for opt in options:
            if opt.total_amount is not None:
                amt = float(opt.total_amount)
                amounts.append(self._to_usd(amt, currency))
        amounts.sort()
        return amounts

    def _to_usd(self, amount: float, currency: str) -> float:
        """통화 변환 (KRW -> USD)."""
        if currency == "KRW":
            return amount / self.EXCHANGE_RATE
        return amount

    def _format_usd(self, amount: float) -> str:
        """USD 금액 포맷팅."""
        if amount >= 1_000_000:
            return f"${amount / 1_000_000:.2f}M"
        elif amount >= 1_000:
            return f"${amount / 1_000:.1f}K"
        return f"${amount:,.0f}"

    def _format_krw_note(self, amount_krw: float) -> str:
        """KRW 병기용 문자열."""
        if amount_krw >= 100_000_000:  # 1억 이상
            billions = amount_krw / 100_000_000
            if billions == int(billions):
                return f"{int(billions)}억"
            return f"{billions:.2f}억"
        elif amount_krw >= 10_000:
            return f"{amount_krw / 10_000:.0f}만원"
        return f"{amount_krw:,.0f}원"

    def _krw_note_if_needed(self, options: list, currency: str) -> str:
        """KRW 원본이 있으면 괄호 병기."""
        if currency != "KRW":
            return ""
        # KRW 원본 금액 정리
        amounts = []
        for opt in options:
            if opt.total_amount is not None:
                amounts.append(float(opt.total_amount))
        if not amounts:
            return ""
        amounts.sort()

        if len(amounts) == 1:
            return f" ({self._format_krw_note(amounts[0])})"

        return f" ({self._format_krw_note(amounts[0])}~{self._format_krw_note(amounts[-1])})"

    def format_summary(
        self,
        vendor_quotes: Dict[str, str],
        budget_target_usd: Optional[float] = None,
    ) -> str:
        """여러 업체 견적을 한 줄로 요약."""
        parts = []
        for vendor, quote_str in vendor_quotes.items():
            # 첫 줄만 사용
            first_line = quote_str.split("\n")[0]
            # 업체명 축약
            short_name = vendor.replace("클라우드", "").replace("소프트", "").strip()
            parts.append(f"{short_name} {first_line}")

        summary = " | ".join(parts)

        if budget_target_usd is not None:
            budget_str = self._format_usd(budget_target_usd)
            summary += f" (vs 예산 {budget_str})"

        return summary


def format_vendor_quote(
    vendor_name: str,
    options: list,
    revision_options=None,
    budget_target_usd=None,
) -> str:
    """모듈 레벨 편의 함수."""
    return QuoteFormatter().format_quote(
        vendor_name=vendor_name,
        options=options,
        revision_options=revision_options,
        budget_target_usd=budget_target_usd,
    )


def _run_tests() -> bool:
    """인라인 테스트 - 9개 케이스."""
    sys.stdout.reconfigure(encoding="utf-8")

    formatter = QuoteFormatter()
    passed = 0
    failed = 0

    def _assert(test_name, condition, detail=""):
        nonlocal passed, failed
        if condition:
            print(f"  PASS: {test_name}")
            passed += 1
        else:
            print(f"  FAIL: {test_name} - {detail}")
            failed += 1

    print("=== QuoteFormatter Tests ===\n")

    # 1. test_format_vimeo_multiple_options
    print("[Test 1] Vimeo 복수 옵션")
    opts = [
        QuoteOption(option_id="0", option_name="기본", total_amount=Decimal("42500"), currency="USD"),
        QuoteOption(option_id="1", option_name="추천1", total_amount=Decimal("108000"), currency="USD"),
        QuoteOption(option_id="2", option_name="추천2", total_amount=Decimal("282000"), currency="USD"),
        QuoteOption(option_id="3", option_name="추천3", total_amount=Decimal("388000"), currency="USD"),
    ]
    result = formatter.format_quote("Vimeo OTT", opts)
    lines = result.strip().split("\n")
    _assert("3줄 이내", len(lines) <= 3, f"실제: {len(lines)}줄")
    _assert("$42.5K 포함", "$42.5K" in result, f"실제: {result}")
    _assert("$388 포함", "$388" in result, f"실제: {result}")
    _assert("옵션 수 표시", "4옵션" in result or "4개" in result, f"실제: {result}")

    # 2. test_format_vimeo_with_revision
    print("\n[Test 2] Vimeo 수정 견적")
    rev_opts = [
        QuoteOption(option_id="r0", option_name="수정0", total_amount=Decimal("207800"), currency="USD"),
        QuoteOption(option_id="r1", option_name="수정1", total_amount=Decimal("531500"), currency="USD"),
    ]
    result2 = formatter.format_quote("Vimeo OTT", opts, revision_options=rev_opts)
    lines2 = result2.strip().split("\n")
    _assert("3줄 이내", len(lines2) <= 3, f"실제: {len(lines2)}줄")
    _assert("수정 포함", "수정" in result2, f"실제: {result2}")

    # 3. test_format_brightcove_single_usd
    print("\n[Test 3] Brightcove 단일 USD")
    bc_opts = [
        QuoteOption(option_id="bc", option_name="Annual", total_amount=Decimal("1735949"), currency="USD"),
    ]
    result3 = formatter.format_quote("Brightcove", bc_opts)
    _assert("$1.7M 포함", "$1.7" in result3 and "M" in result3, f"실제: {result3}")

    # 4. test_format_megazone_krw_to_usd
    print("\n[Test 4] 메가존 KRW->USD")
    mz_opts = [
        QuoteOption(option_id="mz", option_name="구축비", total_amount=Decimal("4800000000"), currency="KRW"),
        QuoteOption(option_id="mz2", option_name="연운영", total_amount=Decimal("1500000000"), currency="KRW"),
    ]
    result4 = formatter.format_quote("메가존클라우드", mz_opts)
    _assert("$ 접두사", "$" in result4, f"실제: {result4}")
    _assert("억 병기", "억" in result4, f"실제: {result4}")

    # 5. test_format_malgumsoft_krw
    print("\n[Test 5] 맑음소프트 KRW")
    ms_opts = [
        QuoteOption(option_id="ms", option_name="컨설팅+구축", total_amount=Decimal("374000000"), currency="KRW"),
    ]
    result5 = formatter.format_quote("맑음소프트", ms_opts)
    _assert("$ 접두사", "$" in result5, f"실제: {result5}")
    _assert("억 병기", "억" in result5 or "만" in result5, f"실제: {result5}")

    # 6. test_format_usd_ranges
    print("\n[Test 6] USD 금액 포맷팅")
    _assert("$999", formatter._format_usd(999) == "$999", f"실제: {formatter._format_usd(999)}")
    _assert("$42.5K", formatter._format_usd(42500) == "$42.5K", f"실제: {formatter._format_usd(42500)}")
    _assert("$1.74M", formatter._format_usd(1735949) == "$1.74M", f"실제: {formatter._format_usd(1735949)}")

    # 7. test_output_max_3_lines
    print("\n[Test 7] 모든 업체 3줄 이내")
    all_results = [result, result2, result3, result4, result5]
    all_pass = all(len(r.strip().split("\n")) <= 3 for r in all_results)
    _assert("전체 3줄 이내", all_pass, f"초과 결과 있음")

    # 8. test_budget_in_summary_only
    print("\n[Test 8] 예산은 요약에서만")
    no_budget_in_quote = "목표" not in result and "예산" not in result
    _assert("개별 quote에 예산 없음", no_budget_in_quote, f"실제: {result}")

    vendor_quotes = {"Vimeo OTT": result, "Brightcove": result3}
    summary = formatter.format_summary(vendor_quotes, budget_target_usd=10000)
    _assert("요약에 예산 표시", "예산" in summary, f"실제: {summary}")

    # 9. test_decimal_to_float_coercion
    print("\n[Test 9] Decimal -> float 변환")
    dec_opts = [
        QuoteOption(option_id="d", option_name="test", total_amount=Decimal("42500"), currency="USD"),
    ]
    try:
        dec_result = formatter.format_quote("Test", dec_opts)
        _assert("TypeError 없음", True)
    except TypeError as e:
        _assert("TypeError 없음", False, str(e))

    print(f"\n=== Results: {passed}/{passed + failed} passed ===")
    return failed == 0


def _demo():
    """4개 업체 데모 출력."""
    sys.stdout.reconfigure(encoding="utf-8")

    formatter = QuoteFormatter()

    print("=== Quote Formatter Demo ===\n")

    # Vimeo OTT
    vimeo_opts = [
        QuoteOption(option_id="0", option_name="기본", total_amount=Decimal("42500"), currency="USD"),
        QuoteOption(option_id="1", option_name="추천1", total_amount=Decimal("108000"), currency="USD"),
        QuoteOption(option_id="2", option_name="추천2", total_amount=Decimal("282000"), currency="USD"),
        QuoteOption(option_id="3", option_name="추천3", total_amount=Decimal("388000"), currency="USD"),
    ]
    vimeo_rev = [
        QuoteOption(option_id="r0", option_name="수정0", total_amount=Decimal("207800"), currency="USD"),
        QuoteOption(option_id="r1", option_name="수정1", total_amount=Decimal("282000"), currency="USD"),
        QuoteOption(option_id="r2", option_name="수정2", total_amount=Decimal("389500"), currency="USD"),
        QuoteOption(option_id="r3", option_name="수정3", total_amount=Decimal("531500"), currency="USD"),
    ]
    vimeo = formatter.format_quote("Vimeo OTT", vimeo_opts, revision_options=vimeo_rev)
    print(f"[Vimeo OTT]\n{vimeo}\n")

    # Brightcove
    bc_opts = [
        QuoteOption(option_id="bc", option_name="Annual", total_amount=Decimal("1735949"), currency="USD"),
    ]
    bc = formatter.format_quote("Brightcove", bc_opts)
    print(f"[Brightcove]\n{bc}\n")

    # 메가존
    mz_opts = [
        QuoteOption(option_id="mz", option_name="구축비", total_amount=Decimal("4800000000"), currency="KRW"),
        QuoteOption(option_id="mz2", option_name="연운영", total_amount=Decimal("1500000000"), currency="KRW"),
    ]
    mz = formatter.format_quote("메가존클라우드", mz_opts)
    print(f"[메가존클라우드]\n{mz}\n")

    # 맑음소프트
    ms_opts = [
        QuoteOption(option_id="ms", option_name="컨설팅+구축", total_amount=Decimal("374000000"), currency="KRW"),
    ]
    ms = formatter.format_quote("맑음소프트", ms_opts)
    print(f"[맑음소프트]\n{ms}\n")

    # Summary
    vendor_quotes = {
        "Vimeo OTT": vimeo,
        "Brightcove": bc,
        "메가존클라우드": mz,
        "맑음소프트": ms,
    }
    summary = formatter.format_summary(vendor_quotes, budget_target_usd=10000)
    print(f"=== Summary ===\n{summary}")


if __name__ == "__main__":
    if "--test" in sys.argv:
        success = _run_tests()
        sys.exit(0 if success else 1)
    else:
        _demo()
