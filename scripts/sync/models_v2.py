"""Data models for Slack Lists sync v2."""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, computed_field


class VendorStatus(str, Enum):
    """업체 진행 상태 (상태 머신)"""
    INITIAL_CONTACT = "initial_contact"
    RFP_SENT = "rfp_sent"
    QUOTE_WAITING = "quote_waiting"
    QUOTE_RECEIVED = "quote_received"
    REVIEWING = "reviewing"
    NEGOTIATING = "negotiating"
    CONTRACT_REVIEW = "contract_review"
    ON_HOLD = "on_hold"
    EXCLUDED = "excluded"


class CommunicationDirection(str, Enum):
    """커뮤니케이션 방향"""
    INBOUND = "inbound"   # 업체 → 우리
    OUTBOUND = "outbound" # 우리 → 업체


class EmailThread(BaseModel):
    """이메일 스레드 분석 결과"""
    thread_id: str
    vendor: str
    message_count: int = 0
    inbound_count: int = 0   # 업체에서 온 메일 수
    outbound_count: int = 0  # 우리가 보낸 메일 수
    first_date: Optional[datetime] = None
    last_date: Optional[datetime] = None
    last_direction: Optional[CommunicationDirection] = None
    avg_response_time_hours: Optional[float] = None

    @computed_field
    @property
    def is_active_negotiation(self) -> bool:
        """양방향 커뮤니케이션 = 협상 진행 중"""
        return self.inbound_count >= 1 and self.outbound_count >= 1


class QuoteOption(BaseModel):
    """견적 옵션 (하나의 업체가 여러 옵션 제공 가능)"""
    option_id: str = ""  # 예: "A", "Basic", "Enterprise"
    option_name: str = ""
    total_amount: Optional[Decimal] = None
    currency: str = "KRW"
    period_months: Optional[int] = None
    breakdown: Dict[str, Decimal] = Field(default_factory=dict)
    conditions: List[str] = Field(default_factory=list)
    source_file: Optional[str] = None
    extracted_at: Optional[datetime] = None
    extraction_method: str = "rule_based"  # rule_based | ai_assisted | manual
    confidence: float = 1.0  # 추출 신뢰도 (0.0 ~ 1.0)

    @computed_field
    @property
    def total_amount_display(self) -> str:
        """금액 표시용 문자열"""
        if self.total_amount is None:
            return "-"
        amount = float(self.total_amount)
        if amount >= 100_000_000:  # 1억 이상
            return f"{amount / 100_000_000:.1f}억원"
        elif amount >= 10_000:  # 1만원 이상
            return f"{amount / 10_000:.0f}만원"
        return f"{amount:,.0f}원"


class VendorQuote(BaseModel):
    """업체별 견적 (다중 옵션 포함)"""
    vendor: str
    options: List[QuoteOption] = Field(default_factory=list)
    received_date: Optional[datetime] = None
    valid_until: Optional[datetime] = None

    @computed_field
    @property
    def primary_option(self) -> Optional[QuoteOption]:
        """기본 옵션 (첫 번째)"""
        return self.options[0] if self.options else None

    @computed_field
    @property
    def total_options(self) -> int:
        return len(self.options)

    @computed_field
    @property
    def summary(self) -> str:
        """견적 요약 문자열"""
        if not self.options:
            return "미수령"
        if len(self.options) == 1:
            return self.options[0].total_amount_display
        return f"{self.options[0].total_amount_display} 외 {len(self.options)-1}개 옵션"


class Attachment(BaseModel):
    """첨부파일 상세 정보"""
    id: str
    email_id: str
    filename: str
    mime_type: str
    size: int = 0
    local_path: Optional[str] = None
    parsed: bool = False
    parse_result: Optional[Dict] = None

    @computed_field
    @property
    def is_quote_file(self) -> bool:
        """견적 관련 파일인지 판단"""
        quote_keywords = ["견적", "quote", "proposal", "제안", "estimate"]
        filename_lower = self.filename.lower()
        return any(kw in filename_lower for kw in quote_keywords)

    @computed_field
    @property
    def file_type(self) -> str:
        """파일 타입 (pdf, excel, other)"""
        if self.mime_type == "application/pdf" or self.filename.endswith(".pdf"):
            return "pdf"
        if "spreadsheet" in self.mime_type or self.filename.endswith((".xlsx", ".xls")):
            return "excel"
        return "other"


class StatusTransition(BaseModel):
    """상태 전이 기록"""
    from_status: VendorStatus
    to_status: VendorStatus
    trigger: str  # 전이 원인
    confidence: float = 1.0  # 1.0 = 확실 (규칙), <1.0 = AI 추론
    evidence: List[str] = Field(default_factory=list)
    requires_approval: bool = False
    detected_at: datetime = Field(default_factory=datetime.now)


class VendorState(BaseModel):
    """업체 전체 상태 (Slack Lists Row에 매핑)"""
    vendor_name: str
    status: VendorStatus = VendorStatus.INITIAL_CONTACT
    quote: VendorQuote = Field(default_factory=lambda: VendorQuote(vendor=""))
    threads: List[EmailThread] = Field(default_factory=list)
    attachments: List[Attachment] = Field(default_factory=list)
    last_contact: Optional[datetime] = None
    next_action: Optional[str] = None
    notes: str = ""

    # 메타데이터
    updated_at: datetime = Field(default_factory=datetime.now)
    update_source: str = "auto"  # auto | manual | ai

    def model_post_init(self, __context) -> None:
        """초기화 후 vendor 이름 동기화"""
        if not self.quote.vendor:
            self.quote = VendorQuote(vendor=self.vendor_name, options=self.quote.options)

    @computed_field
    @property
    def has_active_negotiation(self) -> bool:
        """활성 협상 여부"""
        return any(t.is_active_negotiation for t in self.threads)

    @computed_field
    @property
    def quote_summary(self) -> str:
        """견적 요약"""
        return self.quote.summary


# Re-export existing models for backward compatibility
try:
    from .models import SyncResult, EmailDirection, EmailLogEntry, SlackDecision, SlackActionItem
except ImportError:
    from models import SyncResult, EmailDirection, EmailLogEntry, SlackDecision, SlackActionItem
