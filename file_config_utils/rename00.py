#用于将指定文件夹中的文件按顺序重命名为 0.jpg、1.jpg、2.jpg
import os
def rename_files(folder_path):
    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)

    # 过滤出所有.jpg文件，并按文件名排序（确保顺序正确）
    jpg_files = sorted([f for f in files if f.endswith('.jpg')])

    # 遍历文件列表并重命名
    for index, filename in enumerate(jpg_files):
        # 构造新的文件名（格式为数字.jpg）
        new_filename = f"{index}.jpg"
        # 构造完整的旧文件路径和新文件路径
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)
        # 重命名文件
        os.rename(old_file_path, new_file_path)
        print(f"重命名文件：{filename} -> {new_filename}")


# 设置你的文件夹路径
folder_path = r"D:\Desktop\PycharmProjects\数据增强\0406\img"  # 替换为你的文件夹路径
rename_files(folder_path)