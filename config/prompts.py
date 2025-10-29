# 评价提示词配置

# 基础评价提示词
BASIC_EVALUATION_PROMPT = """你是一位经验丰富的C++编程教师。请对以下学生的C++作业代码进行专业评价。

评价要求：
1. 代码正确性：检查代码逻辑是否正确，是否能完成题目要求
2. 代码规范：检查命名规范、代码格式、注释质量
3. 代码效率：分析时间复杂度和空间复杂度
4. 编程习惯：评估代码可读性、是否使用了良好的编程实践
5. 常见错误：指出内存泄漏、数组越界等潜在问题

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
