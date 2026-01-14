import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
import time
import os  # 添加这一行，导入 os 模块


def read_image_label(path_to_img: str, path_to_txt: str, normalize: bool = False) -> Tuple[np.array, np.array]:
    # 读取图片
    image = cv2.imread(path_to_img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_h, img_w = image.shape[:2]

    # 读取标签文件
    with open(path_to_txt, "r") as f:
        txt_file = f.readlines()[0].split()
        cls_idx = txt_file[0]
        coords = txt_file[1:]
        polygon = np.array([[eval(x), eval(y)] for x, y in
                            zip(coords[0::2], coords[1::2])])  # 将坐标转换为 NumPy 数组

    # 如果需要，将归一化的坐标转换为图片的原始坐标
    if normalize:
        polygon[:, 0] = polygon[:, 0] * img_w
        polygon[:, 1] = polygon[:, 1] * img_h
    return image, polygon.astype(np.int32)


def show_image_mask(img: np.array, polygon: np.array, alpha: float = 0.7):
    # 创建掩膜
    mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    overlay = img.copy()

    # 在图片和掩膜上绘制多边形
    cv2.fillPoly(mask, pts=[polygon], color=(255, 255, 255))
    cv2.fillPoly(img, pts=[polygon], color=(255, 0, 0))
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    # 显示图片和掩膜
    fig = plt.figure(figsize=(22, 18))
    axes = fig.subplots(nrows=1, ncols=2)
    axes[0].imshow(img)
    axes[1].imshow(mask, cmap="Greys_r")
    axes[0].set_title("Original image with mask")
    axes[1].set_title("Mask")
    plt.show()


def reduce_polygon(polygon: np.array, angle_th: int = 0, distance_th: int = 0) -> np.array:
    angle_th_rad = np.deg2rad(angle_th)
    points_removed = [0]
    while len(points_removed):
        points_removed = list()
        for i in range(0, len(polygon) - 2, 2):
            v01 = polygon[i - 1] - polygon[i]
            v12 = polygon[i] - polygon[i + 1]
            d01 = np.linalg.norm(v01)
            d12 = np.linalg.norm(v12)
            if d01 < distance_th and d12 < distance_th:
                points_removed.append(i)
                continue
            angle = np.arccos(np.sum(v01 * v12) / (d01 * d12))
            if angle < angle_th_rad:
                points_removed.append(i)
        polygon = np.delete(polygon, points_removed, axis=0)
    return polygon


def show_result_reducing(polygon: List[List[int]]) -> List[Tuple[int, int]]:
    original_polygon = np.array([[x, y] for x, y in zip(polygon[0::2], polygon[1::2])])

    tic = time.time()
    reduced_polygon = reduce_polygon(original_polygon, angle_th=1, distance_th=20)
    toc = time.time()

    fig = plt.figure(figsize=(16, 5))
    axes = fig.subplots(nrows=1, ncols=2)
    axes[0].scatter(original_polygon[:, 0], original_polygon[:, 1], label=f"{len(original_polygon)}", c='b', marker='x',
                    s=2)
    axes[1].scatter(reduced_polygon[:, 0], reduced_polygon[:, 1], label=f"{len(reduced_polygon)}", c='b', marker='x',
                    s=2)
    axes[0].invert_yaxis()
    axes[1].invert_yaxis()

    axes[0].set_title("Original polygon")
    axes[1].set_title("Reduced polygon")
    axes[0].legend()
    axes[1].legend()

    plt.show()

    print("\n\n", f'[bold black] Original_polygon length[/bold black]: {len(original_polygon)}\n',
          f'[bold black] Reduced_polygon length[/bold black]: {len(reduced_polygon)}\n'
          f'[bold black] Running time[/bold black]: {round(toc - tic, 4)} seconds')

    return reduced_polygon


# 指定图片和标签文件的目录
image_dir = r"D:\yolov5-master\runs\predict-seg\exp7"  # 图片目录
label_dir = r"D:\yolov5-master\runs\predict-seg\exp7\labels"  # 标签目录

# 遍历图片目录中的所有图片
for img_name in os.listdir(image_dir):
    # 检查是否是图片文件
    if img_name.endswith(('.png', '.jpg', '.jpeg')):
        # 构建图片和标签文件的完整路径
        img_path = os.path.join(image_dir, img_name)
        txt_name = os.path.splitext(img_name)[0] + ".txt"
        txt_path = os.path.join(label_dir, txt_name)

        # 检查标签文件是否存在
        if os.path.exists(txt_path):
            # 读取图片和标签
            image, polygon = read_image_label(img_path, txt_path, normalize=True)

            # 显示原始图片和掩膜
            show_image_mask(image.copy(), polygon.copy())

            # 减少多边形点数并显示结果
            reduced_polygon = show_result_reducing(polygon.flatten().tolist())
        else:
            print(f"标签文件 {txt_path} 不存在")