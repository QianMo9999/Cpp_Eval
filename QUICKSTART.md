# C++作业自动评价系统 - 快速开始指南

## 5分钟快速上手

### 第一步：安装Python依赖

```bash
cd cpp_homework_evaluator
pip install -r requirements.txt
```

### 第二步：配置API密钥

```bash
# 复制配置模板
cp .env.example .env

# 编辑.env文件，填入你的API密钥
# 如果使用OpenAI:
API_PROVIDER=openai
OPENAI_API_KEY=你的API密钥
```

### 第三步：准备作业文件

将作业ZIP文件放入 `data/` 目录：

```
data/
└── 第02周上机作业.zip
```

### 第四步：运行评价

**方式1：使用快速启动脚本（推荐）**

```bash
# Linux/Mac
./run.sh

# Windows
run.bat
```

**方式2：使用命令行**

```bash
python src/main.py data/第02周上机作业.zip --week 02
```

### 第五步：查看结果

打开 `output/` 目录查看评价报告：

```
output/
├── 第02周/
│   ├── 张三_评价报告.md
│   ├── 李四_评价报告.md
│   └── ...
├── 第02周_评价汇总_20240101_120000.xlsx
└── 第02周_评价结果_20240101_120000.json
```

## 主要功能

### 1. 自动解压和扫描

系统自动解压ZIP文件并识别所有C++代码文件（.cpp, .h, .cc等）。

### 2. 智能姓名识别

支持多种文件组织方式：
- `第02周作业/张三/code.cpp` → 识别为"张三"
- `第02周作业/张三_code.cpp` → 识别为"张三"
- `第02周作业/2024001_张三.cpp` → 识别为"张三"

### 3. 大模型评价

调用大模型API对代码进行专业评价，包括：
- 代码正确性
- 代码规范
- 代码效率
- 改进建议
- 参考代码

### 4. 多格式输出

- **Markdown报告**：每个学生一份详细报告
- **Excel汇总**：所有学生评价结果汇总表
- **JSON数据**：原始数据，便于二次处理

## 自定义评价标准

编辑 `config/prompts.py` 可以自定义评价标准：

```python
WEEK_SPECIFIC_PROMPTS = {
    "02": """第02周评价重点：
- 基本语法
- 输入输出
- 条件语句
...""",

    "03": """第03周评价重点：
- 循环语句
- 数组使用
...""",
}
```

## 支持的API提供商

- ✅ OpenAI (GPT-4, GPT-3.5)
- ✅ Anthropic Claude
- ✅ 阿里云通义千问
- 🔧 可扩展其他API

## 常见问题

**Q: API调用费用是多少？**
A: 取决于使用的模型和代码量。建议先用少量数据测试，GPT-3.5成本较低。

**Q: 可以离线使用吗？**
A: 需要联网调用API，但可以配置本地部署的大模型（需自行实现API接口）。

**Q: 支持哪些编程语言？**
A: 目前针对C++优化，但修改提示词后可用于其他语言。

**Q: 评价结果准确吗？**
A: AI评价仅供参考，建议教师进行人工复核。

## 项目结构

```
cpp_homework_evaluator/
├── src/              # 核心代码
│   ├── main.py           # 主程序
│   ├── extractor.py      # ZIP解压和扫描
│   ├── llm_evaluator.py  # API调用
│   └── result_saver.py   # 结果保存
├── config/           # 配置文件
│   └── prompts.py        # 评价提示词
├── data/             # 输入数据（ZIP文件）
├── output/           # 输出结果
├── .env              # API密钥配置
├── requirements.txt  # Python依赖
└── README.md         # 详细文档
```

## 技术支持

- 详细文档：查看 `README.md`
- 测试模块：运行 `python src/模块名.py`
- 问题反馈：检查日志输出和错误信息

## 下一步

1. ✅ 测试基本功能
2. ✅ 自定义评价标准
3. ✅ 处理真实作业数据
4. ✅ 根据需求调整输出格式

---

祝使用愉快！如有问题，请查阅完整README.md文档。
