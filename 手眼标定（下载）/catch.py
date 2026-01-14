import numpy as np
import os
import cv2
import glob
from scipy.spatial.transform import Rotation as R

# 设置标定板尺寸信息 单位（mm）
grid_size = 12.6
offset = 1.4
width = 15  # 标定板宽度
height = 13  # 标定板高度

# 设置相机参数
mtx = np.array([
    [916.28, 0, 650.7],
    [0, 916.088, 352.941],
    [0, 0, 1],
])

dist = np.array([0, 0, 0, 0, 0])

# 从marker_detect模块导入函数
from marker_detect import camera_calibrate, aruco_detect, generate_3D_point, eulerAnglesToRotationMatrix


def get_Ts_board_in_camera(img_name):
    img = cv2.imread(img_name)
    if img is None:
        print(f"Failed to read image: {img_name}")
        return None
    h, w, c = img.shape
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0, (w, h))  # 自由比例参数
    img = cv2.undistort(img, mtx, dist, None, newcameramtx)

    R_board_in_camera, T_board_in_camera = camera_calibrate(grid_size, offset, img)
    if R_board_in_camera is None or T_board_in_camera is None:
        print(f"Failed to calibrate camera for image: {img_name}")
        return None

    Ts_board_in_camera = np.zeros((4, 4), np.float)
    Ts_board_in_camera[:3, :3] = R_board_in_camera
    Ts_board_in_camera[:3, 3] = np.array(T_board_in_camera).flatten()
    Ts_board_in_camera[3, 3] = 1
    return Ts_board_in_camera


def get_Ts_hand_in_base(file):
    if not os.path.exists(file):
        print(f"File not found: {file}")
        return None
    with open(file, "r") as f:
        line = f.readline()
        Ts = line.split(" ")
        if len(Ts) != 6:
            print(f"Invalid data format in file: {file}")
            return None
        Ts = [float(i) for i in Ts]
        R_hand_in_base = R.from_euler('xyz', np.array(Ts[3:]), degrees=True).as_matrix()
        T_hand_in_base = Ts[:3]
        Ts_hand_in_base = np.zeros((4, 4), np.float)
        Ts_hand_in_base[:3, :3] = R_hand_in_base
        Ts_hand_in_base[:3, 3] = np.array(T_hand_in_base).flatten()
        Ts_hand_in_base[3, 3] = 1
    return Ts_hand_in_base


def calibrate_opencv(Ts_board_to_camera, Ts_hand_to_base):
    n = len(Ts_hand_to_base)

    R_base_to_hand = []
    T_base_to_hand = []
    R_board_to_camera = []
    T_board_to_camera = []

    for i in range(n):
        Ts_base_to_hand = np.linalg.inv(Ts_hand_to_base[i])
        R_base_to_hand.append(np.array(Ts_base_to_hand[:3, :3]))
        T_base_to_hand.append(np.array(Ts_base_to_hand[:3, 3]))
        R_board_to_camera.append(np.array(Ts_board_to_camera[i][:3, :3]))
        T_board_to_camera.append(np.array(Ts_board_to_camera[i][:3, 3]))

    if len(R_base_to_hand) < 3 or len(T_base_to_hand) < 3 or len(R_board_to_camera) < 3 or len(T_board_to_camera) < 3:
        print("Error: Not enough valid data for calibration.")
        return None, None

    R_camera_to_base, T_camera_to_base = cv2.calibrateHandEye(
        R_base_to_hand, T_base_to_hand, R_board_to_camera, T_board_to_camera,
        method=cv2.CALIB_HAND_EYE_TSAI
    )
    return R_camera_to_base, T_camera_to_base


def calibrate(path):
    imgs_name = glob.glob(os.path.join(path, "*-Color.png"))
    files_name = glob.glob(os.path.join(path, "*.txt"))

    print("Images found:", imgs_name)
    print("Files found:", files_name)

    n_files = len(imgs_name)
    print("Number of files:", n_files)

    if n_files < 3:
        print("Error: At least 3 files are needed for calibration.")
        return None, None

    Ts_hand_in_base_all = []
    Ts_board_in_camera_all = []

    for i in range(n_files):
        file_name = str(i + 1) + ".txt"
        img_name = str(i + 1) + "-Color.png"

        Ts_board_in_camera = get_Ts_board_in_camera(os.path.join(path, img_name))
        Ts_hand_in_base = get_Ts_hand_in_base(os.path.join(path, file_name))

        if Ts_board_in_camera is None or Ts_hand_in_base is None:
            print(f"Failed to get Ts_board_in_camera or Ts_hand_in_base for file {i+1}")
            continue

        Ts_board_in_camera_all.append(Ts_board_in_camera)
        Ts_hand_in_base_all.append(Ts_hand_in_base)

    print("Length of Ts_board_in_camera_all:", len(Ts_board_in_camera_all))
    print("Length of Ts_hand_in_base_all:", len(Ts_hand_in_base_all))

    if len(Ts_board_in_camera_all) < 3 or len(Ts_hand_in_base_all) < 3:
        print("Error: Not enough valid data for calibration.")
        return None, None

    R_camera_to_base, T_camera_to_base = calibrate_opencv(Ts_board_in_camera_all, Ts_hand_in_base_all)
    return R_camera_to_base, T_camera_to_base


if __name__ == '__main__':
    # 图片所在路径
    path = 'D:\\Downloads\\98872-main\\98872-main\\手眼标定\\data'
    print("Path:", path)

    R_camera_to_base, T_camera_to_base = calibrate(path)
    if R_camera_to_base is not None and T_camera_to_base is not None:
        print("Calibration successful!")
        print("Rotation matrix (R_camera_to_base):")
        print(R_camera_to_base)
        print("Translation vector (T_camera_to_base):")
        print(T_camera_to_base)
        Ts_camera_to_base = np.vstack((np.hstack((R_camera_to_base, T_camera_to_base)), np.array([0, 0, 0, 1])))
        # 存储标定结果矩阵
        np.savetxt("calibration.txt", Ts_camera_to_base)
    else:
        print("Calibration failed.")