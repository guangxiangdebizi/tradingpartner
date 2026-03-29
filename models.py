"""数据模型定义"""
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime


@dataclass
class Lead:
    """潜在客户数据模型"""
    company_name: str
    industry: str = ""
    contact_person: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    source: str = ""
    website: str = ""
    business_scope: str = ""
    status: str = "未联系"  # 未联系 / 已联系 / 有意向 / 无需求
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def headers() -> list:
        return [
            "公司名称", "所属行业", "联系人", "电话", "邮箱",
            "地址", "来源", "官网", "经营范围", "跟进状态",
            "备注", "采集时间",
        ]

    def to_row(self) -> list:
        return [
            self.company_name, self.industry, self.contact_person,
            self.phone, self.email, self.address, self.source,
            self.website, self.business_scope, self.status,
            self.notes, self.created_at,
        ]
