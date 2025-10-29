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
        解压ZIP文件

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
        1. 第02周上机作业/张三/code.cpp -> 张三
        2. 第02周上机作业/张三_code.cpp -> 张三
        3. 作业/2024001_张三.cpp -> 张三

        Args:
            file_path: 文件完整路径
            root_path: 根目录路径

        Returns:
            学生姓名
        """
        relative_path = file_path.relative_to(root_path)
        parts = relative_path.parts

        # 情况1: 文件在以学生姓名命名的文件夹中
        if len(parts) >= 2:
            # 假设倒数第二个部分是学生文件夹
            folder_name = parts[-2]
            # 排除一些常见的非学生名称的文件夹
            if folder_name not in ['src', 'include', 'homework', '作业']:
                return folder_name

        # 情况2: 文件名包含学生姓名（使用下划线分隔）
        file_stem = file_path.stem  # 不包含扩展名的文件名
        if '_' in file_stem:
            # 取下划线前的部分或后的部分作为姓名
            parts = file_stem.split('_')
            # 尝试找到看起来像姓名的部分（通常是中文或较短的英文）
            for part in parts:
                if part and not part.isdigit():
                    return part

        # 情况3: 无法提取，使用文件名（不含扩展名）
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
