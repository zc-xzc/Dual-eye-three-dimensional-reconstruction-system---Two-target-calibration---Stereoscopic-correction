"""参数width指的是棋盘格宽方向黑白格子相交点个数
参数height指的是棋盘格长方向黑白格子相交点个数
参数left_video是左路相机ID，一般就是相机连接主板的USB接口号
参数right_video是右路相机ID，一般就是相机连接主板的USB接口号
PS：如果你的双目相机是单USB连接线的双目摄像头(
    左右摄像头被拼接在同一个视频中显示)，则设置left_video = 相机ID，而right_video = -1，
参数detect建议设置True，这样可实时检测棋盘格，方面调整角度
按键盘s或者c保存左右视图图片
————————————————
原文链接：https: // blog.csdn.net / guyuealian / article / details / 121301896
"""

#python get_stereo_images.py --left_video 0 --right_video 1 --width 8  --height 11  --save_dir "data/camera" --detect True

import subprocess

# 定义要运行的命令
command = [
    "python", "get_stereo_images.py",
    "--left_video", "0",
    "--right_video", "1",
    "--width", "8",
    "--height", "11",
    "--save_dir", "data/camera",
    "--detect", "True"
]

# 使用 subprocess 运行命令
subprocess.run(command)