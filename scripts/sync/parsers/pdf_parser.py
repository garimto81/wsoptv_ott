"""PDF parser for text and table extraction."""

from pathlib import Path
from typing import List, Optional

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


class PDFParser:
    """Extract text and tables from PDF files."""

    def __init__(self):
        """Initialize parser."""
        if not HAS_PDFPLUMBER:
            print("Warning: pdfplumber not installed. Install with: pip install pdfplumber")

    def extract_text(self, path: Path) -> str:
        """
        Extract all text from PDF.

        Args:
            path: Path to PDF file

        Returns:
            Extracted text content
        """
        if not HAS_PDFPLUMBER:
            raise ImportError("pdfplumber required: pip install pdfplumber")

        text_parts = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

        return "\n\n".join(text_parts)

    def extract_tables(self, path: Path) -> List:
        """
        Extract tables from PDF.

        Args:
            path: Path to PDF file

        Returns:
            List of pandas DataFrames (or list of lists if pandas not available)
        """
        if not HAS_PDFPLUMBER:
            raise ImportError("pdfplumber required: pip install pdfplumber")

        tables = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                for table in page_tables:
                    if table and len(table) > 1:  # Has header + data
                        if HAS_PANDAS:
                            # Convert to DataFrame
                            header = table[0]
                            data = table[1:]
                            df = pd.DataFrame(data, columns=header)
                            tables.append(df)
                        else:
                            tables.append(table)

        return tables

    def extract_all(self, path: Path) -> dict:
        """
        Extract both text and tables.

        Args:
            path: Path to PDF file

        Returns:
            Dict with 'text' and 'tables' keys
        """
        return {
            "text": self.extract_text(path),
            "tables": self.extract_tables(path),
            "page_count": self._get_page_count(path),
        }

    def _get_page_count(self, path: Path) -> int:
        """Get number of pages in PDF."""
        if not HAS_PDFPLUMBER:
            return 0

        with pdfplumber.open(path) as pdf:
            return len(pdf.pages)


# Singleton instance
_parser = None

def get_pdf_parser() -> PDFParser:
    """Get singleton PDFParser instance."""
    global _parser
    if _parser is None:
        _parser = PDFParser()
    return _parser
