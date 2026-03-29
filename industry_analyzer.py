"""潜在客户行业分析模块 - 分析哪些行业/企业需要干燥剂"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from config import TARGET_INDUSTRIES

console = Console()


INDUSTRY_ANALYSIS = {
    "食品加工": {
        "需求等级": "★★★★★",
        "应用场景": "食品包装内置干燥剂防潮保鲜，茶叶/坚果/饼干/奶粉等必备",
        "推荐产品": "食品级硅胶干燥剂、蒙脱石干燥剂",
        "采购特点": "量大、持续采购、对食品安全认证要求高",
        "切入话术": "我们的干燥剂通过FDA/食品级认证，专为食品包装设计",
    },
    "医药制造": {
        "需求等级": "★★★★★",
        "应用场景": "药品瓶内干燥剂、医疗器械包装防潮",
        "推荐产品": "药用硅胶干燥剂、分子筛干燥剂",
        "采购特点": "品质要求极高、需要GMP认证、利润空间大",
        "切入话术": "我们具备药用干燥剂GMP生产资质，可提供验证文件",
    },
    "电子产品": {
        "需求等级": "★★★★☆",
        "应用场景": "电子元器件/PCB板/芯片存储和运输防潮",
        "推荐产品": "硅胶干燥剂、氯化钙干燥剂、湿度指示卡",
        "采购特点": "对吸湿速率和容量有技术指标要求",
        "切入话术": "我们的干燥剂吸湿率高达300%，配合湿度指示卡使用",
    },
    "皮革鞋业": {
        "需求等级": "★★★★☆",
        "应用场景": "鞋盒/皮具包装内防霉防潮",
        "推荐产品": "硅胶干燥剂、蒙脱石干燥剂",
        "采购特点": "季节性采购高峰（出口旺季前）、量大价敏感",
        "切入话术": "我们为多家鞋厂提供定制包装干燥剂，支持印刷LOGO",
    },
    "服装纺织": {
        "需求等级": "★★★☆☆",
        "应用场景": "服装仓储和出口运输防潮防霉",
        "推荐产品": "硅胶干燥剂、集装箱干燥剂",
        "采购特点": "出口企业需求大，内销企业需求一般",
        "切入话术": "出口服装集装箱防潮方案，避免海运霉变索赔",
    },
    "仓储物流": {
        "需求等级": "★★★★☆",
        "应用场景": "集装箱运输防潮、仓库除湿",
        "推荐产品": "集装箱干燥剂（氯化钙）、悬挂式干燥剂",
        "采购特点": "单次用量大（每柜10-20条）、持续复购",
        "切入话术": "一条干燥剂保护一柜货，避免数万元霉变损失",
    },
    "汽车零部件": {
        "需求等级": "★★★☆☆",
        "应用场景": "汽车零部件包装和仓储防锈防潮",
        "推荐产品": "硅胶干燥剂、VCI防锈干燥剂",
        "采购特点": "配合防锈需求，技术门槛较高",
        "切入话术": "防潮+防锈二合一方案，降低零部件仓储损耗",
    },
    "光学仪器": {
        "需求等级": "★★★★☆",
        "应用场景": "镜头/仪器防雾防潮",
        "推荐产品": "变色硅胶干燥剂、分子筛干燥剂",
        "采购特点": "量小但单价高、品质要求极高",
        "切入话术": "精密仪器专用干燥剂，超低粉尘，可重复再生使用",
    },
    "家具木材": {
        "需求等级": "★★★☆☆",
        "应用场景": "木材/家具仓储和出口运输防潮",
        "推荐产品": "集装箱干燥剂、大包装工业干燥剂",
        "采购特点": "出口家具企业需求大",
        "切入话术": "木材出口防潮整体解决方案，减少退货率",
    },
    "金属加工": {
        "需求等级": "★★★☆☆",
        "应用场景": "金属制品/五金件防锈防潮",
        "推荐产品": "硅胶干燥剂、氯化钙干燥剂",
        "采购特点": "配合防锈油/防锈纸使用",
        "切入话术": "金属制品防锈防潮组合方案，成本更低效果更好",
    },
}


def show_industry_analysis():
    """展示行业分析报告"""
    console.print(Panel("[bold cyan]干燥剂行业潜在客户分析报告[/bold cyan]", expand=False))

    table = Table(title="目标行业需求分析", show_lines=True)
    table.add_column("行业", style="bold yellow", width=12)
    table.add_column("需求等级", width=10)
    table.add_column("应用场景", width=30)
    table.add_column("推荐产品", width=25)
    table.add_column("采购特点", width=25)

    for industry, info in INDUSTRY_ANALYSIS.items():
        table.add_row(
            industry,
            info["需求等级"],
            info["应用场景"],
            info["推荐产品"],
            info["采购特点"],
        )

    console.print(table)


def get_search_keywords_for_industry(industry: str) -> list[str]:
    """根据行业生成搜索关键词"""
    base_keywords = TARGET_INDUSTRIES.get(industry, [])
    result = []
    for kw in base_keywords:
        result.append(kw)
        result.append(f"{kw} 联系方式")
        result.append(f"{kw} 采购")
    return result


def get_sales_pitch(industry: str) -> str:
    """获取行业对应的销售话术"""
    info = INDUSTRY_ANALYSIS.get(industry, {})
    return info.get("切入话术", "我们是专业干燥剂生产厂家，产品齐全，价格优惠")


if __name__ == "__main__":
    show_industry_analysis()
