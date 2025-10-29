"""
主程序 - C++作业自动评价系统
整合所有模块，提供完整的评价流程
"""
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extractor import HomeworkExtractor
from llm_evaluator import get_evaluator
from result_saver import ResultSaver

# 添加config路径
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config')
sys.path.insert(0, config_path)

from config.prompts import get_prompt


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

    def run(self, save_individual: bool = True, save_excel: bool = True, save_json: bool = True):
        """
        运行完整的评价流程

        Args:
            save_individual: 是否保存单个学生的报告
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

        # 2. 扫描C++文件
        print("\n[步骤 2/4] 扫描C++文件...")
        try:
            cpp_files = self.extractor.scan_cpp_files()
            if not cpp_files:
                print("✗ 未找到C++文件")
                return []
        except Exception as e:
            print(f"✗ 扫描失败: {str(e)}")
            return []

        # 3. 逐个评价
        print(f"\n[步骤 3/4] 开始评价 (共{len(cpp_files)}个文件)...")
        print("-" * 60)

        for idx, file_info in enumerate(cpp_files, 1):
            student_name = file_info['student_name']
            file_path = file_info['file_path']
            file_name = file_info['file_name']

            print(f"\n[{idx}/{len(cpp_files)}] 评价学生: {student_name} ({file_name})")

            try:
                # 读取代码
                code = self.extractor.read_code(file_path)

                # 生成提示词
                prompt = get_prompt(
                    student_name=student_name,
                    filename=file_name,
                    code=code,
                    week=self.week
                )

                # 调用大模型评价
                evaluation = self.evaluator.evaluate(prompt)

                # 提取分数（如果评价中包含分数）
                score = self._extract_score(evaluation)

                # 记录结果
                result = {
                    'student_name': student_name,
                    'file_name': file_name,
                    'file_path': file_path,
                    'evaluation': evaluation,
                    'score': score,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self.results.append(result)

                # 保存单个报告
                if save_individual:
                    self.saver.save_individual_report(
                        student_name=student_name,
                        file_name=file_name,
                        evaluation=evaluation,
                        week=self.week,
                        format="markdown"
                    )

                print(f"✓ 评价完成 (分数: {score}/100)" if score else "✓ 评价完成")

            except Exception as e:
                print(f"✗ 评价失败: {str(e)}")
                # 记录失败信息
                self.results.append({
                    'student_name': student_name,
                    'file_name': file_name,
                    'file_path': file_path,
                    'evaluation': f"评价失败: {str(e)}",
                    'score': None,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        # 4. 保存汇总结果
        print(f"\n[步骤 4/4] 保存汇总结果...")
        print("-" * 60)

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
        print(f"总计评价: {len(cpp_files)} 个文件")
        print(f"成功: {len([r for r in self.results if r.get('score') is not None])} 个")
        print(f"失败: {len([r for r in self.results if r.get('score') is None])} 个")

        if self.results and any(r.get('score') for r in self.results):
            scores = [r['score'] for r in self.results if r.get('score') is not None]
            print(f"平均分: {sum(scores) / len(scores):.1f}")
            print(f"最高分: {max(scores)}")
            print(f"最低分: {min(scores)}")

        print("=" * 60)

        return self.results

    def _extract_score(self, evaluation: str) -> int:
        """
        从评价文本中提取分数

        Args:
            evaluation: 评价文本

        Returns:
            分数（0-100），如果未找到则返回None
        """
        import re

        # 尝试匹配常见的分数格式
        patterns = [
            r'分数[：:]\s*(\d+)\s*/?\s*100',
            r'得分[：:]\s*(\d+)',
            r'评分[：:]\s*(\d+)',
            r'(\d+)\s*/\s*100',
        ]

        for pattern in patterns:
            match = re.search(pattern, evaluation)
            if match:
                try:
                    score = int(match.group(1))
                    if 0 <= score <= 100:
                        return score
                except ValueError:
                    continue

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
    parser.add_argument('--no-individual', action='store_true', help='不保存单个报告')
    parser.add_argument('--no-excel', action='store_true', help='不保存Excel汇总')
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
            save_individual=not args.no_individual,
            save_excel=not args.no_excel,
            save_json=not args.no_json
        )
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ 系统错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
