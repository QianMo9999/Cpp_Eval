# 故障排除指南

## 常见错误及解决方案

### 1. ModuleNotFoundError: No module named 'dotenv'

**错误信息：**
```
ModuleNotFoundError: No module named 'dotenv'
```

**原因：**
缺少 `python-dotenv` 库

**解决方案：**

**方式1：使用安装脚本**
```bash
# Linux/Mac
./install.sh

# Windows
install.bat
```

**方式2：手动安装**
```bash
pip install python-dotenv
# 或安装所有依赖
pip install -r requirements.txt
```

**方式3：如果pip和python版本不匹配**
```bash
# 使用python3
python3 -m pip install -r requirements.txt

# 或指定pip3
pip3 install -r requirements.txt
```

---

### 2. ModuleNotFoundError: No module named 'config'

**错误信息：**
```
ModuleNotFoundError: No module named 'config'
```

**原因：**
Python路径导入问题

**解决方案：**
确保以下文件存在：
- `config/__init__.py`
- `src/__init__.py`

这些文件已经自动创建，如果缺失，请检查项目完整性。

---

### 3. API密钥相关错误

**错误信息：**
```
ValueError: 请在.env文件中设置DEEPSEEK_API_KEY
```

**解决方案：**

1. **检查.env文件是否存在**
```bash
ls -la .env
```

2. **如果不存在，复制模板文件**
```bash
cp .env.example .env
```

3. **编辑.env文件，填入真实的API密钥**
```bash
# 使用vim或其他编辑器
vim .env
# 或使用nano
nano .env
```

4. **确保API密钥格式正确**
```bash
# DeepSeek密钥格式
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx

# OpenAI密钥格式
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx

# 注意：不要有多余的空格或引号
```

5. **测试API配置**
```bash
python test_api.py
```

---

### 4. 401 Unauthorized / API调用失败

**错误信息：**
```
Exception: DeepSeek API调用失败: 401 Unauthorized
```

**原因：**
- API密钥无效
- API密钥过期
- API密钥被禁用

**解决方案：**

1. **检查API密钥是否正确**
   - 登录API提供商的控制台
   - 确认密钥状态
   - 如有必要，重新生成密钥

2. **检查账户余额**
   - DeepSeek: https://platform.deepseek.com/
   - OpenAI: https://platform.openai.com/account/billing
   - Claude: https://console.anthropic.com/

3. **重新配置API密钥**
```bash
# 编辑.env文件
nano .env
# 更新密钥后测试
python test_api.py
```

---

### 5. ZIP文件解压失败

**错误信息：**
```
Exception: ZIP文件不是有效的ZIP文件
```

**解决方案：**

1. **检查文件格式**
```bash
file data/第02周上机作业.zip
# 应该显示: Zip archive data
```

2. **尝试手动解压测试**
```bash
unzip -t data/第02周上机作业.zip
```

3. **重新下载ZIP文件**
   - 可能下载过程中文件损坏
   - 确保文件完整下载

4. **检查文件权限**
```bash
ls -l data/第02周上机作业.zip
# 确保有读权限
```

---

### 6. 找不到C++文件

**错误信息：**
```
✓ 找到 0 个C++文件
```

**原因：**
ZIP文件中没有C++代码文件

**解决方案：**

1. **检查ZIP文件内容**
```bash
unzip -l data/第02周上机作业.zip
```

2. **确保文件扩展名正确**
   - 支持的扩展名：`.cpp`, `.cc`, `.cxx`, `.c`, `.h`, `.hpp`
   - 检查文件是否使用其他扩展名

3. **检查文件夹结构**
```
正确的结构示例：
第02周上机作业/
├── 张三/
│   └── code.cpp
└── 李四/
    └── main.cpp
```

---

### 7. 编码问题

**错误信息：**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

**原因：**
代码文件使用了非UTF-8编码

**解决方案：**

系统已自动处理多种编码（UTF-8, GBK, GB2312），如果仍有问题：

1. **将代码文件转换为UTF-8编码**
```bash
iconv -f GBK -t UTF-8 原文件.cpp > 新文件.cpp
```

2. **或使用专门工具批量转换**

---

### 8. Excel保存失败

**错误信息：**
```
Exception: 请安装openpyxl库
```

**解决方案：**
```bash
pip install openpyxl
```

---

### 9. python命令找不到

**错误信息：**
```
command not found: python
```

**解决方案：**

**Mac/Linux:**
```bash
# 使用python3
python3 src/main.py data/第02周上机作业.zip --week 02

# 或创建软链接
alias python=python3
```

**Windows:**
```bash
# 通常Windows使用python
python src/main.py data/第02周上机作业.zip --week 02
```

---

### 10. 网络连接问题

**错误信息：**
```
Exception: API调用失败: Connection timeout
```

**解决方案：**

1. **检查网络连接**
```bash
ping api.deepseek.com
```

2. **DeepSeek在国内可直接访问**
   - 无需特殊网络环境
   - 检查防火墙设置

3. **OpenAI和Claude需要特殊网络**
   - 如果使用这些API，需要配置代理

---

## 调试技巧

### 1. 开启详细日志

修改代码添加调试信息：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. 测试单个模块

```bash
# 测试ZIP解压模块
python src/extractor.py

# 测试API调用模块
python src/llm_evaluator.py

# 测试结果保存模块
python src/result_saver.py
```

### 3. 使用交互式测试

```python
# 进入Python交互模式
python3

# 导入模块测试
>>> from src.llm_evaluator import get_evaluator
>>> evaluator = get_evaluator('deepseek')
>>> print(evaluator)
```

---

## 获取帮助

如果以上方法都无法解决问题：

1. **检查官方文档**
   - README.md
   - QUICKSTART.md
   - DEEPSEEK_GUIDE.md

2. **使用API测试工具**
```bash
python test_api.py
```

3. **查看日志输出**
   - 仔细阅读错误信息
   - 检查完整的堆栈跟踪

4. **确认环境配置**
```bash
# Python版本
python --version
# 应该是Python 3.7+

# 已安装的包
pip list | grep -E "openai|anthropic|dotenv|openpyxl"
```

---

## 快速诊断脚本

运行此脚本检查环境配置：

```bash
python3 << 'EOF'
import sys
print(f"Python版本: {sys.version}")
print(f"Python路径: {sys.executable}")

try:
    import dotenv
    print("✓ python-dotenv 已安装")
except:
    print("✗ python-dotenv 未安装")

try:
    import openai
    print("✓ openai 已安装")
except:
    print("✗ openai 未安装")

try:
    import anthropic
    print("✓ anthropic 已安装")
except:
    print("✗ anthropic 未安装")

try:
    import openpyxl
    print("✓ openpyxl 已安装")
except:
    print("✗ openpyxl 未安装")

import os
if os.path.exists('.env'):
    print("✓ .env 文件存在")
else:
    print("✗ .env 文件不存在")
EOF
```

运行此脚本将显示你的环境配置状态。
