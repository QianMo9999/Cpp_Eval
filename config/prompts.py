# 评价提示词配置

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
2. 评分标准（每题总分100）：
   - 正确性：50分
   - 代码规范：20分
   - 程序效率：15分
   - 代码可读性：15分
3. 每道题评价包括：优点、需要改进的地方
4. **重要**：对于需要改进的地方，必须基于学生提交的代码给出具体的改进示范代码
5. **重要**：每道题之间必须用 === 分隔

以下是该学生的所有题目代码：

{all_codes}

请按以下格式输出评价（每道题之间用===分隔）：

### 题目1: [题目名称]
**分数**: XX/100

**优点**:
-

**需要改进**:
-

**改进示范**:
```cpp
// 针对上述问题的改进代码
```

===

### 题目2: [题目名称]
**分数**: XX/100

...（依此类推）
"""

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
    template = BATCH_EVALUATION_PROMPT

    # 格式化提示词
    return template.format(
        student_name=student_name,
        student_id=student_id or '无',
        week=week,
        num_problems=len(all_problems),
        all_codes=codes_text
    )

