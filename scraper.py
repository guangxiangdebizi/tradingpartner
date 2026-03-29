"""目标客户采集模块

策略调整：
1. 不再搜索“行业 + 干燥剂”，避免搜到同行或供应商。
2. 改为搜索“目标行业企业 + 联系方式/电话”等关键词。
3. 对搜索结果做一层客户匹配过滤，只保留更像目标客户的公司。
"""
import random
import re
import time
from typing import Optional
from urllib.parse import quote, urljoin

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from config import (
    CUSTOMER_QUERY_SUFFIXES,
    EXCLUDED_COMPANY_KEYWORDS,
    MAX_PAGES,
    QUERY_NOISE_TERMS,
    REQUEST_DELAY_MAX,
    REQUEST_DELAY_MIN,
    REQUEST_TIMEOUT,
    TARGET_INDUSTRIES,
)
from models import Lead

console = Console()

COMPANY_PATTERN = re.compile(
    r"([\u4e00-\u9fa5A-Za-z0-9（）()·\-]{4,40}?"
    r"(?:有限责任公司|股份有限公司|集团有限公司|有限公司|集团|工厂|企业|公司|厂))"
)
GENERIC_NAME_KEYWORDS = ("搜索", "关注", "推荐", "下载", "附近", "电话邦", "元宝")


class SessionManager:
    """管理 HTTP 会话，自动轮换 UA 并控制请求频率。"""

    def __init__(self):
        self.session = requests.Session()
        try:
            self.ua = UserAgent()
        except Exception:
            self.ua = None
        self._update_headers()

    def _update_headers(self):
        ua_string = self.ua.random if self.ua else (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.session.headers.update({
            "User-Agent": ua_string,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Referer": "https://www.sogou.com/",
        })

    def get(self, url: str, **kwargs) -> Optional[requests.Response]:
        self._update_headers()
        delay = random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX)
        time.sleep(delay)
        try:
            resp = self.session.get(url, timeout=REQUEST_TIMEOUT, **kwargs)
            if not resp.encoding or resp.encoding.lower() == "iso-8859-1":
                resp.encoding = resp.apparent_encoding
            resp.raise_for_status()
            return resp
        except requests.RequestException as e:
            console.print(f"[red]请求失败: {url} -> {e}[/red]")
            return None


def _normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "")
    return text.strip()


def _normalize_company_text(text: str) -> str:
    text = _normalize_text(text)
    text = re.sub(r"(?<=[\u4e00-\u9fa5A-Za-z0-9])\s+(?=[\u4e00-\u9fa5A-Za-z0-9])", "", text)
    return text


def _extract_phone(text: str) -> list[str]:
    patterns = [
        r"1[3-9]\d{9}",
        r"1[3-9]\d{2}\*{4}\d{4}",
        r"(?:0\d{2,3}[-\s]?)?\d{7,8}",
        r"0\d{2,3}\*{3,4}\d{3,4}",
        r"400[-\s]?\d{3}[-\s]?\d{4}",
        r"400\d?\*{3}\d{3}",
    ]
    phones: list[str] = []
    for pattern in patterns:
        phones.extend(re.findall(pattern, text))
    return list(dict.fromkeys(phones))


def _extract_email(text: str) -> list[str]:
    patterns = [
        r"[a-zA-Z0-9._%+\-*]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
    ]
    emails: list[str] = []
    for pattern in patterns:
        emails.extend(re.findall(pattern, text))
    return list(dict.fromkeys(emails))


def _extract_address(text: str) -> str:
    match = re.search(
        r"(?:地址|企业地址)[:：]?\s*"
        r"(.{6,60}?)(?=\s*(?:电话|邮箱|传真|官网|介绍|经营范围|$))",
        text,
    )
    return match.group(1).strip() if match else ""


def _guess_company_name(text: str) -> str:
    candidates = COMPANY_PATTERN.findall(_normalize_company_text(text))
    if not candidates:
        return ""

    cleaned = []
    for candidate in candidates:
        candidate = candidate.strip(" -|_，,。.：:；;()（）[]【】")
        if candidate and candidate not in cleaned:
            cleaned.append(candidate)

    return cleaned[0] if cleaned else ""


def _is_generic_company_name(company: str, query: str) -> bool:
    if not company:
        return True
    if any(word in company for word in GENERIC_NAME_KEYWORDS):
        return True

    bare = re.sub(
        r"(有限责任公司|股份有限公司|集团有限公司|有限公司|集团|工厂|企业|公司|厂)$",
        "",
        company,
    )
    bare = bare.strip()
    query_base = _normalize_company_text(query)
    query_bare = re.sub(r"(联系方式|电话|邮箱|地址|公司|企业|厂家|工厂|厂)$", "", query_base)

    if company == query_base or bare == query_base:
        return True
    if query_bare and bare == query_bare:
        return True
    if len(bare) <= 2:
        return True
    if len(company) <= 6 and company.endswith("厂"):
        return True
    if bare in TARGET_INDUSTRIES.get(query, []):
        return True
    return False


def _score_candidate(company: str, text: str, industry: str, query: str) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    haystack = _normalize_text(f"{company} {text}")

    for blocked in EXCLUDED_COMPANY_KEYWORDS:
        if blocked in haystack:
            return -99, [f"排除词:{blocked}"]

    query_terms = [
        term for term in re.split(r"\s+", query)
        if term and term not in QUERY_NOISE_TERMS
    ]
    expanded_terms: list[str] = []
    for term in query_terms:
        expanded_terms.append(term)
        stripped = re.sub(r"(公司|企业|厂家|工厂|厂|生产|加工|中心|仓储|代理|器械)$", "", term)
        if len(stripped) >= 2:
            expanded_terms.append(stripped)

    industry_terms = TARGET_INDUSTRIES.get(industry, [])

    if industry and industry in haystack:
        score += 2
        reasons.append(industry)

    for term in list(dict.fromkeys(expanded_terms + industry_terms)):
        if term in company:
            score += 2
            reasons.append(term)
        elif term in haystack:
            score += 1
            reasons.append(term)

    if _extract_phone(text):
        score += 1
        reasons.append("电话")
    if _extract_email(text):
        score += 1
        reasons.append("邮箱")
    if _extract_address(text):
        score += 1
        reasons.append("地址")

    if company.endswith(("有限公司", "有限责任公司", "股份有限公司", "工厂", "厂", "公司")):
        score += 1

    return score, list(dict.fromkeys(reasons))


def _build_lead(text: str, title: str, href: str, industry: str, query: str, source_name: str) -> Optional[Lead]:
    company = _guess_company_name(title) or _guess_company_name(text)
    if not company or _is_generic_company_name(company, query):
        return None

    score, reasons = _score_candidate(company, text, industry, query)
    if score < 3:
        return None

    phones = _extract_phone(text)
    emails = _extract_email(text)
    address = _extract_address(text)
    if not (phones or emails or address) and not company.endswith(
        ("有限公司", "有限责任公司", "股份有限公司", "公司", "企业")
    ):
        return None

    notes = f"搜索词: {query}; 匹配依据: {', '.join(reasons[:5])}; 匹配分: {score}"

    return Lead(
        company_name=company,
        industry=industry,
        phone=phones[0] if phones else "",
        email=emails[0] if emails else "",
        address=address,
        source=f"{source_name}-{query}",
        website=href,
        business_scope=text[:120],
        notes=notes,
    )


def build_customer_queries(base_keyword: str) -> list[str]:
    """基于一个行业关键词构造更偏向目标客户的搜索词。"""
    preferred_order = [
        base_keyword,
        f"{base_keyword} 联系方式",
        f"{base_keyword} 电话",
        f"{base_keyword} 公司",
        f"{base_keyword} 企业",
    ]
    queries = preferred_order[:]
    for suffix in CUSTOMER_QUERY_SUFFIXES:
        queries.append(f"{base_keyword} {suffix}")
    return list(dict.fromkeys(queries))


class SogouSearchScraper:
    """通过搜狗结果页抓取公开企业线索。"""

    BASE_URL = "https://www.sogou.com/web"

    def __init__(self, session_mgr: SessionManager):
        self.sm = session_mgr
        self.blocked = False

    @staticmethod
    def _is_blocked(resp: requests.Response) -> bool:
        text = resp.text
        return (
            "antispider" in resp.url
            or "请输入验证码" in text
            or "访问受限" in text
        )

    def search(self, query: str, industry: str = "", max_pages: int = 1) -> list[Lead]:
        if self.blocked:
            console.print("[yellow]搜索源已触发限制，建议稍后再试[/yellow]")
            return []

        leads: list[Lead] = []
        console.print(f"[cyan]搜狗搜索目标客户: {query}[/cyan]")

        for page in range(1, max_pages + 1):
            url = f"{self.BASE_URL}?query={quote(query)}&page={page}"
            resp = self.sm.get(url, allow_redirects=True)
            if not resp:
                continue

            if self._is_blocked(resp):
                console.print("[yellow]搜狗触发反爬限制，本轮跳过该关键词[/yellow]")
                self.blocked = True
                break

            soup = BeautifulSoup(resp.text, "lxml")
            result_blocks = soup.select("div.vrwrap, div.rb, div.reactResult")
            if not result_blocks:
                console.print("[yellow]未解析到搜索结果，可能是页面结构变化或结果为空[/yellow]")
                continue

            for item in result_blocks:
                text = _normalize_text(item.get_text(" ", strip=True))
                if not text or len(text) < 10:
                    continue

                link_el = item.select_one("a[href]")
                href = urljoin("https://www.sogou.com", link_el.get("href", "")) if link_el else ""
                title = _normalize_text(link_el.get_text(" ", strip=True)) if link_el else ""

                lead = _build_lead(text, title, href, industry, query, "搜狗")
                if lead:
                    leads.append(lead)

        console.print(f"[green]  -> 找到 {len(leads)} 条目标客户线索[/green]")
        return leads


def scrape_all(industries: list[str] = None, max_pages: int = None) -> list[Lead]:
    """对指定行业执行目标客户采集。"""
    if max_pages is None:
        max_pages = min(MAX_PAGES, 1)

    if industries is None:
        industries = list(TARGET_INDUSTRIES.keys())

    sm = SessionManager()
    sogou = SogouSearchScraper(sm)
    all_leads: list[Lead] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("采集中...", total=len(industries))

        for industry in industries:
            progress.update(task, description=f"正在获取对应客户: {industry}")
            keywords = TARGET_INDUSTRIES.get(industry, [])[:2]

            for keyword in keywords:
                for query in build_customer_queries(keyword)[:3]:
                    all_leads.extend(sogou.search(query, industry=industry, max_pages=max_pages))

            progress.advance(task)

    console.print(f"\n[bold green]采集完成！共获取 {len(all_leads)} 条原始客户线索[/bold green]")
    return all_leads


def scrape_by_keyword(keyword: str, max_pages: int = 1) -> list[Lead]:
    """按自定义关键词采集目标客户。"""
    sm = SessionManager()
    sogou = SogouSearchScraper(sm)

    leads: list[Lead] = []
    for query in build_customer_queries(keyword)[:3]:
        leads.extend(sogou.search(query, max_pages=max_pages))

    console.print(f"\n[bold green]关键词 '{keyword}' 采集完成，共 {len(leads)} 条客户线索[/bold green]")
    return leads
