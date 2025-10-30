# C++作业自动评价系统

基于大模型API的C++作业自动评价系统，帮助教师高效批改学生作业，提供详细的代码评价和改进建议。

## 🌟 功能特点

- ✅ **智能批量评价**：每个学生只调用一次API，一次性评价所有题目，速度更快
- ✅ **实时PDF生成**：评价完一个学生立即生成PDF报告，无需等待
- ✅ **多格式输出**：支持PDF报告、Excel汇总、JSON数据等多种格式
- ✅ **自动解压ZIP**：智能识别学生姓名和代码文件
- ✅ **多模型支持**：支持DeepSeek、OpenAI、Claude、通义千问等多个大模型
- ✅ **自定义评价**：可针对不同周次定制评价标准和提示词
- ✅ **详细调试信息**：提供完整的评价过程日志，便于问题排查
- 🆕 **DeepSeek Reasoner**：支持最新的推理模型，评价质量更高
- 🆕 **智能容错处理**：自动处理API响应异常，确保评价完整性

## 🚀 推荐配置

**推荐使用 DeepSeek Reasoner 模型**：
- 💰 **性价比最高**：比GPT-4便宜10-20倍
- 🧠 **推理能力强**：专门优化的推理模型，评价更深入
- 🚀 **代码专精**：在代码理解和评价方面表现优秀
- 🇨🇳 **国内稳定**：无需特殊网络环境，响应速度快

## 📁 项目结构

```
cpp_homework_evaluator/
├── src/                      # 源代码目录
│   ├── main.py              # 主程序入口（支持批量评价）
│   ├── extractor.py         # ZIP解压和文件扫描模块
│   ├── llm_evaluator.py     # 大模型API调用模块（支持DeepSeek Reasoner）
│   └── result_saver.py      # 结果保存模块（支持实时PDF生成）
├── config/                   # 配置目录
│   └── prompts.py           # 评价提示词配置（支持批量评价模板）
├── data/                     # 数据目录（存放ZIP文件）
├── output/                   # 输出目录
│   ├── 第XX周_PDF/          # PDF报告目录
│   ├── 第XX周/              # Markdown报告目录
│   └── *.xlsx              # Excel汇总文件
├── requirements.txt         # Python依赖
├── .env.example            # 环境变量示例
└── README.md               # 使用说明
```

## ⚡ 快速开始

### 1. 系统依赖安装

**macOS用户**：
```bash
# 如果没有安装Homebrew，请先安装
/bin/bash -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"

# 安装系统依赖（PDF生成必需）
brew install pango gdk-pixbuf libffi
```

**Ubuntu/Debian用户**：
```bash
sudo apt-get update
sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

**Windows用户**：
建议使用WSL或Docker环境，或者使用预编译的WeasyPrint包。

### 2. Python依赖安装

```bash
pip install -r requirements.txt
```

### 3. 配置API密钥

复制 `.env.example` 为 `.env` 并配置：

```bash
cp .env.example .env
```

**推荐配置（DeepSeek Reasoner）：**

```bash
# DeepSeek Reasoner 配置（推荐）
API_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here
DEEPSEEK_MODEL=deepseek-chat

# 其他选项
# DEEPSEEK_MODEL=deepseek-chat  # 标准聊天模型
```

### 3.添加作业数据

将作业.zip复制到 `/Cpp_Eval/data/` 下

### 4. 运行评价

```bash
python src/main.py data/第02周上机作业.zip --week 02
```

### 5. 查看结果

评价完成后会生成：

```
output/
├── 第02周_PDF/                    # 每个学生的PDF报告
│   ├── 学号_姓名_评价报告.pdf
│   └── ...
├── 第02周_评价汇总_时间戳.xlsx     # Excel汇总表格
└── 第02周_评价结果_时间戳.json     # JSON原始数据
```

### 6.故障处理指南

查看 `TROUBLESHOOTING.md` 故障处理指南

## 📋 使用说明

### 基本命令

```bash
python src/main.py <ZIP文件路径> [选项]
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `zip_path` | 作业ZIP文件路径（必需） | - |
| `--week` | 作业周次 | 02 |
| `--provider` | API提供商 | 从.env读取 |
| `--output` | 输出目录 | ./output |
| `--no-pdf` | 不生成PDF报告 | - |
| `--excel` | 同时生成Excel汇总 | - |
| `--no-json` | 不保存JSON结果 | - |

### 使用示例

```bash
# 基本使用（推荐）
python src/main.py data/第02周上机作业.zip --week 02

# 使用DeepSeek Chat模型
python src/main.py data/第02周上机作业.zip --provider deepseek

# 生成PDF和Excel
python src/main.py data/第02周上机作业.zip --week 02 --excel

# 只生成JSON，不生成PDF
python src/main.py data/第02周上机作业.zip --week 02 --no-pdf
```

## 🔧 支持的大模型

### DeepSeek（推荐）

```bash
API_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_key
DEEPSEEK_MODEL=deepseek-chat  # 推理模型（推荐）
# DEEPSEEK_MODEL=deepseek-reasoner    # 聊天模型
```

### OpenAI GPT系列

```bash
API_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4-turbo-preview
```

### Anthropic Claude系列

```bash
API_PROVIDER=claude
ANTHROPIC_API_KEY=your_key
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### 通义千问

```bash
API_PROVIDER=dashscope
QWEN_API_KEY=your_key
QWEN_MODEL=qwen3-coder-plus
```

## 🎯 系统特性

### 批量评价模式

- **高效处理**：每个学生只调用一次API，一次性评价所有题目
- **智能解析**：自动分割批量评价结果，提取每道题的评价内容
- **多重容错**：支持多种分隔符格式，确保评价内容完整

### 实时PDF生成

- **即时反馈**：评价完一个学生立即生成PDF，无需等待所有人完成
- **中断友好**：如果中途中断，已评价的学生PDF已经生成
- **美观格式**：支持中文字体、Markdown格式转换、表格布局

### 智能调试

- **详细日志**：显示API调用状态、内容长度、解析过程
- **错误诊断**：自动检测并报告常见问题
- **内容预览**：显示评价内容预览，便于验证结果

## 🛠️ 自定义配置

### Token长度限制

可以在 `src/llm_evaluator.py` 中调整：

```python
max_tokens=50000  # 当前设置，可根据需要调整
```

### 评价提示词

编辑 `config/prompts.py` 中的批量评价模板：

```python
WEEK_BATCH_PROMPTS = {
    "02": """第02周批量评价模板...""",
    "03": """第03周批量评价模板...""",
}
```

## 📊 输出格式

### PDF报告内容

每个学生的PDF报告包含：
- 学生基本信息（姓名、学号、周次）
- 题目总数和总评分
- 每道题的详细评价（优点、需要改进、建议、分数）
- 格式化的Markdown内容显示

### Excel汇总表格

包含所有学生的评价汇总：
- 学生信息、文件名、评分、状态
- 评价时间、详细评价内容
- 支持筛选和排序

## 🔍 故障排除

### 常见问题

1. **评价内容为空**
   - 检查API密钥是否正确
   - 确认模型名称是否支持
   - 查看调试日志中的错误信息

2. **PDF生成失败**
   - 确保安装了reportlab库
   - 检查系统是否支持中文字体
   - 查看PDF生成过程的错误日志

3. **批量评价解析失败**
   - 查看"AI返回内容预览"确认API响应
   - 检查评价内容是否使用了正确的分隔符
   - 尝试调整max_tokens设置

### 调试信息

运行时会显示详细的调试信息：
```
[1/78] 评价学生: 学号 姓名 (8道题)
   正在评价 8 道题...
正在调用DeepSeek API (deepseek-reasoner)...
   API响应状态: 成功
   返回内容长度: 2543 字符
   使用推理内容作为评价结果
   ✓ 成功解析 8 道题的评价
   题目1: 分数=85, 评价预览='...'
   正在生成PDF报告...
✓ PDF报告已生成
```

# 更新日志

## v2.0.0 (当前版本) - DeepSeek Reasoner & 批量评价优化

### 🚀 重大功能更新
- **DeepSeek Reasoner支持**：新增对DeepSeek推理模型的完整支持
  - 自动处理推理内容（reasoning_content）
  - 智能提取评价结果，避免内容截断
  - 支持更高的token限制（8000 tokens）
  - 推理质量显著提升

### 🔧 批量评价系统优化
- **智能解析引擎**：全面重构批量评价解析逻辑
  - 支持多种分隔符格式（===、### 题目N:、题目标题模式）
  - 智能段落重组，确保评价内容完整
  - 自动容错处理，避免解析失败
  - 详细的解析过程日志

### 📄 PDF生成系统增强
- **实时PDF生成**：评价完一个学生立即生成PDF报告
- **内容完整性保障**：移除错误的长度判断逻辑
- **格式优化**：支持Markdown格式转换、中文字体、表格布局
- **错误容错**：解析失败时自动降级为纯文本显示

### 🔍 调试和监控系统
- **详细调试信息**：
  - API响应状态和内容长度显示
  - 评价内容预览和分割过程日志
  - 每道题的解析结果预览
  - 推理内容长度统计
- **智能错误诊断**：自动检测并报告常见问题
- **实时进度反馈**：显示评价进度和PDF生成状态

### 🛠️ 技术改进
- **API调用优化**：
  - 增加max_tokens到8000，支持更长评价
  - 改进DeepSeek API响应处理逻辑
  - 支持reasoning_content字段提取
- **容错机制增强**：
  - 多重分割策略，确保内容解析成功
  - 默认评价内容生成，避免空白结果
  - 智能分数推断和默认值设置

### 📝 文档更新
- **README.md**：全面更新，添加最新功能说明
- **requirements.txt**：添加dashscope依赖
- **调试指南**：新增详细的故障排除说明

### 🐛 问题修复
- ✅ 修复DeepSeek Reasoner模型返回内容为空的问题
- ✅ 修复批量评价解析失败导致的评价内容不完整
- ✅ 修复PDF生成时"评价内容较短"的错误提示
- ✅ 修复分数提取不准确的问题
- ✅ 修复特殊字符在PDF中显示异常的问题

---

## v1.3.1 - 实时PDF生成

### 🆕 新增功能
- **实时PDF生成**：评价完一个学生立即生成PDF，无需等待所有人评价完成
- **批量评价模式**：每个学生只调用一次API，一次性评价所有题目
- **智能内容解析**：自动分割批量评价结果，提取每道题的评价内容

### 📊 性能优化
- 提升评价效率：减少API调用次数
- 改进用户体验：实时反馈，中断友好
- 优化内存使用：流式处理，避免内存积累

---

## v1.2.0 - 多格式输出支持

### 🆕 新增功能
- **PDF报告生成**：为每个学生生成精美的PDF评价报告
- **Excel汇总表格**：支持生成包含所有学生评价的Excel文件
- **JSON数据导出**：便于后续数据处理和分析

### 🎨 界面优化
- PDF报告支持中文字体和表格布局
- Excel表格包含详细的评价信息和统计数据
- 改进命令行输出格式和进度显示

---

## v1.1.0 - 新增DeepSeek支持

### 🆕 新增功能
- **DeepSeek API支持**：新增对DeepSeek大模型的支持
  - 性价比极高（比GPT-4便宜10-20倍）
  - 代码能力强，特别适合C++作业评价
  - 国内访问稳定，无需特殊网络环境
  - 响应速度快

### 📝 文档更新
- 新增 `DEEPSEEK_GUIDE.md`：DeepSeek API详细配置指南
- 更新 `README.md`：添加DeepSeek使用说明
- 更新 `QUICKSTART.md`：推荐使用DeepSeek
- 更新 `.env.example`：添加DeepSeek配置示例

### 🔧 代码优化
- `src/llm_evaluator.py`：添加 `DeepSeekEvaluator` 类
- `src/main.py`：命令行参数支持deepseek选项
- 新增 `test_api.py`：API配置测试工具

### 📊 支持的API提供商
- ✅ DeepSeek（推荐）
- ✅ OpenAI (GPT-4, GPT-3.5)
- ✅ Anthropic Claude
- ✅ 阿里云通义千问

### 🎯 最佳实践建议
- 首选DeepSeek Reasoner：推理能力强，评价质量高
- DeepSeek Chat：适合预算有限、批量处理的场景
- GPT-4：追求最佳质量但成本较高
- Claude：长文本处理优势

---

## v1.0.0 - 首次发布

### ✨ 核心功能
- ZIP文件自动解压和扫描
- 智能识别学生姓名
- 支持多种C++文件格式（.cpp, .cc, .h等）
- 大模型API集成（OpenAI、Claude、通义千问）
- 自定义评价提示词
- 生成Markdown格式的评价报告
- 导出Excel汇总表格
- JSON格式数据导出

### 📦 项目结构
- 模块化设计，易于维护和扩展
- 完整的配置文件系统
- 详细的使用文档

### 🛠️ 开发工具
- 快速启动脚本（run.sh / run.bat）
- 环境变量配置（.env）
- Git忽略文件配置

### 📚 文档
- README.md：完整使用文档
- QUICKSTART.md：快速开始指南
- data/README.md：数据文件组织说明

---

### 欢迎贡献
如果你有好的想法或发现了bug，欢迎提Issue或Pull Request！

---

## 📞 技术支持

- 🐛 **问题反馈**：请在GitHub Issues中报告
- 📖 **使用文档**：查看README.md和相关文档
- 🔧 **故障排除**：参考TROUBLESHOOTING.md
- 💡 **功能建议**：欢迎在Issues中提出



