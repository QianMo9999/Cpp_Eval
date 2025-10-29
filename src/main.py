"""
主程序 - C++作业自动评价系统
整合所有模块，提供完整的评价流程
"""
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, project_root)

from extractor import HomeworkExtractor
from llm_evaluator import get_evaluator
from result_saver import ResultSaver

# 导入prompts模块
from config.prompts import get_prompt, get_batch_prompt
import re


class HomeworkEvaluationSystem:
    """作业评价系统"""

    def __init__(
        self,
        zip_path: str,
        week: str = "02",
        api_provider: str = None,
        output_dir: str = "./output"
    ):
        """
        初始化评价系统

        Args:
            zip_path: ZIP文件路径
            week: 周次
            api_provider: API提供商
            output_dir: 输出目录
        """
        self.zip_path = zip_path
        self.week = week
        self.output_dir = output_dir

        # 初始化各模块
        self.extractor = HomeworkExtractor(zip_path)
        self.evaluator = get_evaluator(provider=api_provider)
        self.saver = ResultSaver(output_dir=output_dir)

        # 评价结果列表
        self.results = []

    def run(self, save_pdf: bool = True, save_excel: bool = False, save_json: bool = True):
        """
        运行完整的评价流程

        Args:
            save_pdf: 是否保存PDF报告（每个学生一份）
            save_excel: 是否保存Excel汇总
            save_json: 是否保存JSON结果

        Returns:
            评价结果列表
        """
        print("=" * 60)
        print("C++作业自动评价系统")
        print("=" * 60)
        print(f"ZIP文件: {self.zip_path}")
        print(f"作业周次: 第{self.week}周")
        print(f"输出目录: {self.output_dir}")
        print("=" * 60)

        # 1. 解压ZIP文件
        print("\n[步骤 1/4] 解压ZIP文件...")
        try:
            extract_path = self.extractor.extract_zip()
        except Exception as e:
            print(f"✗ 解压失败: {str(e)}")
            return []

        # 2. 扫描C++文件和学生名单
        print("\n[步骤 2/4] 扫描学生和作业文件...")
        try:
            # 获取所有学生（包括未提交的）
            all_students = self.extractor.get_all_students()

            if not all_students:
                print("✗ 未找到学生文件夹")
                return []

            # 统计未提交作业的学生
            not_submitted_students = [s for s in all_students if not s['has_submission']]
            submitted_students = [s for s in all_students if s['has_submission']]

            if not_submitted_students:
                print(f"\n⚠ 以下学生未提交作业:")
                for student in not_submitted_students:
                    student_name = student['student_name']
                    student_id = student.get('student_id', '')
                    print(f"   - {student_id} {student_name}" if student_id else f"   - {student_name}")
                    # 记录未提交的学生
                    self.results.append({
                        'student_name': student_name,
                        'student_id': student_id,
                        'file_name': '未提交',
                        'file_path': '',
                        'evaluation': '该学生未提交作业',
                        'score': 0,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'status': 'not_submitted'
                    })

        except Exception as e:
            print(f"✗ 扫描失败: {str(e)}")
            return []

        # 3. 批量评价已提交的作业（优化：一个学生的所有题目一次性评价）
        print(f"\n[步骤 3/4] 开始批量评价 (共{len(submitted_students)}个学生)...")
        print("💡 提示：现在使用批量评价模式，每个学生的所有题目一次性评价，速度更快！")
        print("💡 评价完一个学生立即生成PDF，无需等待所有人评价完成")
        print("-" * 60)

        pdf_count = 0
        for idx, student in enumerate(submitted_students, 1):
            student_name = student['student_name']
            student_id = student.get('student_id', '')
            num_problems = student['file_count']

            print(f"\n[{idx}/{len(submitted_students)}] 评价学生: {student_id} {student_name} ({num_problems}道题)")

            try:
                # 收集该学生的所有题目代码
                all_problems = []
                for file_info in student['files']:
                    file_path = file_info['file_path']
                    file_name = file_info['file_name']

                    # 从路径中提取题目名称
                    problem_name = self._extract_problem_name(file_info['relative_path'])

                    # 读取代码
                    code = self.extractor.read_code(file_path)

                    all_problems.append({
                        'problem_name': problem_name,
                        'file_name': file_name,
                        'file_path': file_path,
                        'code': code
                    })

                # 生成批量评价提示词
                batch_prompt = get_batch_prompt(
                    student_name=student_name,
                    student_id=student_id,
                    all_problems=all_problems,
                    week=self.week
                )

                # 一次性调用API评价所有题目
                print(f"   正在评价 {num_problems} 道题...")
                batch_evaluation = self.evaluator.evaluate(batch_prompt)

                # 解析批量评价结果
                problem_evaluations = self._parse_batch_evaluation(batch_evaluation, all_problems)

                # 准备该学生的所有评价数据
                student_evaluations = []

                # 记录每道题的评价结果
                for problem, evaluation_data in zip(all_problems, problem_evaluations):
                    result = {
                        'student_name': student_name,
                        'student_id': student_id,
                        'file_name': problem['file_name'],
                        'file_path': problem['file_path'],
                        'problem_name': problem['problem_name'],
                        'evaluation': evaluation_data['evaluation'],
                        'score': evaluation_data['score'],
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'status': 'evaluated'
                    }
                    self.results.append(result)

                    # 添加到学生评价列表（用于生成PDF）
                    student_evaluations.append({
                        'file_name': problem['file_name'],
                        'problem_name': problem['problem_name'],
                        'evaluation': evaluation_data['evaluation'],
                        'score': evaluation_data['score'],
                        'timestamp': result['timestamp']
                    })

                # 计算平均分
                scores = [e['score'] for e in problem_evaluations if e['score'] is not None]
                avg_score = sum(scores) / len(scores) if scores else 0
                print(f"✓ 评价完成 (平均分: {avg_score:.1f}/100，{len(scores)}/{num_problems}题)")

                # 【关键修改】评价完立即生成PDF
                if save_pdf and student_evaluations:
                    try:
                        print(f"   正在生成PDF报告...")
                        self.saver.save_student_pdf(
                            student_name=student_name,
                            student_id=student_id,
                            evaluations=student_evaluations,
                            week=self.week
                        )
                        pdf_count += 1
                        print(f"✓ PDF报告已生成")
                    except Exception as e:
                        print(f"⚠ PDF生成失败: {str(e)}")

            except Exception as e:
                print(f"✗ 评价失败: {str(e)}")
                # 记录失败信息（为该学生的每个文件都记录失败）
                for problem in all_problems if 'all_problems' in locals() else student['files']:
                    self.results.append({
                        'student_name': student_name,
                        'student_id': student_id,
                        'file_name': problem.get('file_name', ''),
                        'file_path': problem.get('file_path', ''),
                        'problem_name': problem.get('problem_name', ''),
                        'evaluation': f"评价失败: {str(e)}",
                        'score': None,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'status': 'failed'
                    })

        # 4. 保存结果
        print(f"\n[步骤 4/4] 保存评价结果...")

        print("-" * 60)

        if save_pdf:
            print(f"✓ 已生成 {pdf_count} 份PDF报告（评价过程中实时生成）")

        # 保存Excel汇总（可选）
        if save_excel and self.results:
            try:
                self.saver.save_summary_excel(self.results, week=self.week)
            except Exception as e:
                print(f"✗ Excel保存失败: {str(e)}")

        if save_json and self.results:
            try:
                self.saver.save_json(self.results, week=self.week)
            except Exception as e:
                print(f"✗ JSON保存失败: {str(e)}")

        # 5. 输出统计信息
        print("\n" + "=" * 60)
        print("评价完成!")
        print("=" * 60)

        # 分类统计
        evaluated_results = [r for r in self.results if r.get('status') == 'evaluated']
        not_submitted_results = [r for r in self.results if r.get('status') == 'not_submitted']
        failed_results = [r for r in self.results if r.get('status') not in ['evaluated', 'not_submitted']]

        print(f"学生总数: {len(all_students)} 人")
        print(f"  - 已提交并评价: {len(set([r['student_name'] for r in evaluated_results]))} 人")
        print(f"  - 未提交作业: {len(not_submitted_results)} 人")
        if failed_results:
            print(f"  - 评价失败: {len(set([r['student_name'] for r in failed_results]))} 人")

        # 分数统计（只统计已评价的）
        if evaluated_results:
            scores = [r['score'] for r in evaluated_results if r.get('score') is not None and r['score'] > 0]
            if scores:
                print(f"\n分数统计（所有题目）:")
                print(f"  - 平均分: {sum(scores) / len(scores):.1f}")
                print(f"  - 最高分: {max(scores)}")
                print(f"  - 最低分: {min(scores)}")

        print("=" * 60)

        return self.results

    def _extract_problem_name(self, relative_path: str) -> str:
        """
        从相对路径中提取题目名称

        Args:
            relative_path: 相对路径，如"未分班/学号+姓名/代码文件/第1关-求三位数-186949483/main.cpp"

        Returns:
            题目名称，如"第1关-求三位数"
        """
        # 分割路径
        parts = relative_path.split('/')

        # 倒数第二个通常是题目文件夹
        if len(parts) >= 2:
            problem_folder = parts[-2]
            # 移除最后的数字ID (如-186949483)
            problem_name = re.sub(r'-\d+$', '', problem_folder)
            return problem_name

        return "未知题目"

    def _parse_batch_evaluation(self, batch_evaluation: str, all_problems: list) -> list:
        """
        解析批量评价结果，提取每道题的评价和分数

        Args:
            batch_evaluation: 批量评价的完整文本
            all_problems: 题目列表

        Returns:
            每道题的评价数据列表
            [
                {'evaluation': '评价内容...', 'score': 85},
                ...
            ]
        """
        evaluations = []
        
        print(f"   正在解析 {len(all_problems)} 道题的评价结果...")
        print(f"   评价内容长度: {len(batch_evaluation)} 字符")
        
        # 【调试】输出AI返回的原始评价内容（前500字符）
        print(f"   AI返回内容预览: {batch_evaluation[:500]}...")
        if len(batch_evaluation) > 500:
            print(f"   ...（还有 {len(batch_evaluation) - 500} 个字符）")
        
        # 【调试】检查评价内容是否为空或过短
        if not batch_evaluation or len(batch_evaluation.strip()) < 10:
            print(f"   ⚠ 警告：AI返回的评价内容为空或过短！")
            print(f"   原始内容: '{batch_evaluation}'")
            # 为每道题提供默认评价
            for idx, problem in enumerate(all_problems):
                problem_name = problem.get('problem_name', f'题目{idx+1}')
                evaluations.append({
                    'evaluation': f"【题目{idx+1}: {problem_name}】\n\nAI评价失败，未能获取到评价内容。请检查API配置或网络连接。",
                    'score': 70  # 默认分数
                })
            return evaluations

        # 【修复】改进分割逻辑，支持多种分隔符格式
        sections = []
        
        # 方法1：尝试按 === 分隔
        temp_sections = re.split(r'={3,}', batch_evaluation)
        temp_sections = [s.strip() for s in temp_sections if s.strip()]
        
        if len(temp_sections) >= len(all_problems):
            sections = temp_sections
            print(f"   使用 === 分隔符成功分割为 {len(sections)} 个部分")
        else:
            # 方法2：尝试按 ### 题目N: 分隔
            temp_sections = re.split(r'###\s*题目\s*\d+\s*[:：]', batch_evaluation)
            temp_sections = [s.strip() for s in temp_sections if s.strip()]
            
            if len(temp_sections) >= len(all_problems):
                sections = temp_sections
                print(f"   使用 ### 题目N: 分隔符成功分割为 {len(sections)} 个部分")
            else:
                # 方法3：尝试按题目标题模式分隔
                # 匹配类似 "题目1:", "第1关", "第1题" 等模式
                pattern = r'(?:题目|第\d+关|第\d+题).*?[:：]'
                temp_sections = re.split(pattern, batch_evaluation)
                temp_sections = [s.strip() for s in temp_sections if s.strip()]
                
                if len(temp_sections) >= len(all_problems):
                    sections = temp_sections
                    print(f"   使用题目标题模式成功分割为 {len(sections)} 个部分")
                else:
                    # 方法4：按段落分割（最后的备选方案）
                    paragraphs = batch_evaluation.split('\n\n')
                    paragraphs = [p.strip() for p in paragraphs if p.strip()]
                    
                    # 尝试将段落重新组合成题目评价
                    if len(paragraphs) > len(all_problems):
                        # 将段落按题目数量平均分配
                        paras_per_problem = len(paragraphs) // len(all_problems)
                        sections = []
                        for i in range(len(all_problems)):
                            start_idx = i * paras_per_problem
                            end_idx = start_idx + paras_per_problem if i < len(all_problems) - 1 else len(paragraphs)
                            combined_section = '\n\n'.join(paragraphs[start_idx:end_idx])
                            sections.append(combined_section)
                        print(f"   使用段落重组方式分割为 {len(sections)} 个部分")
                    else:
                        sections = paragraphs
                        print(f"   使用段落分割为 {len(sections)} 个部分")

        # 【修复】如果仍然分割失败，使用整体评价作为每道题的评价
        if len(sections) < len(all_problems):
            print(f"   ⚠ 分割结果不足，将使用完整评价内容")
            # 为每道题使用完整的评价内容，并添加题目标识
            for idx, problem in enumerate(all_problems):
                problem_name = problem.get('problem_name', f'题目{idx+1}')
                
                # 尝试从完整评价中提取该题目的相关内容
                problem_evaluation = self._extract_problem_evaluation(batch_evaluation, problem_name, idx + 1)
                
                if not problem_evaluation:
                    problem_evaluation = f"【题目{idx+1}: {problem_name}】\n\n{batch_evaluation}"
                
                score = self._extract_score(problem_evaluation)
                
                evaluations.append({
                    'evaluation': problem_evaluation,
                    'score': score if score is not None else 75  # 默认分数
                })
        else:
            # 正常处理分割后的sections
            for idx, problem in enumerate(all_problems):
                if idx < len(sections):
                    section = sections[idx]
                    
                    # 【修复】确保评价内容完整
                    if len(section) < 50:  # 如果内容太短，可能是分割错误
                        print(f"   ⚠ 题目{idx+1}的评价内容较短，尝试补充...")
                        # 尝试合并相邻的section
                        if idx + 1 < len(sections):
                            section = section + "\n\n" + sections[idx + 1]
                    
                    # 添加题目标识（如果没有的话）
                    problem_name = problem.get('problem_name', f'题目{idx+1}')
                    if not re.search(r'题目\d+|第\d+关', section):
                        section = f"【题目{idx+1}: {problem_name}】\n\n{section}"
                    
                    # 提取分数
                    score = self._extract_score(section)
                    
                    evaluations.append({
                        'evaluation': section,
                        'score': score if score is not None else 75  # 默认分数
                    })
                else:
                    # 如果没有对应的section，使用默认评价
                    problem_name = problem.get('problem_name', f'题目{idx+1}')
                    evaluations.append({
                        'evaluation': f"【题目{idx+1}: {problem_name}】\n\n该题目的评价内容未能正确解析，请检查代码实现。",
                        'score': 60  # 默认分数
                    })

        print(f"   ✓ 成功解析 {len(evaluations)} 道题的评价")
        return evaluations

    def _extract_problem_evaluation(self, full_evaluation: str, problem_name: str, problem_index: int) -> str:
        """
        从完整评价中提取特定题目的评价内容
        
        Args:
            full_evaluation: 完整的评价文本
            problem_name: 题目名称
            problem_index: 题目序号
            
        Returns:
            该题目的评价内容
        """
        # 尝试多种模式匹配该题目的评价
        patterns = [
            rf'###\s*题目{problem_index}\s*[:：].*?(?=###\s*题目\d+|$)',
            rf'题目{problem_index}.*?(?=题目\d+|$)',
            rf'{re.escape(problem_name)}.*?(?=第\d+关|题目\d+|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, full_evaluation, re.DOTALL | re.IGNORECASE)
            if match:
                content = match.group(0).strip()
                if len(content) > 50:  # 确保内容足够长
                    return content
        
        return ""

    def _extract_score(self, evaluation: str) -> int:
        """
        从评价文本中提取分数

        Args:
            evaluation: 评价文本

        Returns:
            分数（0-100），如果未找到则返回None
        """
        # 【修复】改进分数提取逻辑，支持更多格式
        patterns = [
            r'\*\*分数\*\*\s*[:：]\s*(\d+)\s*/?\\s*100',  # **分数**: 85/100
            r'\*\*分数\*\*\s*[:：]\s*(\d+)',              # **分数**: 85
            r'分数\s*[:：]\s*(\d+)\s*/\s*100',            # 分数: 85/100
            r'分数\s*[:：]\s*(\d+)',                      # 分数: 85
            r'得分\s*[:：]\s*(\d+)',                      # 得分: 85
            r'评分\s*[:：]\s*(\d+)',                      # 评分: 85
            r'(\d+)\s*/\s*100',                          # 85/100
            r'(\d+)\s*分',                               # 85分
            r'score\s*[:：]\s*(\d+)',                    # score: 85
            r'总分\s*[:：]\s*(\d+)',                     # 总分: 85
        ]

        for pattern in patterns:
            matches = re.findall(pattern, evaluation, re.IGNORECASE)
            if matches:
                try:
                    # 取第一个匹配的分数
                    score = int(matches[0])
                    if 0 <= score <= 100:
                        return score
                except (ValueError, IndexError):
                    continue

        # 【新增】如果没有找到明确的分数，尝试从评价内容推断
        evaluation_lower = evaluation.lower()
        
        # 根据评价关键词推断分数
        if any(word in evaluation_lower for word in ['优秀', '很好', '完美', 'excellent', 'perfect']):
            return 90
        elif any(word in evaluation_lower for word in ['良好', '不错', 'good', 'well']):
            return 80
        elif any(word in evaluation_lower for word in ['一般', '还可以', 'average', 'ok']):
            return 70
        elif any(word in evaluation_lower for word in ['需要改进', '有问题', 'poor', 'bad']):
            return 60
        elif any(word in evaluation_lower for word in ['很差', '错误很多', 'terrible', 'fail']):
            return 40
        
        # 如果都没有匹配，返回None（调用方会使用默认分数）
        return None


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='C++作业自动评价系统')
    parser.add_argument('zip_path', help='作业ZIP文件路径')
    parser.add_argument('--week', default='02', help='作业周次 (默认: 02)')
    parser.add_argument('--provider', choices=['openai', 'claude', 'dashscope', 'deepseek'],
                        help='API提供商 (默认: 从.env读取)')
    parser.add_argument('--output', default='./output', help='输出目录 (默认: ./output)')
    parser.add_argument('--no-pdf', action='store_true', help='不生成PDF报告')
    parser.add_argument('--excel', action='store_true', help='同时生成Excel汇总')
    parser.add_argument('--no-json', action='store_true', help='不保存JSON结果')

    args = parser.parse_args()

    # 检查ZIP文件是否存在
    if not os.path.exists(args.zip_path):
        print(f"错误: ZIP文件不存在: {args.zip_path}")
        sys.exit(1)

    # 创建评价系统
    system = HomeworkEvaluationSystem(
        zip_path=args.zip_path,
        week=args.week,
        api_provider=args.provider,
        output_dir=args.output
    )

    # 运行评价
    try:
        results = system.run(
            save_pdf=not args.no_pdf,
            save_excel=args.excel,
            save_json=not args.no_json
        )
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ 系统错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()