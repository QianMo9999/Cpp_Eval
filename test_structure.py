#!/usr/bin/env python3
"""
测试extractor模块是否能正确处理实际的文件结构
"""
import sys
import os

# 添加src路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from extractor import HomeworkExtractor

def test_structure():
    """测试文件结构识别"""

    # 使用实际的目录路径
    test_dir = "/Users/qianmo/Downloads/第02周上机作业"

    if not os.path.exists(test_dir):
        print(f"错误: 测试目录不存在: {test_dir}")
        return

    print("=" * 60)
    print("测试文件结构识别")
    print("=" * 60)

    # 创建extractor（不使用ZIP，直接扫描目录）
    extractor = HomeworkExtractor("dummy.zip")
    extractor.extract_path = test_dir

    # 测试.cpp.txt文件重命名
    print("\n[测试1] 检测.cpp.txt文件...")
    extractor._rename_cpp_txt_files(test_dir)

    # 测试获取所有学生
    print("\n[测试2] 获取学生名单...")
    students = extractor.get_all_students(test_dir)

    print(f"\n找到 {len(students)} 个学生")

    # 显示前5个学生的详细信息
    print("\n学生详情（前5个）:")
    for i, student in enumerate(students[:5], 1):
        print(f"\n{i}. 学生: {student['student_name']}")
        print(f"   学号: {student.get('student_id', '无')}")
        print(f"   已提交: {'是' if student['has_submission'] else '否'}")
        print(f"   文件数: {student['file_count']}")

        if student['has_submission'] and student['file_count'] > 0:
            print(f"   文件列表:")
            for j, file_info in enumerate(student['files'][:3], 1):
                print(f"     {j}. {file_info['file_name']}")
                # 提取题目名称
                path_parts = file_info['relative_path'].split('/')
                if len(path_parts) >= 2:
                    topic = path_parts[-2]  # 题目文件夹名
                    print(f"        题目: {topic}")

    # 统计信息
    submitted = [s for s in students if s['has_submission']]
    not_submitted = [s for s in students if not s['has_submission']]

    print("\n" + "=" * 60)
    print("统计信息")
    print("=" * 60)
    print(f"总学生数: {len(students)}")
    print(f"已提交: {len(submitted)} 人")
    print(f"未提交: {len(not_submitted)} 人")

    if not_submitted:
        print("\n未提交名单:")
        for s in not_submitted[:10]:
            print(f"  - {s.get('student_id', '')} {s['student_name']}")

    # 统计每个学生的题目数
    if submitted:
        file_counts = [s['file_count'] for s in submitted]
        print(f"\n题目数统计:")
        print(f"  平均: {sum(file_counts)/len(file_counts):.1f} 题")
        print(f"  最多: {max(file_counts)} 题")
        print(f"  最少: {min(file_counts)} 题")

if __name__ == "__main__":
    test_structure()
