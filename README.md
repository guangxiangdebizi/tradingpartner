<div align="center">

# 🏭 TradingPartner — 干燥剂行业客户开发系统

**智能采集 · 行业分析 · 精准营销 · 一站式 B2B 获客工具**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge)]()

<br>

<img src="https://img.shields.io/badge/-%E6%90%9C%E7%B4%A2%E5%BC%95%E6%93%8E%E9%87%87%E9%9B%86-blue?style=flat-square" alt="搜索引擎采集">
<img src="https://img.shields.io/badge/-%E6%99%BA%E8%83%BD%E5%8E%BB%E9%87%8D-orange?style=flat-square" alt="智能去重">
<img src="https://img.shields.io/badge/-Excel%E5%AF%BC%E5%87%BA-success?style=flat-square" alt="Excel导出">
<img src="https://img.shields.io/badge/-%E9%82%AE%E4%BB%B6%E8%90%A5%E9%94%80-red?style=flat-square" alt="邮件营销">

</div>

---

## 📖 项目简介

**TradingPartner** 是一款专为干燥剂行业销售团队打造的 **B2B 潜在客户开发工具**。

在干燥剂行业中，食品加工、医药制造、电子产品等下游行业对防潮产品有着刚性需求，但传统获客方式效率低下。本工具通过 **搜索引擎智能采集 → 数据清洗去重 → 行业需求分析 → 精准邮件营销** 的完整链路，帮助销售人员快速建立目标客户池，大幅提升获客效率。

### 核心工作流

```
🔍 搜索采集          📊 数据处理          📧 精准触达
   │                    │                    │
   ├─ 搜狗搜索引擎      ├─ 智能去重合并       ├─ 行业定制话术
   ├─ 10大目标行业      ├─ 评分过滤机制       ├─ 个性化HTML邮件
   ├─ 自动翻页采集      ├─ Excel格式化导出    ├─ 批量发送+预览
   └─ 反爬策略保护      └─ JSON持久化存储     └─ 发送间隔控制
```

---

## ✨ 功能特性

<table>
<tr>
<td width="50%">

### 🔍 智能客户采集
- 基于搜狗搜索引擎的自动化爬虫
- 覆盖 **10 大目标行业**，每个行业 3-6 个子关键词
- 自动提取公司名、电话、邮箱、地址等信息
- 正则匹配手机号、座机、400 电话
- 评分过滤机制（≥3 分才保留），过滤无效结果

</td>
<td width="50%">

### 🛡️ 反爬与稳定性
- User-Agent 自动轮换（`fake-useragent`）
- 随机请求延迟（2-5 秒）
- 验证码 / 反爬页面自动检测
- 同行公司智能过滤（排除干燥剂供应商）
- 异常重试与优雅降级

</td>
</tr>
<tr>
<td>

### 📊 数据管理与导出
- JSON 文件持久化存储
- 按公司名智能去重（自动合并多源信息）
- 格式化 Excel 导出（蓝色表头、自动筛选、冻结首行）
- 终端表格可视化展示（前 50 条 + 行业分布统计）
- 支持增量采集，数据不丢失

</td>
<td>

### 📧 邮件营销系统
- 根据客户行业生成 **个性化 HTML 邮件**
- 渐变色邮件头部 + CTA 按钮
- 行业定制销售话术自动嵌入
- 支持预览模式（dry_run），发送前可检查
- 批量发送，每封间隔 3 秒避免触发限制

</td>
</tr>
<tr>
<td colspan="2">

### 📈 行业需求分析
- 内置 10 大行业的干燥剂需求深度分析
- 每个行业包含：需求等级、应用场景、推荐产品、采购特点、销售切入话术
- 帮助销售人员快速了解行业痛点，精准沟通

</td>
</tr>
</table>

---

## 🏗️ 项目结构

```
tradingpartner/
│
├── main.py                 # 主入口 — CLI 交互菜单（7 大功能）
├── config.py               # 全局配置 — 关键词、行业、邮件、请求参数
├── models.py               # 数据模型 — Lead 潜在客户类（12 字段）
├── scraper.py              # 采集引擎 — 搜狗搜索爬虫 + 信息提取
├── data_manager.py         # 数据管理 — 存储、去重、导出、展示
├── email_sender.py         # 邮件营销 — 模板生成 + 批量发送
├── industry_analyzer.py    # 行业分析 — 10 大行业需求分析知识库
├── requirements.txt        # Python 依赖清单
│
├── data/
│   └── leads.json          # 已采集的客户线索数据
│
└── output/
    └── 潜在客户名单.xlsx    # 导出的 Excel 客户名单
```

### 模块依赖关系

```
                    ┌─────────────┐
                    │   main.py   │  CLI 入口
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   ┌─────────────┐ ┌─────────────┐ ┌──────────────┐
   │ scraper.py  │ │data_manager │ │ email_sender │
   │  搜索采集   │ │  数据管理   │ │  邮件营销    │
   └──────┬──────┘ └──────┬──────┘ └──────┬───────┘
          │                │                │
          ▼                ▼                ▼
   ┌─────────────┐ ┌─────────────┐ ┌──────────────┐
   │ config.py   │ │ models.py   │ │  industry_   │
   │  全局配置   │ │  数据模型   │ │ analyzer.py  │
   └─────────────┘ └─────────────┘ └──────────────┘
```

---

## 🚀 快速开始

### 环境要求

- **Python** 3.10 或更高版本
- **pip** 包管理器
- 网络连接（用于搜索引擎采集）

### 安装步骤

**1. 克隆项目**

```bash
git clone https://github.com/guangxiangdebizi/tradingpartner.git
cd tradingpartner
```

**2. 创建虚拟环境（推荐）**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. 安装依赖**

```bash
pip install -r requirements.txt
```

**4. 配置邮件（可选，仅邮件功能需要）**

编辑 `config.py` 中的 `EMAIL_CONFIG` 部分：

```python
EMAIL_CONFIG = {
    "smtp_server": "smtp.qq.com",
    "smtp_port": 465,
    "username": "你的QQ邮箱@qq.com",
    "password": "你的SMTP授权码",       # 非QQ密码，需在QQ邮箱设置中获取
    "from_name": "你的公司名称",
}
```

**5. 启动程序**

```bash
python main.py
```

---

## 📋 使用指南

启动后将看到交互式菜单：

```
╭──────────────────────────────────────╮
│   干燥剂行业 · 潜在客户获取与管理系统   │
╰──────────────────────────────────────╯

  [1] 📈 查看行业分析报告
  [2] 🔍 按行业获取潜在客户
  [3] 🔎 按关键词获取潜在客户
  [4] 📋 查看已获取的客户数据
  [5] 📊 导出客户名单到 Excel
  [6] 👀 预览营销邮件
  [7] 📧 发送营销邮件
  [0] 🚪 退出
```

### 典型使用流程

| 步骤 | 操作 | 说明 |
|:----:|------|------|
| 1 | 选择 `[1]` 查看行业分析 | 了解各行业对干燥剂的需求程度和切入策略 |
| 2 | 选择 `[2]` 按行业采集 | 选择目标行业，系统自动搜索并提取客户信息 |
| 3 | 选择 `[4]` 查看数据 | 在终端中预览已采集的客户列表和行业分布 |
| 4 | 选择 `[5]` 导出 Excel | 生成格式化的客户名单，方便线下跟进 |
| 5 | 选择 `[6]` 预览邮件 | 检查将要发送的邮件内容和格式 |
| 6 | 选择 `[7]` 发送邮件 | 向有邮箱的客户批量发送个性化营销邮件 |

### 功能详解

<details>
<summary><b>🔍 按行业采集客户</b></summary>

系统会展示 10 大目标行业供选择，选定后自动执行：
1. 组合行业子关键词 + 后缀（联系方式/电话/公司/企业）
2. 通过搜狗搜索引擎逐页采集
3. 正则提取公司名、电话、邮箱、地址
4. 评分过滤（≥3 分保留）+ 同行排除
5. 自动去重后保存到 `data/leads.json`

</details>

<details>
<summary><b>📊 Excel 导出格式</b></summary>

导出的 Excel 文件包含以下特性：
- 微软雅黑字体，专业排版
- 蓝色渐变表头，白色交替行
- 自动列宽调整
- 首行冻结，方便滚动查看
- 自动筛选功能，可按行业/状态过滤
- 输出路径：`output/潜在客户名单.xlsx`

</details>

<details>
<summary><b>📧 邮件营销</b></summary>

邮件系统特性：
- 根据客户所属行业自动选择对应的销售话术
- 生成包含渐变色头部和 CTA 按钮的 HTML 邮件
- 邮件主题自动包含行业名称 + "免费样品试用"
- 支持 `dry_run` 预览模式，不实际发送
- 批量发送时每封间隔 3 秒，避免被判定为垃圾邮件

</details>

---

## 🏭 覆盖行业

系统内置 10 大干燥剂需求行业的深度分析：

| 行业 | 需求等级 | 典型应用场景 | 搜索子关键词 |
|------|:--------:|-------------|-------------|
| **食品加工** | ⭐⭐⭐⭐⭐ | 零食/茶叶/保健品/奶粉防潮 | 食品厂、零食生产、茶叶公司、坚果加工 |
| **医药制造** | ⭐⭐⭐⭐⭐ | 药品/医疗器械包装防潮 | 药厂、医药公司、制药企业、医疗器械 |
| **电子产品** | ⭐⭐⭐⭐ | 芯片/PCB/LED 防静电防潮 | 电子厂、半导体、芯片封装、PCB生产 |
| **皮革鞋业** | ⭐⭐⭐⭐ | 皮具/鞋类仓储防霉 | 皮革厂、鞋厂、箱包厂、皮具公司 |
| **仓储物流** | ⭐⭐⭐⭐ | 集装箱/仓库防潮除湿 | 仓储公司、物流中心、集装箱运输 |
| **光学仪器** | ⭐⭐⭐⭐ | 精密仪器/镜头防雾防潮 | 光学仪器、精密仪器、镜头生产 |
| **服装纺织** | ⭐⭐⭐ | 布料/成衣仓储防霉 | 服装厂、纺织厂、布料仓储 |
| **汽车零部件** | ⭐⭐⭐ | 金属件/电子件防锈防潮 | 汽车零部件、汽车配件厂 |
| **家具木材** | ⭐⭐⭐ | 木材/板材防潮防变形 | 家具厂、木材加工、板材厂 |
| **金属加工** | ⭐⭐⭐ | 五金/模具/钢材防锈 | 五金厂、模具厂、钢材仓储 |

---

## 📦 数据模型

每条客户线索（`Lead`）包含以下字段：

```python
@dataclass
class Lead:
    company_name: str       # 公司名称（主键）
    industry: str           # 所属行业
    contact_person: str     # 联系人
    phone: str              # 电话（手机/座机/400）
    email: str              # 邮箱
    address: str            # 地址
    source: str             # 数据来源（如 "搜狗-食品厂"）
    website: str            # 官网链接
    business_scope: str     # 经营范围
    status: str             # 跟进状态（默认 "未联系"）
    notes: str              # 备注（含匹配分和搜索词）
    created_at: str         # 采集时间
```

数据以 JSON 格式存储在 `data/leads.json`，支持增量追加和智能去重。

---

## ⚙️ 配置说明

所有配置集中在 `config.py` 中，主要配置项：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `SEARCH_KEYWORDS` | 干燥剂相关搜索关键词 | 12 个关键词 |
| `TARGET_INDUSTRIES` | 目标行业及子关键词 | 10 大行业 |
| `EXCLUDED_COMPANY_KEYWORDS` | 同行过滤关键词 | 干燥剂、硅胶、除湿剂等 |
| `REQUEST_TIMEOUT` | 请求超时时间 | 15 秒 |
| `REQUEST_DELAY` | 请求间隔范围 | 2-5 秒随机 |
| `MAX_PAGES` | 最大翻页数 | 5 页 |
| `EMAIL_CONFIG` | SMTP 邮件配置 | QQ 邮箱（需填写授权码） |
| `DATA_DIR` | 数据存储目录 | `data/` |
| `OUTPUT_DIR` | Excel 导出目录 | `output/` |

> **注意**：邮件功能需要先在 QQ 邮箱中开启 SMTP 服务并获取授权码。

---

## 🛠️ 技术栈

| 类别 | 技术 | 用途 |
|------|------|------|
| 语言 | Python 3.10+ | 主语言 |
| 网页采集 | `requests` + `BeautifulSoup4` + `lxml` | 搜索引擎爬虫 |
| UA 伪装 | `fake-useragent` | 反爬策略 |
| 数据处理 | `pandas` + `openpyxl` | Excel 导出 |
| 终端 UI | `rich` | 美化表格、进度条、面板 |
| 邮件发送 | `smtplib` + `email`（标准库） | SMTP 邮件 |
| 数据存储 | JSON 文件 | 轻量持久化 |

---

## 🗺️ 路线图

- [x] 搜狗搜索引擎客户采集
- [x] 10 大行业需求分析知识库
- [x] 智能去重与评分过滤
- [x] 格式化 Excel 导出
- [x] 个性化 HTML 邮件营销
- [ ] 百度搜索引擎支持
- [ ] 企查查 / 天眼查 API 集成
- [ ] 客户跟进状态管理（CRM 功能）
- [ ] Web 界面（Flask/Streamlit）
- [ ] 定时自动采集（调度任务）
- [ ] 微信/钉钉消息推送通知

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源许可。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 提交 Pull Request

---

## ⚠️ 免责声明

- 本工具仅供学习和合法商业用途，请遵守相关法律法规
- 使用爬虫功能时请遵守目标网站的 `robots.txt` 协议
- 发送营销邮件时请确保符合《反垃圾邮件法》等相关规定
- 请勿用于非法数据采集或骚扰性营销

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐ Star 支持一下！**

Made with ❤️ for the desiccant industry

</div>
