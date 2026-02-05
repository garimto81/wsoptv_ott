"""Quote extractor for parsing pricing information from documents."""

import re
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import List, Optional, Union

import sys
sys.path.insert(0, str(Path(__file__).parents[1]))
from models_v2 import QuoteOption

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


class QuoteExtractor:
    """Extract quote/pricing information from text and tables."""

    # Korean amount patterns
    AMOUNT_PATTERNS = [
        # 48억원, 3.74억원
        (r'(\d+(?:\.\d+)?)\s*억\s*(?:원)?', 100_000_000),
        # 6,600만원, 3,000만원
        (r'(\d{1,3}(?:,\d{3})*)\s*만\s*(?:원)?', 10_000),
        # 66,000,000원
        (r'(\d{1,3}(?:,\d{3})+)\s*원', 1),
        # $48,000,000
        (r'\$\s*(\d{1,3}(?:,\d{3})+)', 1),
        # 48M, 3.74M (millions)
        (r'(\d+(?:\.\d+)?)\s*[Mm](?:illion)?', 1_000_000),
    ]

    # Keywords for total/summary rows
    TOTAL_KEYWORDS = [
        "합계", "총계", "total", "sum", "grand total",
        "소계", "subtotal", "전체", "최종"
    ]

    # Keywords for quote options
    OPTION_KEYWORDS = [
        "옵션", "option", "안", "plan", "패키지", "package",
        "basic", "standard", "enterprise", "pro"
    ]

    def __init__(self):
        """Initialize extractor."""
        self._compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), multiplier)
            for pattern, multiplier in self.AMOUNT_PATTERNS
        ]

    def extract_amounts(self, text: str) -> List[tuple]:
        """
        Extract all monetary amounts from text.

        Args:
            text: Text to parse

        Returns:
            List of (amount_decimal, original_text, position) tuples
        """
        results = []

        for pattern, multiplier in self._compiled_patterns:
            for match in pattern.finditer(text):
                try:
                    # Parse the number
                    num_str = match.group(1).replace(",", "")
                    num = float(num_str)
                    amount = Decimal(str(num * multiplier))

                    results.append((
                        amount,
                        match.group(0),
                        match.start(),
                    ))
                except (ValueError, IndexError):
                    continue

        # Sort by position
        results.sort(key=lambda x: x[2])
        return results

    def extract_from_text(self, text: str) -> List[QuoteOption]:
        """
        Extract quote options from plain text.

        Args:
            text: Text content (e.g., from PDF)

        Returns:
            List of QuoteOption objects
        """
        options = []
        amounts = self.extract_amounts(text)

        if not amounts:
            return options

        # Look for total/summary amounts
        text_lower = text.lower()

        # Find the largest amount (often the total)
        max_amount = max(amounts, key=lambda x: x[0])

        # Check if there's a clear total indicator
        for keyword in self.TOTAL_KEYWORDS:
            if keyword in text_lower:
                # Find amounts near the keyword
                keyword_pos = text_lower.find(keyword)
                nearby_amounts = [
                    a for a in amounts
                    if abs(a[2] - keyword_pos) < 200  # Within 200 chars
                ]
                if nearby_amounts:
                    total = max(nearby_amounts, key=lambda x: x[0])
                    options.append(QuoteOption(
                        option_id="total",
                        option_name="합계",
                        total_amount=total[0],
                        currency="KRW",
                        source_file=None,
                        extracted_at=datetime.now(),
                        extraction_method="rule_based",
                        confidence=0.8,
                    ))
                    return options

        # Fallback: use largest amount as primary quote
        options.append(QuoteOption(
            option_id="primary",
            option_name="견적",
            total_amount=max_amount[0],
            currency="KRW",
            source_file=None,
            extracted_at=datetime.now(),
            extraction_method="rule_based",
            confidence=0.6,
        ))

        return options

    def extract_from_table(
        self,
        data: Union[List, "pd.DataFrame"],
    ) -> List[QuoteOption]:
        """
        Extract quote options from table data.

        Args:
            data: Table data (DataFrame or list of lists)

        Returns:
            List of QuoteOption objects
        """
        options = []

        if HAS_PANDAS and isinstance(data, pd.DataFrame):
            return self._extract_from_dataframe(data)

        # List-based extraction
        return self._extract_from_list(data)

    def _extract_from_dataframe(self, df: "pd.DataFrame") -> List[QuoteOption]:
        """Extract from pandas DataFrame."""
        options = []

        # Find amount columns
        amount_cols = []
        for col in df.columns:
            col_str = str(col).lower()
            if any(kw in col_str for kw in ["금액", "amount", "가격", "price", "비용", "cost"]):
                amount_cols.append(col)

        # If no explicit amount column, try all numeric columns
        if not amount_cols:
            amount_cols = df.select_dtypes(include=['number']).columns.tolist()

        # Find total row
        for idx, row in df.iterrows():
            row_str = " ".join(str(v).lower() for v in row.values if pd.notna(v))

            if any(kw in row_str for kw in self.TOTAL_KEYWORDS):
                # Extract amount from this row
                for col in amount_cols:
                    val = row.get(col)
                    if pd.notna(val):
                        try:
                            amount = Decimal(str(val))
                            if amount > 0:
                                options.append(QuoteOption(
                                    option_id="total",
                                    option_name="합계",
                                    total_amount=amount,
                                    currency="KRW",
                                    extracted_at=datetime.now(),
                                    extraction_method="rule_based",
                                    confidence=0.9,
                                ))
                                break
                        except (ValueError, TypeError):
                            pass

        # Look for option rows
        for idx, row in df.iterrows():
            row_str = " ".join(str(v).lower() for v in row.values if pd.notna(v))

            if any(kw in row_str for kw in self.OPTION_KEYWORDS):
                for col in amount_cols:
                    val = row.get(col)
                    if pd.notna(val):
                        try:
                            amount = Decimal(str(val))
                            if amount > 0:
                                # Extract option name from first column
                                option_name = str(row.iloc[0]) if len(row) > 0 else f"Option {len(options) + 1}"
                                options.append(QuoteOption(
                                    option_id=f"opt_{len(options) + 1}",
                                    option_name=option_name[:50],
                                    total_amount=amount,
                                    currency="KRW",
                                    extracted_at=datetime.now(),
                                    extraction_method="rule_based",
                                    confidence=0.85,
                                ))
                                break
                        except (ValueError, TypeError):
                            pass

        return options

    def _extract_from_list(self, data: List) -> List[QuoteOption]:
        """Extract from list of lists."""
        options = []

        for row in data:
            if not row:
                continue

            row_str = " ".join(str(v).lower() for v in row if v is not None)

            # Check for total row
            if any(kw in row_str for kw in self.TOTAL_KEYWORDS):
                # Find numeric values in row
                for cell in row:
                    amounts = self.extract_amounts(str(cell) if cell else "")
                    if amounts:
                        options.append(QuoteOption(
                            option_id="total",
                            option_name="합계",
                            total_amount=amounts[0][0],
                            currency="KRW",
                            extracted_at=datetime.now(),
                            extraction_method="rule_based",
                            confidence=0.85,
                        ))
                        break

        return options

    def extract_from_excel(
        self,
        sheets: dict,
    ) -> List[QuoteOption]:
        """
        Extract quotes from all Excel sheets.

        Args:
            sheets: Dict mapping sheet name to DataFrame/list

        Returns:
            Combined list of QuoteOption objects
        """
        all_options = []

        for sheet_name, data in sheets.items():
            options = self.extract_from_table(data)
            for opt in options:
                opt.source_file = f"Sheet: {sheet_name}"
            all_options.extend(options)

        # Deduplicate by amount
        seen_amounts = set()
        unique = []
        for opt in all_options:
            if opt.total_amount not in seen_amounts:
                seen_amounts.add(opt.total_amount)
                unique.append(opt)

        return unique


# Singleton instance
_extractor = None

def get_quote_extractor() -> QuoteExtractor:
    """Get singleton QuoteExtractor instance."""
    global _extractor
    if _extractor is None:
        _extractor = QuoteExtractor()
    return _extractor
