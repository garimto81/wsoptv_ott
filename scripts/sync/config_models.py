"""Configuration models for Slack Lists sync v2."""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class VendorMapping(BaseModel):
    """업체 도메인 → 이름 매핑"""
    name: str
    domains: List[str]
    keywords: List[str] = Field(default_factory=list)
    slack_list_row_id: Optional[str] = None


class SlackListsConfig(BaseModel):
    """Slack Lists 설정"""
    list_id: str
    team_id: str
    channel_id: str
    pinned_message_ts: Optional[str] = None
    columns: Dict[str, str] = Field(default_factory=dict)
    status_options: Dict[str, str] = Field(default_factory=dict)


class StatusTransitionRule(BaseModel):
    """상태 전이 규칙"""
    from_status: str  # "*" = any
    to_status: str
    triggers: List[str]
    direction: str = "positive"  # positive | negative
    auto_apply: bool = True


class ProjectConfig(BaseModel):
    """프로젝트별 설정 (YAML 파일에서 로드)"""
    project_name: str
    gmail_label: str
    slack_channel_id: str

    vendors: List[VendorMapping] = Field(default_factory=list)
    slack_lists: Optional[SlackListsConfig] = None
    status_rules: List[StatusTransitionRule] = Field(default_factory=list)

    # 파일 경로
    attachments_dir: Path = Path("./attachments")
    state_file: Path = Path("./.sync_state_v2.json")

    # AI 설정
    enable_ai_analysis: bool = False
    ai_model: str = "claude-3-haiku"

    @classmethod
    def from_yaml(cls, path: Path) -> "ProjectConfig":
        """YAML 파일에서 설정 로드"""
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # Convert nested dicts to models
        if "vendors" in data:
            data["vendors"] = [VendorMapping(**v) for v in data["vendors"]]
        if "slack_lists" in data:
            data["slack_lists"] = SlackListsConfig(**data["slack_lists"])
        if "status_rules" in data:
            data["status_rules"] = [StatusTransitionRule(**r) for r in data["status_rules"]]
        if "attachments_dir" in data:
            data["attachments_dir"] = Path(data["attachments_dir"])
        if "state_file" in data:
            data["state_file"] = Path(data["state_file"])

        return cls(**data)

    def get_vendor_by_domain(self, email: str) -> Optional[VendorMapping]:
        """이메일 도메인으로 업체 찾기"""
        email_lower = email.lower()
        for vendor in self.vendors:
            for domain in vendor.domains:
                if domain.lower() in email_lower:
                    return vendor
        return None

    def get_vendor_by_name(self, name: str) -> Optional[VendorMapping]:
        """업체명으로 찾기"""
        name_lower = name.lower()
        for vendor in self.vendors:
            if vendor.name.lower() == name_lower:
                return vendor
        return None
