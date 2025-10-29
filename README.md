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

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

复制 `.env.example` 为 `.env` 并配置：

```bash
cp .env.example .env
```

**推荐配置（DeepSeek Reasoner）：**

```bash
# DeepSeek Reasoner 配置（推荐）
API_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here
DEEPSEEK_MODEL=deepseek-reasoner

# 其他选项
# DEEPSEEK_MODEL=deepseek-chat  # 标准聊天模型
```

### 3. 运行评价

```bash
python3 src/main.py data/第02周上机作业.zip --week 02
```

### 4. 查看结果

评价完成后会生成：

```
output/
├── 第02周_PDF/                    # 每个学生的PDF报告
│   ├── 学号_姓名_评价报告.pdf
│   └── ...
├── 第02周_评价汇总_时间戳.xlsx     # Excel汇总表格
└── 第02周_评价结果_时间戳.json     # JSON原始数据
```

## 📋 使用说明

### 基本命令

```bash
python3 src/main.py <ZIP文件路径> [选项]
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
python3 src/main.py data/第02周上机作业.zip --week 02

# 使用DeepSeek Chat模型
python3 src/main.py data/第02周上机作业.zip --provider deepseek

# 生成PDF和Excel
python3 src/main.py data/第02周上机作业.zip --week 02 --excel

# 只生成JSON，不生成PDF
python3 src/main.py data/第02周上机作业.zip --week 02 --no-pdf
```

## 🔧 支持的大模型

### DeepSeek（推荐）

```bash
API_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_key
DEEPSEEK_MODEL=deepseek-reasoner  # 推理模型（推荐）
# DEEPSEEK_MODEL=deepseek-chat    # 聊天模型
```

**DeepSeek Reasoner 特点：**
- 🧠 **深度推理**：在推理过程中进行详细思考，评价更全面
- 📊 **结构化输出**：自动按照要求的格式输出评价结果
- 🎯 **精准分析**：能够准确识别代码问题并给出改进建议
- 💡 **教学导向**：评价风格更适合教学场景

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
DASHSCOPE_API_KEY=your_key
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

## 📝 更新日志

### v1.4.0 (当前版本)
- ✅ 支持DeepSeek Reasoner模型
- ✅ 改进批量评价解析逻辑
- ✅ 增强PDF内容显示
- ✅ 添加详细调试信息
- ✅ 优化错误处理和容错机制

### v1.3.1
- ✅ 实时PDF生成
- ✅ 批量评价模式
- ✅ 智能内容解析

## 📞 技术支持

如遇问题，请查看：
1. 控制台的详细调试输出
2. `TROUBLESHOOTING.md` 故障排除指南
3. `QUICK_REFERENCE.md` 快速参考

## 📄 许可证

MIT License