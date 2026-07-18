'''1. **视频路径和输出路径**：
   - `video_path` 是视频文件的路径。- `output_folder` 是保存抽取帧的图片的文件夹路径。
2. **帧率计算**：
   - 通过 `cap.get(cv2.CAP_PROP_FPS)` 获取视频的帧率。   - 根据目标帧率（每秒2帧）计算出每秒需要抽取的帧间隔。
3. **帧抽取与保存**：
   - 使用 `cv2.VideoCapture` 逐帧读取视频。  - 每隔 `frame_interval` 帧保存一次图片到指定文件夹。
4. **文件命名**：
   - 保存的图片文件命名为 `frame_0000.jpg`、`frame_0001.jpg` 等，便于排序和识别。
### 注意事项
- 确保视频文件路径和输出文件夹路径正确无误。- 如果视频文件较大或帧率较高，抽取过程可能需要一些时间。
- 如果输出文件夹不存在，代码会自动创建该文件夹。'''

import cv2
import os

def extract_frames(video_path, output_folder, fps=2):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("无法打开视频文件")
        return

    # 获取视频的帧率
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"视频帧率: {video_fps} fps")

    # 计算每秒需要抽取的帧间隔
    frame_interval = int(video_fps / fps)
    if frame_interval == 0:
        print("帧间隔为0，无法抽取帧")
        return

    # 初始化帧计数器
    frame_count = 0
    save_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 读取到视频末尾

        # 每隔frame_interval帧保存一次
        if frame_count % frame_interval == 0:
            output_path = os.path.join(output_folder, f"frame_{save_count:04d}.jpg")
            cv2.imwrite(output_path, frame)
            save_count += 1

        frame_count += 1

    print(f"共抽取了 {save_count} 帧")
    cap.release()

# 设置视频路径和输出文件夹路径
video_path = r"D:\yolov5-master\111.mp4"
output_folder = r"D:\yolov5-master\runs\date\image1"

# 调用函数
extract_frames(video_path, output_folder, fps=2)