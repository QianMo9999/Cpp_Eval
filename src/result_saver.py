"""
评价结果保存模块
支持保存为文本、Markdown和Excel格式
"""
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import json


class ResultSaver:
    """评价结果保存器"""

    def __init__(self, output_dir: str = "./output"):
        """
        初始化保存器

        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def save_individual_report(
        self,
        student_name: str,
        file_name: str,
        evaluation: str,
        week: str = "02",
        format: str = "markdown"
    ) -> str:
        """
        保存单个学生的评价报告

        Args:
            student_name: 学生姓名
            file_name: 代码文件名
            evaluation: 评价内容
            week: 周次
            format: 保存格式 (markdown, txt)

        Returns:
            保存的文件路径
        """
        # 创建周次目录
        week_dir = os.path.join(self.output_dir, f"第{week}周")
        os.makedirs(week_dir, exist_ok=True)

        # 确定文件扩展名
        ext = ".md" if format == "markdown" else ".txt"

        # 生成文件名
        safe_student_name = student_name.replace('/', '_').replace('\\', '_')
        file_path = os.path.join(week_dir, f"{safe_student_name}_评价报告{ext}")

        # 准备内容
        if format == "markdown":
            content = self._format_markdown_report(student_name, file_name, evaluation, week)
        else:
            content = self._format_text_report(student_name, file_name, evaluation, week)

        # 保存文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ 已保存评价报告: {file_path}")
        return file_path

    def _format_markdown_report(
        self,
        student_name: str,
        file_name: str,
        evaluation: str,
        week: str
    ) -> str:
        """格式化Markdown报告"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return f"""# C++作业评价报告

---

**学生姓名**: {student_name}
**作业周次**: 第{week}周
**代码文件**: {file_name}
**评价时间**: {timestamp}

---

{evaluation}

---

*本评价由AI自动生成，仅供参考*
"""

    def _format_text_report(
        self,
        student_name: str,
        file_name: str,
        evaluation: str,
        week: str
    ) -> str:
        """格式化文本报告"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return f"""====================================
C++作业评价报告
====================================

学生姓名: {student_name}
作业周次: 第{week}周
代码文件: {file_name}
评价时间: {timestamp}

------------------------------------

{evaluation}

------------------------------------

*本评价由AI自动生成，仅供参考*
"""

    def save_summary_excel(
        self,
        results: List[Dict],
        week: str = "02",
        filename: str = None
    ) -> str:
        """
        保存汇总Excel表格

        Args:
            results: 评价结果列表
                [
                    {
                        'student_name': '张三',
                        'file_name': 'code.cpp',
                        'evaluation': '评价内容...',
                        'score': 85,  # 可选
                        'timestamp': '2024-01-01 10:00:00'
                    },
                    ...
                ]
            week: 周次
            filename: 自定义文件名（可选）

        Returns:
            保存的文件路径
        """
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, Alignment, PatternFill
        except ImportError:
            raise Exception("请安装openpyxl库: pip install openpyxl")

        # 生成文件名
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"第{week}周_评价汇总_{timestamp}.xlsx"

        file_path = os.path.join(self.output_dir, filename)

        # 创建工作簿
        wb = Workbook()
        ws = wb.active
        ws.title = f"第{week}周评价汇总"

        # 设置表头
        headers = ['序号', '学生姓名', '文件名', '评分', '评价时间', '评价内容']
        ws.append(headers)

        # 设置表头样式
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(color="FFFFFF", bold=True)

        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')

        # 填充数据
        for idx, result in enumerate(results, start=1):
            ws.append([
                idx,
                result.get('student_name', '未知'),
                result.get('file_name', ''),
                result.get('score', ''),
                result.get('timestamp', ''),
                result.get('evaluation', '')
            ])

        # 调整列宽
        ws.column_dimensions['A'].width = 8
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 20
        ws.column_dimensions['D'].width = 10
        ws.column_dimensions['E'].width = 20
        ws.column_dimensions['F'].width = 60

        # 设置文本对齐
        for row in ws.iter_rows(min_row=2):
            row[0].alignment = Alignment(horizontal='center')  # 序号
            row[1].alignment = Alignment(horizontal='center')  # 学生姓名
            row[3].alignment = Alignment(horizontal='center')  # 评分
            row[4].alignment = Alignment(horizontal='center')  # 时间
            row[5].alignment = Alignment(wrap_text=True, vertical='top')  # 评价内容

        # 保存文件
        wb.save(file_path)
        print(f"✓ 已保存汇总表格: {file_path}")
        return file_path

    def save_json(self, results: List[Dict], week: str = "02", filename: str = None) -> str:
        """
        保存为JSON格式（便于后续处理）

        Args:
            results: 评价结果列表
            week: 周次
            filename: 自定义文件名（可选）

        Returns:
            保存的文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"第{week}周_评价结果_{timestamp}.json"

        file_path = os.path.join(self.output_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"✓ 已保存JSON结果: {file_path}")
        return file_path


def main():
    """测试函数"""
    saver = ResultSaver()

    # 测试单个报告
    saver.save_individual_report(
        student_name="张三",
        file_name="test.cpp",
        evaluation="## 总体评分\n- 分数: 85/100\n\n## 优点\n- 代码逻辑清晰\n\n## 需要改进的地方\n- 需要添加注释",
        week="02"
    )

    # 测试汇总表格
    results = [
        {
            'student_name': '张三',
            'file_name': 'test1.cpp',
            'evaluation': '代码优秀',
            'score': 95,
            'timestamp': '2024-01-01 10:00:00'
        },
        {
            'student_name': '李四',
            'file_name': 'test2.cpp',
            'evaluation': '需要改进',
            'score': 75,
            'timestamp': '2024-01-01 10:05:00'
        }
    ]
    saver.save_summary_excel(results, week="02")


if __name__ == "__main__":
    main()
