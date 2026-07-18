import argparse
import os
import random
import numpy as np
import cv2
import torch

class mosaic():
    def __init__(self, img_root, label_root, img_size):
        self.img_size = img_size
        self.label_root = label_root
        self.mosaic_border = [-self.img_size / 2, -self.img_size / 2]
        self.img_name = [f for f in os.listdir(img_root) if f.endswith(('.jpg', '.png', '.jpeg'))]  # 确保只处理图片文件
        self.indices = range(len(self.img_name))
        self.im_files = [os.path.join(img_root, x).replace("\\", "/") for x in self.img_name]  # 使用正斜杠
        self.labels = []
        self.gener_labels()

    def gener_labels(self):
        for n in self.img_name:
            label = []
            t = n.split('.')[0] + ".txt"
            label_file = os.path.join(self.label_root, t).replace("\\", "/")  # 使用正斜杠
            if not os.path.exists(label_file):
                print(f"Label file not found: {label_file}")
                continue
            with open(label_file, "r") as f:
                line = f.readlines()
                for l in line:
                    l = l.strip().split(' ')
                    label.append([float(s) for s in l])
            self.labels.append(np.array(label))

    def load_image(self, index):
        img_file = self.im_files[index]
        print(f"Loading image: {img_file}")  # 调试输出路径
        im = cv2.imread(img_file)
        if im is None:
            raise FileNotFoundError(f"无法加载图片: {img_file}")
        h0, w0 = im.shape[:2]
        r = self.img_size / max(h0, w0)
        if r != 1:
            interp = cv2.INTER_LINEAR if (r > 1) else cv2.INTER_AREA
            im = cv2.resize(im, (int(w0 * r), int(h0 * r)), interpolation=interp)
            return im, (h0, w0), im.shape[:2]  # im, hw_original, hw_resized
        return im, _, (h0, w0)

    def xywhn2xyxy(self, label, w, h, padw, padh):
        y = label.clone() if isinstance(label, torch.Tensor) else np.copy(label)
        y[:, 0] = w * (label[:, 0] - label[:, 2] / 2) + padw  # top left x
        y[:, 1] = h * (label[:, 1] - label[:, 3] / 2) + padh  # top left y
        y[:, 2] = w * (label[:, 0] + label[:, 2] / 2) + padw  # bottom right x
        y[:, 3] = h * (label[:, 1] + label[:, 3] / 2) + padh  # bottom right y
        return y

    def box_candidates(self, box1, box2, wh_thr=2, ar_thr=100, area_thr=0.1, eps=1e-16):
        w1, h1 = box1[2] - box1[0], box1[3] - box1[1]
        w2, h2 = box2[2] - box2[0], box2[3] - box2[1]
        ar = np.maximum(w2 / (h2 + eps), h2 / (w2 + eps))  # aspect ratio
        return (w2 > wh_thr) & (h2 > wh_thr) & (w2 * h2 / (w1 * h1 + eps) > area_thr) & (ar < ar_thr)  # candidates

    def load_mosaic4(self, index):
        labels4 = []
        s = self.img_size
        indices = [index] + random.choices(self.indices, k=3)  # 3 additional image indices
        random.shuffle(indices)
        yc, xc = (int(random.uniform(-x, 2 * s + x)) for x in self.mosaic_border)
        for i, index in enumerate(indices):
            img, _, (h, w) = self.load_image(index)
            if i == 0:  # top left
                img4 = np.full((s * 2, s * 2, img.shape[2]), 114, dtype=np.uint8)  # base image with 4 tiles
                x1a, y1a, x2a, y2a = max(xc - w, 0), max(yc - h, 0), xc, yc  # xmin, ymin, xmax, ymax (large image)
                x1b, y1b, x2b, y2b = w - (x2a - x1a), h - (y2a - y1a), w, h  # xmin, ymin, xmax, ymax (small image)
            elif i == 1:  # top right
                x1a, y1a, x2a, y2a = xc, max(yc - h, 0), min(xc + w, s * 2), yc
                x1b, y1b, x2b, y2b = 0, h - (y2a - y1a), min(w, x2a - x1a), h
            elif i == 2:  # bottom left
                x1a, y1a, x2a, y2a = max(xc - w, 0), yc, xc, min(s * 2, yc + h)
                x1b, y1b, x2b, y2b = w - (x2a - x1a), 0, w, min(y2a - y1a, h)
            elif i == 3:  # bottom right
                x1a, y1a, x2a, y2a = xc, yc, min(xc + w, s * 2), min(s * 2, yc + h)
                x1b, y1b, x2b, y2b = 0, 0, min(w, x2a - x1a), min(y2a - y1a, h)

            img4[y1a:y2a, x1a:x2a] = img[y1b:y2b, x1b:x2b]  # img4[ymin:ymax, xmin:xmax]
            padw = x1a - x1b
            padh = y1a - y1b
            labels = self.labels[index].copy()
            if labels.size:
                labels[:, 1:] = self.xywhn2xyxy(labels[:, 1:], w, h, padw, padh)  # normalized xywh to pixel xyxy format
            labels4.append(labels)
        # Concat/clip labels
        labels4 = np.concatenate(labels4, 0)
        for x in (labels4[:, 1:]):
            np.clip(x, 0, 2 * s, out=x)  # clip when using random_perspective()
        return img4, labels4

    def load_mosaic9(self, index):
        labels9 = []
        s = self.img_size
        indices = [index] + random.choices(self.indices, k=8)  # 8 additional image indices
        random.shuffle(indices)
        hp, wp = -1, -1
        for i, index in enumerate(indices):
            img, _, (h, w) = self.load_image(index)
            if i == 0:  # center
                img9 = np.full((s * 3, s * 3, img.shape[2]), 114, dtype=np.uint8)  # base image with 4 tiles
                h0, w0 = h, w
                c = s, s, s + w, s + h  # xmin, ymin, xmax, ymax (base) coordinates
            elif i == 1:  # top
                c = s, s - h, s + w, s
            elif i == 2:  # top right
                c = s + wp, s - h, s + wp + w, s
            elif i == 3:  # right
                c = s + w0, s, s + w0 + w, s + h
            elif i == 4:  # bottom right
                c = s + w0, s + hp, s + w0 + w, s + hp + h
            elif i == 5:  # bottom
                c = s + w0 - w, s + h0, s + w0, s + h0 + h
            elif i == 6:  # bottom left
                c = s + w0 - wp - w, s + h0, s + w0 - wp, s + h0 + h
            elif i == 7:  # left
                c = s - w, s + h0 - h, s, s + h0
            elif i == 8:  # top left
                c = s - w, s + h0 - hp - h, s, s + h0 - hp
            padx, pady = c[:2]
            x1, y1, x2, y2 = (max(x, 0) for x in c)
            labels = self.labels[index].copy()
            if labels.size:
                labels[:, 1:] = self.xywhn2xyxy(labels[:, 1:], w, h, padx, pady)
            labels9.append(labels)
            img9[y1:y2, x1:x2] = img[y1 - pady:, x1 - padx:]
            hp, wp = h, w
        yc, xc = (int(random.uniform(0, s)) for _ in self.mosaic_border)  # mosaic center x, y
        img9 = img9[yc:yc + 2 * s, xc:xc + 2 * s]
        labels9 = np.concatenate(labels9, 0)
        labels9[:, [1, 3]] -= xc
        labels9[:, [2, 4]] -= yc

        for x in (labels9[:, 1:]):
            np.clip(x, 0, 2 * s, out=x)  # clip when using random_perspective()

        return img9, labels9

    def img_show(self, index, type):
        if type == 4:
            img, label = self.load_mosaic4(index)
        elif type == 9:
            img, label = self.load_mosaic9(index)
        else:
            raise ValueError("类型参数有误")
        for box in label.tolist():
            x1, y1, x2, y2 = box[1:]
            img = cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color=(0, 0, 255), thickness=2)
        cv2.imwrite("zhanshi.jpg", img)
        cv2.imshow("img", img.astype(np.uint8))
        cv2.waitKey(0)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_root', type=str, default=r'D:\yolov5-master\dataset\dataset2\val\images')
    parser.add_argument('--label_root', type=str, default=r'D:\yolov5-master\dataset\dataset2\val\labels')
    parser.add_argument('--img_size', type=int, default=640, help='train, val image size (pixels)')
    return parser.parse_known_args()[0]


if __name__ == "__main__":
    opt = parse_opt()
    m = mosaic(img_root=opt.img_root, label_root=opt.label_root, img_size=640)
    m.img_show(0, 9)