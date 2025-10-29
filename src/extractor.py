"""
ZIP文件处理模块
负责解压和扫描作业文件
"""
import zipfile
import os
from pathlib import Path
from typing import List, Dict


class HomeworkExtractor:
    """作业文件提取器"""

    def __init__(self, zip_path: str, extract_path: str = "./data/extracted"):
        """
        初始化提取器

        Args:
            zip_path: ZIP文件路径
            extract_path: 解压目标路径
        """
        self.zip_path = zip_path
        self.extract_path = extract_path

    def extract_zip(self) -> str:
        """
        解压ZIP文件，并自动处理.cpp.txt文件

        Returns:
            解压后的目录路径
        """
        print(f"正在解压文件: {self.zip_path}")

        # 创建解压目录
        os.makedirs(self.extract_path, exist_ok=True)

        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                # 解压所有文件
                zip_ref.extractall(self.extract_path)
            print(f"✓ 文件已解压到: {self.extract_path}")

            # 自动处理.cpp.txt文件（重命名为.cpp）
            self._rename_cpp_txt_files(self.extract_path)

            return self.extract_path
        except zipfile.BadZipFile:
            raise Exception(f"错误: {self.zip_path} 不是有效的ZIP文件")
        except Exception as e:
            raise Exception(f"解压失败: {str(e)}")

    def scan_cpp_files(self, root_folder: str = None) -> List[Dict[str, str]]:
        """
        扫描所有C++文件

        Args:
            root_folder: 要扫描的根目录，默认为解压目录

        Returns:
            包含学生信息和代码路径的列表
            [
                {
                    'student_name': '张三',
                    'file_path': '/path/to/code.cpp',
                    'file_name': 'code.cpp',
                    'relative_path': '第02周上机作业/张三/code.cpp'
                },
                ...
            ]
        """
        if root_folder is None:
            root_folder = self.extract_path

        cpp_files = []
        root_path = Path(root_folder)

        print(f"\n正在扫描C++文件: {root_folder}")

        # 支持的C++文件扩展名
        cpp_extensions = ['.cpp', '.cc', '.cxx', '.c', '.h', '.hpp']

        # 遍历所有文件
        for file_path in root_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in cpp_extensions:
                # 尝试从路径中提取学生姓名
                student_name = self._extract_student_name(file_path, root_path)

                cpp_files.append({
                    'student_name': student_name,
                    'file_path': str(file_path.absolute()),
                    'file_name': file_path.name,
                    'relative_path': str(file_path.relative_to(root_path))
                })

        print(f"✓ 找到 {len(cpp_files)} 个C++文件")
        return cpp_files

    def _extract_student_name(self, file_path: Path, root_path: Path) -> str:
        """
        从文件路径中提取学生姓名

        支持的路径格式：
        1. 第02周上机作业/未分班/52********00+泮妍竹/代码文件/题目/main.cpp -> 泮妍竹
        2. 第02周上机作业/张三/code.cpp -> 张三
        3. 第02周上机作业/张三_code.cpp -> 张三
        4. 作业/2024001_张三.cpp -> 张三

        Args:
            file_path: 文件完整路径
            root_path: 根目录路径

        Returns:
            学生姓名
        """
        relative_path = file_path.relative_to(root_path)
        parts = relative_path.parts

        # 情况1: 路径中包含"学号+姓名"格式（如：52********00+泮妍竹）
        for part in parts:
            if '+' in part:
                # 提取+号后面的姓名
                name = part.split('+')[-1].strip()
                if name:
                    return name

        # 情况2: 文件在以学生姓名命名的文件夹中
        if len(parts) >= 2:
            # 从倒数第二个往前找，跳过"代码文件"、题目文件夹等
            for i in range(len(parts) - 2, -1, -1):
                folder_name = parts[i]
                # 排除一些常见的非学生名称的文件夹
                exclude_folders = ['src', 'include', 'homework', '作业', '代码文件',
                                   '未分班', '已分班', '__MACOSX']
                # 排除数字开头的（可能是题目编号）
                if folder_name not in exclude_folders and not folder_name[0].isdigit():
                    # 如果包含+号，提取后面的部分
                    if '+' in folder_name:
                        name = folder_name.split('+')[-1].strip()
                        if name:
                            return name
                    # 否则直接返回文件夹名
                    return folder_name

        # 情况3: 文件名包含学生姓名（使用下划线或+号分隔）
        file_stem = file_path.stem  # 不包含扩展名的文件名

        # 处理+号
        if '+' in file_stem:
            name = file_stem.split('+')[-1].strip()
            if name:
                return name

        # 处理下划线
        if '_' in file_stem:
            parts = file_stem.split('_')
            # 尝试找到看起来像姓名的部分（通常是中文或较短的英文）
            for part in parts:
                if part and not part.isdigit():
                    return part

        # 情况4: 无法提取，使用文件名（不含扩展名）
        return file_stem

    def read_code(self, file_path: str) -> str:
        """
        读取代码文件内容

        Args:
            file_path: 文件路径

        Returns:
            文件内容字符串
        """
        try:
            # 尝试多种编码
            encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        return f.read()
                except UnicodeDecodeError:
                    continue

            # 如果所有编码都失败，使用二进制模式读取
            with open(file_path, 'rb') as f:
                content = f.read()
                # 尝试解码，忽略错误
                return content.decode('utf-8', errors='ignore')
        except Exception as e:
            raise Exception(f"读取文件失败 {file_path}: {str(e)}")

    def _rename_cpp_txt_files(self, root_folder: str):
        """
        自动将.cpp.txt文件重命名为.cpp
        处理Windows系统下可能出现的文件扩展名问题

        Args:
            root_folder: 根目录路径
        """
        root_path = Path(root_folder)
        renamed_count = 0

        # 查找所有.cpp.txt文件
        for file_path in root_path.rglob('*.cpp.txt'):
            if file_path.is_file():
                # 新文件名：去掉.txt后缀
                new_path = file_path.with_suffix('')  # 移除最后的.txt
                try:
                    file_path.rename(new_path)
                    renamed_count += 1
                except Exception as e:
                    print(f"⚠ 重命名失败 {file_path.name}: {str(e)}")

        if renamed_count > 0:
            print(f"✓ 自动处理了 {renamed_count} 个 .cpp.txt 文件")

    def get_all_students(self, root_folder: str = None) -> List[Dict[str, any]]:
        """
        获取所有学生名单，包括未提交作业的学生
        支持多层嵌套结构，如：第02周上机作业/未分班/学号+姓名/代码文件/题目/main.cpp

        Args:
            root_folder: 要扫描的根目录，默认为解压目录

        Returns:
            学生信息列表
            [
                {
                    'student_name': '泮妍竹',
                    'student_id': '52********00',  # 如果能提取到学号
                    'has_submission': True,
                    'file_count': 2,
                    'files': [...]  # 如果有提交
                },
                ...
            ]
        """
        if root_folder is None:
            root_folder = self.extract_path

        root_path = Path(root_folder)
        students = {}

        print(f"\n正在扫描学生名单: {root_folder}")

        cpp_extensions = ['.cpp', '.cc', '.cxx', '.c', '.h', '.hpp']

        # 递归查找所有包含"学号+姓名"格式的文件夹
        def find_student_folders(path: Path, depth: int = 0, max_depth: int = 5):
            """递归查找学生文件夹"""
            if depth > max_depth:
                return

            for item in path.iterdir():
                # 跳过系统文件夹
                if item.name.startswith('.') or item.name in ['__MACOSX']:
                    continue

                if item.is_dir():
                    # 检查是否是学生文件夹（包含+号的格式）
                    if '+' in item.name:
                        # 提取学号和姓名
                        parts = item.name.split('+')
                        student_id = parts[0].strip() if len(parts) > 0 else ''
                        student_name = parts[-1].strip() if len(parts) > 1 else item.name

                        # 查找该学生的所有C++文件
                        cpp_files = []
                        for file_path in item.rglob('*'):
                            if file_path.is_file() and file_path.suffix.lower() in cpp_extensions:
                                cpp_files.append({
                                    'file_path': str(file_path.absolute()),
                                    'file_name': file_path.name,
                                    'relative_path': str(file_path.relative_to(root_path))
                                })

                        # 使用学号+姓名作为唯一标识
                        key = f"{student_id}+{student_name}" if student_id else student_name

                        students[key] = {
                            'student_name': student_name,
                            'student_id': student_id,
                            'has_submission': len(cpp_files) > 0,
                            'file_count': len(cpp_files),
                            'files': cpp_files
                        }
                    else:
                        # 继续递归查找
                        find_student_folders(item, depth + 1, max_depth)

        # 开始查找
        find_student_folders(root_path)

        # 如果没找到学号+姓名格式，使用旧的简单扫描方式
        if not students:
            print("  未找到标准格式（学号+姓名），使用简单扫描模式...")
            for item in root_path.iterdir():
                if item.is_dir():
                    if item.name.startswith('.') or item.name in ['__MACOSX']:
                        continue

                    student_name = item.name
                    cpp_files = []

                    for file_path in item.rglob('*'):
                        if file_path.is_file() and file_path.suffix.lower() in cpp_extensions:
                            cpp_files.append({
                                'file_path': str(file_path.absolute()),
                                'file_name': file_path.name,
                                'relative_path': str(file_path.relative_to(root_path))
                            })

                    students[student_name] = {
                        'student_name': student_name,
                        'student_id': '',
                        'has_submission': len(cpp_files) > 0,
                        'file_count': len(cpp_files),
                        'files': cpp_files
                    }

        # 转换为列表并排序
        student_list = sorted(students.values(), key=lambda x: x['student_name'])

        # 统计信息
        submitted_count = sum(1 for s in student_list if s['has_submission'])
        not_submitted_count = len(student_list) - submitted_count

        print(f"✓ 找到 {len(student_list)} 个学生")
        print(f"  - 已提交: {submitted_count} 人")
        print(f"  - 未提交: {not_submitted_count} 人")

        return student_list


def main():
    """测试函数"""
    # 示例用法
    extractor = HomeworkExtractor("./data/第02周上机作业.zip")

    # 解压文件
    extract_path = extractor.extract_zip()

    # 扫描C++文件
    cpp_files = extractor.scan_cpp_files()

    # 打印扫描结果
    print("\n扫描结果:")
    for idx, file_info in enumerate(cpp_files, 1):
        print(f"{idx}. 学生: {file_info['student_name']}")
        print(f"   文件: {file_info['relative_path']}")
        print()


if __name__ == "__main__":
    main()
