"""干燥剂行业潜在客户获取与管理系统 - 主入口"""
import sys
import os

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt

from config import TARGET_INDUSTRIES
from industry_analyzer import show_industry_analysis
from scraper import scrape_all, scrape_by_keyword
from data_manager import (
    save_leads_json, load_leads_json,
    deduplicate, export_excel, show_summary, ensure_dirs,
)
from email_sender import batch_send, build_email_html

console = Console()

BANNER = """
[bold cyan]╔══════════════════════════════════════════════════╗
║     干燥剂行业 · 对应客户获取与管理系统          ║
║                                                  ║
║  功能: 行业分析 | 对应客户获取 | 数据管理 | 邮件营销 ║
╚══════════════════════════════════════════════════╝[/bold cyan]
"""

def show_menu():
    console.print(BANNER)
    console.print("[bold]请选择功能：[/bold]\n")
    console.print("  [1] 查看行业分析报告（了解哪些行业需要干燥剂）")
    console.print("  [2] 按行业获取对应客户")
    console.print("  [3] 按关键词获取对应客户")
    console.print("  [4] 查看已获取的客户数据")
    console.print("  [5] 导出客户名单到 Excel")
    console.print("  [6] 预览营销邮件")
    console.print("  [7] 发送营销邮件（需先配置邮箱）")
    console.print("  [0] 退出\n")
    return Prompt.ask("请输入编号", choices=["0","1","2","3","4","5","6","7"], default="1")


def action_industry_analysis():
    show_industry_analysis()


def action_scrape_by_industry():
    console.print("\n[bold]可选行业：[/bold]")
    industries = list(TARGET_INDUSTRIES.keys())
    for i, ind in enumerate(industries, 1):
        console.print(f"  [{i}] {ind}")
    console.print(f"  [0] 全部行业")

    choice = Prompt.ask("\n请输入行业编号（多个用逗号分隔，如 1,3,5）", default="0")

    if choice.strip() == "0":
        selected = industries
    else:
        indices = [int(x.strip()) for x in choice.split(",") if x.strip().isdigit()]
        selected = [industries[i - 1] for i in indices if 0 < i <= len(industries)]

    if not selected:
        console.print("[red]未选择有效行业[/red]")
        return

    console.print(f"\n[cyan]将获取以下行业的对应客户: {', '.join(selected)}[/cyan]\n")
    leads = scrape_all(industries=selected)
    leads = deduplicate(leads)
    save_leads_json(leads)
    show_summary(leads)


def action_scrape_by_keyword():
    keyword = Prompt.ask("请输入搜索关键词（如：食品厂 干燥剂）")
    if not keyword.strip():
        return
    leads = scrape_by_keyword(keyword.strip())
    leads = deduplicate(leads)
    save_leads_json(leads)
    show_summary(leads)


def action_view_data():
    leads = load_leads_json()
    if not leads:
        console.print("[yellow]暂无数据，请先执行采集[/yellow]")
        return
    show_summary(leads)


def action_export_excel():
    leads = load_leads_json()
    if not leads:
        console.print("[yellow]暂无数据，请先执行采集[/yellow]")
        return
    leads = deduplicate(leads)
    export_excel(leads)
    console.print(f"\n[bold]提示: 用 Excel 打开 output/潜在客户名单.xlsx 查看[/bold]")


def action_preview_email():
    leads = load_leads_json()
    if not leads:
        console.print("[yellow]暂无数据[/yellow]")
        return
    batch_send(leads, dry_run=True)


def action_send_email():
    leads = load_leads_json()
    if not leads:
        console.print("[yellow]暂无数据[/yellow]")
        return
    console.print(Panel(
        "[bold red]注意：发送前请确保已在 config.py 中配置正确的邮箱信息！[/bold red]\n"
        "smtp_server / sender_email / sender_password",
        title="邮件配置提醒",
    ))
    batch_send(leads, dry_run=False)

def main():
    ensure_dirs()

    actions = {
        "1": action_industry_analysis,
        "2": action_scrape_by_industry,
        "3": action_scrape_by_keyword,
        "4": action_view_data,
        "5": action_export_excel,
        "6": action_preview_email,
        "7": action_send_email,
    }

    while True:
        try:
            choice = show_menu()
            if choice == "0":
                console.print("[cyan]再见！祝生意兴隆！[/cyan]")
                break
            action = actions.get(choice)
            if action:
                action()
            console.print("\n" + "─" * 50 + "\n")
        except KeyboardInterrupt:
            console.print("\n[cyan]已退出[/cyan]")
            break
        except Exception as e:
            console.print(f"[red]出错了: {e}[/red]")


if __name__ == "__main__":
    main()
