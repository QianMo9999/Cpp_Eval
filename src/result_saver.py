"""
评价结果保存模块
支持保存为文本、Markdown、PDF和Excel格式
"""
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import json
import re


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
        headers = ['序号', '学号', '学生姓名', '文件名', '评分', '状态', '评价时间', '评价内容']
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
            # 确定状态
            status = result.get('status', 'evaluated')
            status_text = {
                'evaluated': '已评价',
                'not_submitted': '未提交',
                'failed': '评价失败'
            }.get(status, '未知')

            ws.append([
                idx,
                result.get('student_id', ''),
                result.get('student_name', '未知'),
                result.get('file_name', ''),
                result.get('score', ''),
                status_text,
                result.get('timestamp', ''),
                result.get('evaluation', '')
            ])

        # 调整列宽
        ws.column_dimensions['A'].width = 8   # 序号
        ws.column_dimensions['B'].width = 18  # 学号
        ws.column_dimensions['C'].width = 12  # 学生姓名
        ws.column_dimensions['D'].width = 20  # 文件名
        ws.column_dimensions['E'].width = 10  # 评分
        ws.column_dimensions['F'].width = 12  # 状态
        ws.column_dimensions['G'].width = 20  # 评价时间
        ws.column_dimensions['H'].width = 60  # 评价内容

        # 设置文本对齐
        for row in ws.iter_rows(min_row=2):
            row[0].alignment = Alignment(horizontal='center')  # 序号
            row[1].alignment = Alignment(horizontal='center')  # 学号
            row[2].alignment = Alignment(horizontal='center')  # 学生姓名
            row[4].alignment = Alignment(horizontal='center')  # 评分
            row[5].alignment = Alignment(horizontal='center')  # 状态
            row[6].alignment = Alignment(horizontal='center')  # 时间
            row[7].alignment = Alignment(wrap_text=True, vertical='top')  # 评价内容

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

    def save_student_pdf(
        self,
        student_name: str,
        student_id: str,
        evaluations: List[Dict],
        week: str = "02"
    ) -> str:
        """
        为每个学生生成一份PDF报告，包含所有题目的评价

        Args:
            student_name: 学生姓名
            student_id: 学号
            evaluations: 该学生的所有评价列表
                [
                    {
                        'file_name': 'main.cpp',
                        'evaluation': '评价内容...',
                        'score': 85,
                        'timestamp': '2024-01-01 10:00:00'
                    },
                    ...
                ]
            week: 周次

        Returns:
            保存的文件路径
        """
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import cm
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
            from reportlab.lib import colors
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            from reportlab.lib.enums import TA_CENTER, TA_LEFT
        except ImportError:
            raise Exception("请安装reportlab库: pip install reportlab")

        # 创建周次目录
        week_dir = os.path.join(self.output_dir, f"第{week}周_PDF")
        os.makedirs(week_dir, exist_ok=True)

        # 生成文件名
        safe_student_name = student_name.replace('/', '_').replace('\\', '_')
        student_display = f"{student_id}_{safe_student_name}" if student_id else safe_student_name
        file_path = os.path.join(week_dir, f"{student_display}_评价报告.pdf")

        # 注册中文字体（尝试使用系统字体）
        try:
            # macOS
            pdfmetrics.registerFont(TTFont('SimSun', '/System/Library/Fonts/STHeiti Light.ttc'))
            chinese_font = 'SimSun'
        except:
            try:
                # Windows
                pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))
                chinese_font = 'SimSun'
            except:
                # 如果都失败，使用默认字体（可能无法显示中文）
                chinese_font = 'Helvetica'
                print(f"⚠ 未找到中文字体，PDF中的中文可能无法正常显示")

        # 创建PDF文档
        doc = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        # 准备内容
        story = []

        # 创建样式
        styles = getSampleStyleSheet()

        # 标题样式
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName=chinese_font,
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=12,
            textColor=colors.HexColor('#1a5490')
        )

        # 副标题样式
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontName=chinese_font,
            fontSize=14,
            spaceAfter=10,
            textColor=colors.HexColor('#2c5282')
        )

        # 正文样式
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontName=chinese_font,
            fontSize=10,
            spaceAfter=6,
            leading=16
        )

        # 添加标题
        story.append(Paragraph(f"C++作业评价报告", title_style))
        story.append(Spacer(1, 0.5*cm))

        # 添加学生信息表格
        student_info = [
            ['学生姓名', student_name, '学号', student_id or '无'],
            ['作业周次', f'第{week}周', '评价时间', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ['题目总数', str(len(evaluations)), '总评分', self._calculate_total_score(evaluations)]
        ]

        info_table = Table(student_info, colWidths=[3*cm, 5*cm, 3*cm, 5*cm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), chinese_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e2e8f0')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#e2e8f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        story.append(info_table)
        story.append(Spacer(1, 0.8*cm))

        # 添加每个题目的评价
        for idx, eval_data in enumerate(evaluations, 1):
            # 题目标题
            file_name = eval_data.get('file_name', '未知文件')
            score = eval_data.get('score', 0)

            story.append(Paragraph(
                f"题目 {idx}: {file_name} (得分: {score}/100)",
                subtitle_style
            ))
            story.append(Spacer(1, 0.3*cm))

            # 评价内容
            evaluation_text = eval_data.get('evaluation', '无评价')

            # 【修复】改进评价内容处理，确保完整显示
            if not evaluation_text or evaluation_text.strip() == '':
                evaluation_text = "该题目暂无评价内容"
            
            # 清理和格式化评价内容
            evaluation_text = evaluation_text.strip()
            
            # 移除可能的题目标识重复
            evaluation_text = re.sub(r'^【题目\d+:.*?】\s*', '', evaluation_text)
            
            # 将评价内容按段落分割，改进显示效果
            paragraphs = evaluation_text.split('\n')
            
            for para in paragraphs:
                para = para.strip()
                if para:
                    # 【修复】改进特殊字符处理
                    # 转义XML特殊字符，但保留Markdown格式
                    safe_para = para.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    
                    # 处理Markdown格式
                    # 粗体 **text** -> <b>text</b>
                    safe_para = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', safe_para)
                    # 斜体 *text* -> <i>text</i>
                    safe_para = re.sub(r'\*(.*?)\*', r'<i>\1</i>', safe_para)
                    
                    try:
                        story.append(Paragraph(safe_para, body_style))
                    except Exception as e:
                        # 如果解析失败，使用纯文本
                        print(f"   ⚠ 段落解析失败，使用纯文本: {str(e)}")
                        # 移除所有HTML标签，使用纯文本
                        plain_text = re.sub(r'<[^>]+>', '', safe_para)
                        story.append(Paragraph(plain_text, body_style))
                else:
                    # 空行用小间距代替
                    story.append(Spacer(1, 0.1*cm))

            story.append(Spacer(1, 0.6*cm))

            # 如果不是最后一个题目，添加分隔线
            if idx < len(evaluations):
                story.append(Spacer(1, 0.3*cm))
                line_table = Table([['']], colWidths=[16*cm])
                line_table.setStyle(TableStyle([
                    ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#cbd5e0'))
                ]))
                story.append(line_table)
                story.append(Spacer(1, 0.5*cm))

        # 添加页脚
        story.append(Spacer(1, 1*cm))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontName=chinese_font,
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        story.append(Paragraph("本评价由AI自动生成，仅供参考", footer_style))

        # 生成PDF
        doc.build(story)

        print(f"✓ 已保存PDF报告: {file_path}")
        return file_path

    def _calculate_total_score(self, evaluations: List[Dict]) -> str:
        """
        计算总评分

        Args:
            evaluations: 评价列表

        Returns:
            格式化的分数字符串
        """
        scores = [e.get('score', 0) for e in evaluations if e.get('score') is not None]
        if not scores:
            return "0/0"

        total = sum(scores)
        avg = total / len(scores)
        return f"{avg:.1f} (总分: {total}/{len(scores)*100})"


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