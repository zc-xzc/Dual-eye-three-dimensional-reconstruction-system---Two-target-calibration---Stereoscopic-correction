import json
import os
from PIL import Image
import numpy as np
import base64

img_path = r"D:\data\img/"  # 图片地址
txt_path = r"D:\data\txt/"  # txt地址
json_path = r"D:\data\json/"  # json保存地址
labels = os.listdir(txt_path)
# 标签名字
class_names = ["person", "dog"]

for label in labels:
    # 设置头部
    tupian = {
        "version": "5.1.1",
        "flags": {},
        "shapes": [],
        "imagePath": "",
        "imageData": "",
        "imageHeight": "",
        "imageWidth": ""

    }

    # 获取图片大小，并保存
    img = np.array(Image.open(img_path + label.strip('.txt') + '.jpg'))
    sh, sw = img.shape[0], img.shape[1]
    tupian["imageHeight"] = sh
    tupian["imageWidth"] = sw

    tupian["imagePath"] = os.path.basename(img_path)  # 获取文件名称
    # 读取base64编码，
    with open(img_path + label.strip('.txt') + '.jpg', "rb") as f:
        base64_data = base64.b64encode(f.read())
    tupian["imageData"] = str(base64_data, encoding='utf-8')

    # 读取txt
    with open(txt_path + label, 'r') as f:
        contents = f.readlines()
        shapes = []
        for content in contents:  # 循环每一行内容
            labeldicts = []
            shapess = {'label': "", "points": [], "group_id": None, "shape_type": "polygon", "flags": {}}  # 后缀
            content = content.strip('\n').split()
            shapess['label'] = class_names[int(content[0])]  # 保存label名称
            del content[0]  # 删除第一个元素，保留坐标
            list__ = [content[i:i + 2] for i in range(0, len(content), 2)]  # 修改数组，两个一组[x,y]
            for i in list__:
                x = float(i[0]) * sw
                y = float(i[1]) * sh
                labeldicts.append([x, y])
            shapess["points"] = labeldicts
            shapes.append(shapess)
        tupian["shapes"] = shapes

    b = json.dumps(tupian)
    f2 = open(json_path + label.strip('.txt') + '.json', 'w')
    f2.write(b)
    f2.close()
