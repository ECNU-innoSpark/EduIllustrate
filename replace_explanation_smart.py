#!/usr/bin/env python3
"""
批量替换项目中所有 'explanation' 为 'explanation'
特别注意：保护第三方库 API，如 moviepy.VideoFileClip
"""

import os
import re
from pathlib import Path
import shutil

# 需要排除的目录
EXCLUDE_DIRS = {
    '.git', '__pycache__', 'node_modules', '.venv', 'venv',
    '.idea', '.vscode', 'dist', 'build', '*.egg-info'
}

# 需要处理的文件扩展名
INCLUDE_EXTENSIONS = {
    '.py', '.md', '.txt', '.json', '.yaml', '.yml',
    '.sh', '.bash', '.gitignore', '.toml', '.cfg', '.ini'
}

# 第三方库 API 保护列表（不应该被替换的）
PROTECTED_PATTERNS = [
    'VideoFileClip',  # moviepy 库的类名
    'video_path',     # 通用的视频路径变量名（需要保留因为指的是实际视频文件）
    'videoFile',      # 驼峰命名的视频文件
]

def should_process_file(file_path):
    """判断是否应该处理该文件"""
    path = Path(file_path)

    # 检查是否在排除目录中
    for part in path.parts:
        if part in EXCLUDE_DIRS or part.startswith('.'):
            return False

    # 检查文件扩展名
    if path.suffix in INCLUDE_EXTENSIONS or path.suffix == '':
        return True

    return False

def replace_in_content(content):
    """
    替换内容中的 explanation 为 explanation，保持大小写风格
    保护第三方库 API 名称
    """
    # 先保护第三方库 API，用占位符替换
    placeholders = {}
    for i, pattern in enumerate(PROTECTED_PATTERNS):
        placeholder = f"__PROTECTED_{i}__"
        placeholders[placeholder] = pattern
        content = content.replace(pattern, placeholder)

    # 执行替换
    replacements = [
        ('EXPLANATION', 'EXPLANATION'),           # 全大写
        ('Explanation', 'Explanation'),           # 首字母大写
        ('explanation', 'explanation'),           # 全小写
        ('EXPLANATION_', 'EXPLANATION_'),         # 大写+下划线
        ('explanation_', 'explanation_'),         # 小写+下划线
        ('Explanation_', 'Explanation_'),         # 首字母大写+下划线
        ('_explanation', '_explanation'),         # 下划线+小写
        ('_Explanation', '_Explanation'),         # 下划线+首字母大写
        ('_EXPLANATION', '_EXPLANATION'),         # 下划线+大写
        ('-explanation', '-explanation'),         # 连字符+小写
        ('-Explanation', '-Explanation'),         # 连字符+首字母大写
    ]

    result = content
    for old, new in replacements:
        result = result.replace(old, new)

    # 恢复被保护的 API
    for placeholder, original in placeholders.items():
        result = result.replace(placeholder, original)

    return result

def get_new_filename(filename):
    """获取重命名后的文件名"""
    # 先保护不应该改的部分
    protected = {}
    for i, pattern in enumerate(PROTECTED_PATTERNS):
        if pattern in filename:
            placeholder = f"__PROTECTED_{i}__"
            protected[placeholder] = pattern
            filename = filename.replace(pattern, placeholder)

    # 执行替换
    new_name = filename
    new_name = new_name.replace('explanation', 'explanation')
    new_name = new_name.replace('Explanation', 'Explanation')
    new_name = new_name.replace('EXPLANATION', 'EXPLANATION')

    # 恢复保护的部分
    for placeholder, original in protected.items():
        new_name = new_name.replace(placeholder, original)

    return new_name

def process_file(file_path):
    """处理单个文件"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 替换内容
        new_content = replace_in_content(content)

        # 如果内容有变化，写回文件
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ 已修改内容: {file_path}")
            return True
        return False
    except Exception as e:
        print(f"✗ 处理文件失败 {file_path}: {e}")
        return False

def rename_file(file_path):
    """重命名文件"""
    path = Path(file_path)
    new_name = get_new_filename(path.name)

    if new_name != path.name:
        new_path = path.parent / new_name
        if new_path.exists():
            print(f"⚠ 目标文件已存在，跳过重命名: {new_path}")
            return None

        try:
            shutil.move(str(path), str(new_path))
            print(f"✓ 已重命名: {path.name} -> {new_name}")
            return str(new_path)
        except Exception as e:
            print(f"✗ 重命名失败 {path}: {e}")
            return None
    return str(file_path)

def main():
    """主函数"""
    project_root = Path(__file__).parent
    print(f"项目根目录: {project_root}")
    print(f"保护的 API 模式: {PROTECTED_PATTERNS}")
    print("=" * 80)

    # 收集所有需要处理的文件
    all_files = []
    for root, dirs, files in os.walk(project_root):
        # 过滤排除的目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]

        for file in files:
            file_path = os.path.join(root, file)
            if should_process_file(file_path):
                all_files.append(file_path)

    print(f"找到 {len(all_files)} 个文件需要处理\n")

    # 第一步：替换文件内容
    print("步骤 1: 替换文件内容（保护第三方库 API）")
    print("-" * 80)
    modified_count = 0
    for file_path in all_files:
        if process_file(file_path):
            modified_count += 1

    print(f"\n内容修改完成: {modified_count}/{len(all_files)} 个文件被修改")
    print("=" * 80)

    # 第二步：重命名文件
    print("\n步骤 2: 重命名文件")
    print("-" * 80)

    # 需要重命名的文件
    files_to_rename = []
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]

        for file in files:
            if 'explanation' in file.lower():
                file_path = os.path.join(root, file)
                files_to_rename.append(file_path)

    renamed_count = 0
    renamed_files = []
    for file_path in files_to_rename:
        new_path = rename_file(file_path)
        if new_path and new_path != file_path:
            renamed_count += 1
            renamed_files.append((file_path, new_path))

    print(f"\n文件重命名完成: {renamed_count} 个文件被重命名")

    if renamed_files:
        print("\n重命名列表:")
        for old, new in renamed_files:
            print(f"  {Path(old).name} -> {Path(new).name}")

    print("=" * 80)
    print("\n✓ 所有替换完成!")
    print(f"  - 修改内容: {modified_count} 个文件")
    print(f"  - 重命名: {renamed_count} 个文件")
    print(f"\n保护的 API 已保留: {', '.join(PROTECTED_PATTERNS)}")

if __name__ == "__main__":
    main()
