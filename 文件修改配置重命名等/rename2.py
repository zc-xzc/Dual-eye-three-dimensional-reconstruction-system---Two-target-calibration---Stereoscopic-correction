import os

# 设置文件夹路径
folder_path = r"D:\Desktop\标签图片处理后\Images"

# 获取文件夹中所有文件名
files = os.listdir(folder_path)

# 按照文件名进行排序（如果需要的话，确保文件处理顺序是正确的）
files.sort()

# 初始化计数器
counter = 10

# 遍历文件夹中的文件并重命名
for file in files:
    # 构造新的文件名
    new_file_name = f"right_{counter:04d}"  # 使用格式化字符串，确保数字部分有四位，不足补零
    counter += 10  # 每次增加10

    # 获取文件的扩展名
    file_extension = os.path.splitext(file)[1]

    # 构造完整的旧文件路径和新文件路径
    old_file_path = os.path.join(folder_path, file)
    new_file_path = os.path.join(folder_path, new_file_name + file_extension)

    # 重命名文件
    os.rename(old_file_path, new_file_path)

print("文件重命名完成！")