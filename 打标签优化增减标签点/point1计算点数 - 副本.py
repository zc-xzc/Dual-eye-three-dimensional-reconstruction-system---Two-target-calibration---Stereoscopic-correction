import os
import cv2
import numpy as np
from typing import List

def mask_to_polygon(mask: np.array, report: bool = False) -> List[int]:
    """
    将掩码转换为多边形格式
    :param mask: 掩码图像（二维数组）
    :param report: 是否打印报告
    :return: 多边形的坐标列表
    """
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    polygons = []
    for object in contours:
        coords = []
        for point in object:
            coords.append(int(point[0][0]))
            coords.append(int(point[0][1]))
        polygons.append(coords)

    if report:
        print(f"Number of points = {len(polygons[0])}")

    # 直接返回扁平化后的列表
    return [coord for polygon in polygons for coord in polygon]

def process_masks(image_dir: str, label_dir: str):
    """
    处理图像目录中的所有掩码文件，并将多边形结果保存到标签目录
    :param image_dir: 图像目录路径
    :param label_dir: 标签目录路径
    """
    # 确保标签目录存在
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)

    # 遍历图像目录中的所有掩码文件
    for filename in os.listdir(image_dir):
        if filename.endswith(".png") or filename.endswith(".jpg"):  # 假设掩码文件是PNG或JPG格式
            mask_path = os.path.join(image_dir, filename)
            mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)  # 以灰度模式读取掩码图像

            if mask is None:
                print(f"Failed to load mask: {mask_path}")
                continue

            # 将掩码转换为多边形
            polygons = mask_to_polygon(mask, report=True)

            # 保存多边形结果到标签文件
            label_filename = os.path.splitext(filename)[0] + ".txt"
            label_path = os.path.join(label_dir, label_filename)
            with open(label_path, "w") as label_file:
                label_file.write(" ".join(map(str, polygons)))

            print(f"Saved label to {label_path}")

# 定义目录路径
image_dir = r"D:\yolov5-master\runs\predict-seg\exp7"  # 图片目录
label_dir = r"D:\yolov5-master\runs\predict-seg\exp7\labels"  # 标签目录

# 处理掩码文件
process_masks(image_dir, label_dir)