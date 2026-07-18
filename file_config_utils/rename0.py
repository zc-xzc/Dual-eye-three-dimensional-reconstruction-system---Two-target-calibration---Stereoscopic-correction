import os

def batch_rename(folder_path, prefix="", start_index=1, extension=None):
    """
    批量重命名文件夹中的文件

    :param folder_path: 文件夹路径
    :param prefix: 新文件名的前缀，默认为空
    :param start_index: 起始编号，默认为1
    :param extension: 如果指定扩展名，只重命名该扩展名的文件，否则重命名所有文件
    """
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"文件夹路径 {folder_path} 不存在")
        return

    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)

    # 过滤指定扩展名的文件（如果指定了扩展名）
    if extension:
        files = [f for f in files if f.endswith(extension)]

    # 对文件进行排序（确保按文件名顺序重命名）
    files.sort()

    # 遍历文件并重命名
    for index, filename in enumerate(files, start=start_index):
        # 构造新的文件名，编号为三位数
        new_filename = f"{prefix}{index:06d}{os.path.splitext(filename)[1]}"  # 修改为6位编号

        # 构造完整的旧文件路径和新文件路径
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)

        # 重命名文件
        os.rename(old_file_path, new_file_path)
        print(f"重命名文件：{filename} -> {new_filename}")

    print("批量重命名完成！")

# 设置相关参数
folder_path = r"D:\yolov5-master\dataset\dataset_all\images"  # 文件夹路径
prefix = ""  # 新文件名的前缀，这里为空
start_index = 0  # 起始编号
extension = ".jpg"  # 如果只想重命名特定扩展名的文件，可以指定扩展名，否则留空

# 调用函数
batch_rename(folder_path, prefix, start_index, extension)