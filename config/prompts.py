# 评价提示词配置

# 基础评价提示词
BASIC_EVALUATION_PROMPT = """
你是一位经验丰富的C++编程教师。请对以下学生的C++作业代码进行专业评价。

评价要求：
1. 代码规范：检查命名规范、代码格式、注释质量
2. 代码效率：分析时间复杂度和空间复杂度
3. 编程习惯：评估代码可读性、是否使用了良好的编程实践
4. 常见错误：指出内存泄漏、数组越界等潜在问题

学生姓名：{student_name}
作业周次：{week}
代码文件：{filename}

代码内容：
```cpp
{code}
```

请按以下格式输出评价：
## 总体评分
- 分数：_/100

## 优点
-

## 需要改进的地方
-

## 详细建议
-

## 参考代码片段（如有必要）
```cpp
// 改进建议
```
"""

# 针对特定题目的评价提示词（可以根据不同周次定制）
WEEK_SPECIFIC_PROMPTS = {
    "02": """你是一位经验丰富的C++编程教师。本周作业主要考察：
- 基本输入输出
- 变量声明和使用
- 基本运算符
- 条件语句（if-else）

请重点关注以上知识点的掌握情况。

学生姓名：{student_name}
代码文件：{filename}

代码内容：
```cpp
{code}
```

请提供详细评价，包括：
1. 知识点掌握情况（每个知识点单独评价）
2. 代码规范性
3. 具体改进建议
4. 鼓励性评语

评分标准（总分100）：
- 正确性：50分
- 代码规范：20分
- 程序效率：15分
- 代码可读性：15分
""",
    # 可以继续添加其他周次的提示词
}

# 批量评价提示词（一次性评价一个学生的所有题目）
BATCH_EVALUATION_PROMPT = """
你是一位经验丰富的C++编程教师。请对以下学生的所有C++作业代码进行批量评价。

学生信息：
- 姓名：{student_name}
- 学号：{student_id}
- 作业周次：第{week}周
- 题目数量：{num_problems}道

评价要求：
1. 逐题评价，每道题单独给出评价和分数
2. 每道题的评价包括：代码规范、程序效率、代码可读性
3. 每道题给出0-100分的分数
4. 使用 === 分隔不同题目的评价

以下是该学生的所有题目代码：

{all_codes}

请按以下格式输出评价（每道题之间用===分隔）：

### 题目1: [题目名称]
**分数**: XX/100

**优点**:
-

**需要改进**:
-

**详细建议**:
-

===

### 题目2: [题目名称]
**分数**: XX/100

...（依此类推）
"""

# 针对特定周次的批量评价提示词
WEEK_BATCH_PROMPTS = {
    "02": """你是一位经验丰富的C++编程教师。第02周作业主要考察：
- 基本输入输出（cin/cout）
- 变量声明和使用
- 基本运算符
- 条件语句（if-else）

学生信息：
- 姓名：{student_name}
- 学号：{student_id}
- 作业周次：第{week}周
- 题目数量：{num_problems}道

请逐题评价该学生的所有作业代码，重点关注以上知识点的掌握情况。

以下是该学生的所有题目代码：

{all_codes}

评价要求：
1. 逐题评价，每道题单独给出评价和分数
2. 评分标准（每题总分100）：
   - 正确性：50分
   - 代码规范：20分
   - 程序效率：15分
   - 代码可读性：15分
3. 每道题评价包括：优点、需要改进的地方、详细建议
4. **重要**：每道题之间必须用 === 分隔

输出格式示例：

### 题目1: 第1关-求三位数
**分数**: 85/100

**优点**:
- 代码逻辑清晰，正确实现了功能
- 变量命名规范

**需要改进**:
- 缺少必要的注释
- 可以添加输入验证

**详细建议**:
- 建议在关键步骤添加注释，提高代码可读性
- 可以检查输入是否为三位数

===

### 题目2: 第2关-数字加密
**分数**: 90/100

**优点**:
- 算法实现正确
- 代码结构清晰

...（依此类推，每道题之间用===分隔）
""",
    # 可以继续添加其他周次的批量评价提示词
}

def get_prompt(student_name, filename, code, week="02"):
    """
    获取评价提示词

    Args:
        student_name: 学生姓名
        filename: 代码文件名
        code: 代码内容
        week: 周次（如 "02", "03"）

    Returns:
        格式化后的提示词
    """
    if week in WEEK_SPECIFIC_PROMPTS:
        template = WEEK_SPECIFIC_PROMPTS[week]
    else:
        template = BASIC_EVALUATION_PROMPT

    return template.format(
        student_name=student_name,
        week=week,
        filename=filename,
        code=code
    )


def get_batch_prompt(student_name, student_id, all_problems, week="02"):
    """
    获取批量评价提示词（一次评价所有题目）

    Args:
        student_name: 学生姓名
        student_id: 学号
        all_problems: 所有题目列表
            [
                {
                    'problem_name': '第1关-求三位数',
                    'file_name': 'main.cpp',
                    'code': '代码内容...'
                },
                ...
            ]
        week: 周次

    Returns:
        格式化后的提示词
    """
    # 构建所有题目的代码文本
    codes_text = ""
    for idx, problem in enumerate(all_problems, 1):
        problem_name = problem.get('problem_name', f'题目{idx}')
        file_name = problem.get('file_name', 'main.cpp')
        code = problem.get('code', '')

        codes_text += f"""
### 题目{idx}: {problem_name}
文件名: {file_name}

```cpp
{code}
```

"""

    # 选择提示词模板
    if week in WEEK_BATCH_PROMPTS:
        template = WEEK_BATCH_PROMPTS[week]
    else:
        template = BATCH_EVALUATION_PROMPT

    # 格式化提示词
    return template.format(
        student_name=student_name,
        student_id=student_id or '无',
        week=week,
        num_problems=len(all_problems),
        all_codes=codes_text
    )
