#!/usr/bin/python
# -*- coding: UTF-8 -*-

import torchvision as tv
import torchvision.transforms as transforms
import torch as t
from PIL import Image

model_path = 'Stereo-Detection-main/yolov5-v6.1-pytorch-master/logs/ep140-loss0.081-val_loss0.066.pth'
def pridict():

    device = t.device("cuda" if t.cuda.is_available() else "cpu")
    model = t.load(model_path, device)  # 创建一个模型
   # model = model.to(device)

  #  model.eval()  # 预测模式

    # 获取测试图片，并行相应的处理
    img = Image.open('battery11.jpg')
    transform = transforms.Compose([transforms.Resize(256),  # 重置图像分辨率
                                    transforms.CenterCrop(224),  # 中心裁剪
                                    transforms.ToTensor(), ])
    img = img.convert("RGB")  # 如果是标准的RGB格式，则可以不加
    img = transform(img)
    img = img.unsqueeze(0)
    img = img.to(device)

    with t.no_grad():
        py = model(img)
    _, predicted = t.max(py, 1)  # 获取分类结果
    classIndex_ = predicted[0]

    print('预测结果', classIndex_)


if __name__ == '__main__':
    pridict()
