"""邮件营销模块 - 模板化邮件 + 批量发送"""
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Optional

from rich.console import Console
from rich.prompt import Confirm

from config import EMAIL_CONFIG
from models import Lead
from industry_analyzer import get_sales_pitch

console = Console()


def build_email_html(lead: Lead) -> str:
    """根据客户信息生成个性化邮件HTML"""
    pitch = get_sales_pitch(lead.industry)
    company = EMAIL_CONFIG["sender_name"]
    contact = lead.contact_person or "采购负责人"
    industry_text = f"贵公司所在的{lead.industry}行业" if lead.industry else "贵公司"

    return f"""
    <div style="font-family: 'Microsoft YaHei', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px 10px 0 0;">
            <h1 style="color: white; margin: 0; font-size: 22px;">{company}</h1>
            <p style="color: rgba(255,255,255,0.9); margin: 8px 0 0 0;">专业干燥剂解决方案供应商</p>
        </div>

        <div style="background: #ffffff; padding: 30px; border: 1px solid #e0e0e0;">
            <p>尊敬的 <strong>{contact}</strong>，您好！</p>

            <p>我是{company}的业务代表。了解到{industry_text}在产品包装、仓储运输中有防潮需求，
            特此联系，希望能为贵司提供专业的干燥剂解决方案。</p>

            <div style="background: #f8f9fa; padding: 15px; border-left: 4px solid #667eea; margin: 20px 0;">
                <strong>我们的优势：</strong>{pitch}
            </div>

            <p><strong>我们可以提供：</strong></p>
            <ul style="line-height: 2;">
                <li>免费样品寄送，先试用再决定</li>
                <li>根据贵司产品定制干燥剂规格和包装</li>
                <li>厂家直供，价格优势明显</li>
                <li>完善的质检报告和资质证书</li>
            </ul>

            <p>如果您有任何防潮需求，欢迎随时联系我们，我们可以安排技术人员上门沟通方案。</p>

            <div style="text-align: center; margin: 25px 0;">
                <a href="mailto:{EMAIL_CONFIG['sender_email']}"
                   style="background: #667eea; color: white; padding: 12px 30px;
                          text-decoration: none; border-radius: 5px; font-size: 16px;">
                    回复咨询
                </a>
            </div>
        </div>

        <div style="background: #f5f5f5; padding: 20px; border-radius: 0 0 10px 10px;
                    text-align: center; color: #666; font-size: 12px;">
            <p>{company} | 电话: 请在config.py中配置</p>
            <p style="color: #999;">如不希望收到此类邮件，请回复"退订"</p>
        </div>
    </div>
    """


def build_subject(lead: Lead) -> str:
    """生成邮件主题"""
    if lead.industry:
        return f"【{EMAIL_CONFIG['sender_name']}】{lead.industry}防潮解决方案 - 免费样品试用"
    return f"【{EMAIL_CONFIG['sender_name']}】专业干燥剂供应 - 免费样品试用"

def send_email(to_email: str, subject: str, html_body: str) -> bool:
    """发送单封邮件"""
    cfg = EMAIL_CONFIG
    msg = MIMEMultipart("alternative")
    msg["From"] = f"{cfg['sender_name']} <{cfg['sender_email']}>"
    msg["To"] = to_email
    msg["Subject"] = Header(subject, "utf-8")

    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        server = smtplib.SMTP_SSL(cfg["smtp_server"], cfg["smtp_port"])
        server.login(cfg["sender_email"], cfg["sender_password"])
        server.sendmail(cfg["sender_email"], [to_email], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        console.print(f"[red]发送失败 -> {to_email}: {e}[/red]")
        return False

def batch_send(leads: list[Lead], dry_run: bool = True) -> dict:
    """批量发送营销邮件"""
    email_leads = [l for l in leads if l.email]

    if not email_leads:
        console.print("[yellow]没有包含邮箱的客户线索[/yellow]")
        return {"total": 0, "success": 0, "failed": 0}

    console.print(f"\n[bold]准备发送邮件给 {len(email_leads)} 个客户[/bold]")

    if dry_run:
        console.print("[yellow]【预览模式】以下邮件不会真正发送：[/yellow]\n")
        for i, lead in enumerate(email_leads[:5], 1):
            console.print(f"  {i}. {lead.company_name} -> {lead.email}")
            console.print(f"     主题: {build_subject(lead)}")
        if len(email_leads) > 5:
            console.print(f"  ... 还有 {len(email_leads) - 5} 封")
        console.print("\n[cyan]如需真正发送，请先配置 config.py 中的邮箱信息，然后使用 --send 参数[/cyan]")
        return {"total": len(email_leads), "success": 0, "failed": 0, "mode": "dry_run"}

    if not Confirm.ask(f"确认发送 {len(email_leads)} 封邮件？"):
        console.print("[yellow]已取消发送[/yellow]")
        return {"total": 0, "success": 0, "failed": 0}

    success = 0
    failed = 0

    for i, lead in enumerate(email_leads, 1):
        subject = build_subject(lead)
        html = build_email_html(lead)

        console.print(f"[{i}/{len(email_leads)}] 发送给 {lead.company_name} ({lead.email})...", end=" ")
        if send_email(lead.email, subject, html):
            console.print("[green]成功[/green]")
            success += 1
        else:
            console.print("[red]失败[/red]")
            failed += 1

        time.sleep(3)

    result = {"total": len(email_leads), "success": success, "failed": failed}
    console.print(f"\n[bold]发送完成: 成功 {success}, 失败 {failed}[/bold]")
    return result
