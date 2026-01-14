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