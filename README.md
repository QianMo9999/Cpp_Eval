# C++作业自动评价系统

基于大模型API的C++作业自动评价系统，帮助教师高效批改学生作业，提供详细的代码评价和改进建议。

## 功能特点

- ✅ 自动解压ZIP格式的作业文件
- ✅ 智能识别学生姓名和代码文件
- ✅ 支持多个大模型API（DeepSeek、OpenAI、Claude、通义千问等）
- ✅ 可自定义评价提示词，针对不同周次定制评价标准
- ✅ 自动生成详细的评价报告（Markdown/文本格式）
- ✅ 生成Excel汇总表格，方便统计和管理
- ✅ 支持批量处理多个学生的作业
- 🆕 推荐使用DeepSeek API（性价比最高，代码能力强）

## 项目结构

```
cpp_homework_evaluator/
├── src/                      # 源代码目录
│   ├── main.py              # 主程序入口
│   ├── extractor.py         # ZIP解压和文件扫描模块
│   ├── llm_evaluator.py     # 大模型API调用模块
│   └── result_saver.py      # 结果保存模块
├── config/                   # 配置目录
│   └── prompts.py           # 评价提示词配置
├── data/                     # 数据目录（存放ZIP文件）
├── output/                   # 输出目录（评价报告）
├── requirements.txt         # Python依赖
├── .env.example            # 环境变量示例
└── README.md               # 使用说明
```

## 快速开始

### 1. 安装依赖

```bash
cd cpp_homework_evaluator
pip install -r requirements.txt
```

### 2. 配置API密钥

复制 `.env.example` 为 `.env` 并填入你的API密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```bash
# 选择使用的API提供商（三选一）

# 方案1: 使用OpenAI
API_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# 方案2: 使用Claude
# API_PROVIDER=claude
# ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here
# ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# 方案3: 使用通义千问
# API_PROVIDER=dashscope
# DASHSCOPE_API_KEY=sk-your-dashscope-api-key-here
```

### 3. 准备作业文件

将学生提交的作业ZIP文件放入 `data` 目录，ZIP文件解压后的结构应类似：

```
第02周上机作业/
├── 张三/
│   └── homework.cpp
├── 李四/
│   └── code.cpp
└── 王五/
    └── main.cpp
```

或者：

```
第02周上机作业/
├── 张三_homework.cpp
├── 李四_code.cpp
└── 王五_main.cpp
```

### 4. 运行评价

```bash
python src/main.py data/第02周上机作业.zip --week 02
```

### 5. 查看结果

评价完成后，在 `output` 目录下会生成：

- `第02周/` - 每个学生的详细评价报告（Markdown格式）
- `第02周_评价汇总_[时间戳].xlsx` - Excel汇总表格
- `第02周_评价结果_[时间戳].json` - JSON格式的原始数据

## 使用说明

### 基本用法

```bash
python src/main.py <ZIP文件路径> [选项]
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `zip_path` | 作业ZIP文件路径（必需） | - |
| `--week` | 作业周次 | 02 |
| `--provider` | API提供商 (openai/claude/dashscope/deepseek) | 从.env读取 |
| `--output` | 输出目录 | ./output |
| `--no-individual` | 不保存单个学生报告 | - |
| `--no-excel` | 不保存Excel汇总 | - |
| `--no-json` | 不保存JSON结果 | - |

### 使用示例

```bash
# 基本使用
python src/main.py data/第02周上机作业.zip

# 指定周次
python src/main.py data/第03周上机作业.zip --week 03

# 使用DeepSeek API（推荐：性价比高）
python src/main.py data/第02周上机作业.zip --provider deepseek

# 使用Claude API
python src/main.py data/第02周上机作业.zip --provider claude

# 只生成Excel汇总，不保存单个报告
python src/main.py data/第02周上机作业.zip --no-individual

# 自定义输出目录
python src/main.py data/第02周上机作业.zip --output ./my_output
```

## 自定义评价标准

### 修改评价提示词

编辑 `config/prompts.py` 文件，可以：

1. 修改 `BASIC_EVALUATION_PROMPT` - 通用评价模板
2. 在 `WEEK_SPECIFIC_PROMPTS` 中添加特定周次的评价标准

示例：

```python
WEEK_SPECIFIC_PROMPTS = {
    "02": """第02周评价标准...""",
    "03": """你是一位经验丰富的C++编程教师。本周作业主要考察：
- 循环语句（for, while）
- 数组的使用
- 函数定义和调用

学生姓名：{student_name}
代码文件：{filename}

代码内容：
```cpp
{code}
```

请根据以上知识点进行详细评价。
""",
}
```

## 支持的大模型

### OpenAI GPT系列

```bash
API_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4-turbo-preview  # 或 gpt-3.5-turbo
```

### Anthropic Claude系列

```bash
API_PROVIDER=claude
ANTHROPIC_API_KEY=your_key
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022  # 或其他Claude模型
```

### 通义千问

```bash
API_PROVIDER=dashscope
DASHSCOPE_API_KEY=your_key
```

需要额外安装：
```bash
pip install dashscope
```

### DeepSeek（推荐：性价比高）

DeepSeek是一个性价比极高的国产大模型，特别擅长代码相关任务，非常适合用于C++作业评价。

```bash
API_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_key
DEEPSEEK_MODEL=deepseek-chat
```

**优势：**
- 💰 **价格低廉**：比GPT-4便宜10-20倍
- 🚀 **代码能力强**：在代码理解和生成方面表现优秀
- 🇨🇳 **国内访问稳定**：无需特殊网络环境
- ⚡ **响应速度快**：延迟低，适合批量处理

**获取API密钥：**
访问 [https://platform.deepseek.com/](https://platform.deepseek.com/) 注册账号并获取API密钥。

## 常见问题

### 1. ZIP文件解压失败

- 确保ZIP文件格式正确
- 检查文件路径是否正确
- 确保有足够的磁盘空间

### 2. API调用失败

- 检查API密钥是否正确
- 确认网络连接正常
- 检查API配额是否充足

### 3. 找不到C++文件

- 检查ZIP文件内的目录结构
- 确保文件扩展名是 `.cpp`, `.cc`, `.cxx`, `.c`, `.h`, `.hpp`

### 4. 学生姓名识别错误

系统会自动从文件路径或文件名中提取学生姓名，如果识别错误，可以：
- 调整文件夹结构（推荐：`学生姓名/代码文件.cpp`）
- 或使用文件名格式：`学生姓名_代码文件.cpp`

### 5. 编码问题

系统会自动尝试多种编码（UTF-8, GBK, GB2312），如果仍有问题，请确保代码文件使用UTF-8编码保存。

## 高级功能

### 1. 单独测试各模块

```bash
# 测试ZIP解压和扫描
python src/extractor.py

# 测试大模型API
python src/llm_evaluator.py

# 测试结果保存
python src/result_saver.py
```

### 2. 在Python代码中使用

```python
from src.main import HomeworkEvaluationSystem

# 创建评价系统
system = HomeworkEvaluationSystem(
    zip_path="data/第02周上机作业.zip",
    week="02",
    api_provider="openai"
)

# 运行评价
results = system.run(
    save_individual=True,
    save_excel=True,
    save_json=True
)

# 处理结果
for result in results:
    print(f"{result['student_name']}: {result['score']}/100")
```

## 注意事项

1. **成本控制**：使用商业API会产生费用，建议先用少量数据测试
2. **隐私保护**：学生代码包含个人信息，请妥善保管
3. **结果参考**：AI评价仅供参考，建议教师进行人工复核
4. **并发限制**：避免同时处理过多文件，注意API调用频率限制

## 许可证

MIT License

## 作者

教育辅助工具 - C++作业评价系统

## 更新日志

### v1.0.0 (2024)
- 初始版本发布
- 支持ZIP文件自动解压
- 支持OpenAI、Claude、通义千问API
- 支持生成Markdown报告和Excel汇总
