import cv2

def test_camera():
    for i in range(10):  # 尝试设备 ID 0 到 9
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"摄像头 {i} 可用")
            ret, frame = cap.read()
            if ret:
                cv2.imshow(f"Camera {i}", frame)
                cv2.waitKey(1000)  # 显示1秒
                cv2.destroyAllWindows()
            cap.release()
        else:
            print(f"摄像头 {i} 不可用")

if __name__ == "__main__":
    test_camera()
