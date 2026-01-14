import os

def batch_rename_extension(folder_path, old_extension, new_extension):
    """
    批量修改文件夹中文件的扩展名

    :param folder_path: 文件夹路径
    :param old_extension: 原扩展名
    :param new_extension: 新扩展名
    """
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"文件夹路径 {folder_path} 不存在")
        return

    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)

    # 过滤指定扩展名的文件
    files = [f for f in files if f.endswith(old_extension)]

    # 遍历文件并修改扩展名
    for filename in files:
        # 构造新的文件名
        new_filename = os.path.splitext(filename)[0] + new_extension

        # 构造完整的旧文件路径和新文件路径
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)

        # 修改文件扩展名
        os.rename(old_file_path, new_file_path)
        print(f"修改扩展名：{filename} -> {new_filename}")

    print("批量修改扩展名完成！")

# 设置相关参数
folder_path = r"D:\Desktop\标签图片处理后\Images2"  # 文件夹路径
old_extension = ".png"  # 原扩展名
new_extension = ".jpg"  # 新扩展名

# 调用函数
batch_rename_extension(folder_path, old_extension, new_extension)