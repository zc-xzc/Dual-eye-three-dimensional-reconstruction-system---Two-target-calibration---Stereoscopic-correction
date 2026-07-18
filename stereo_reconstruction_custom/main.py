import os
import cv2

class StereoCamera(object):
    def __init__(self, chess_width, chess_height, detect=False):
        self.chess_width = chess_width
        self.chess_height = chess_height
        self.detect = detect
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    def detect_chessboard(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (self.chess_width, self.chess_height), None)
        if ret:
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
            image = cv2.drawChessboardCorners(image, (self.chess_width, self.chess_height), corners2, ret)
        return image

    def capture2(self, left_video, right_video, save_dir):
        self.create_file(save_dir)
        capL = cv2.VideoCapture(left_video)
        capR = cv2.VideoCapture(right_video)
        widthL, heightL, numFramesL, fpsL = self.get_video_info(capL)
        widthR, heightR, numFramesR, fpsR = self.get_video_info(capR)
        print("capL:\n", widthL, heightL, numFramesL, fpsL)
        print("capR:\n", widthR, heightR, numFramesR, fpsR)
        save_videoL = os.path.join(save_dir, "video", "left_video.avi")
        save_videoR = os.path.join(save_dir, "video", "right_video.avi")
        writerL = self.get_video_writer(save_videoL, widthL, heightL, fpsL)
        writerR = self.get_video_writer(save_videoR, widthR, heightR, fpsR)
        i = 0
        while True:
            isuccessL, frameL = capL.read()
            isuccessR, frameR = capR.read()
            if not (isuccessL and isuccessR):
                print("No more frames")
                break
            if self.detect:
                l = self.detect_chessboard(frameL.copy())
                r = self.detect_chessboard(frameR.copy())
            else:
                l = frameL.copy()
                r = frameR.copy()
            cv2.imshow('left', l)
            cv2.imshow('right', r)
            key = cv2.waitKey(10)
            if key == ord('q'):
                break
            elif key == ord('c') or key == ord('s'):
                print("save image:{:0=3d}".format(i))
                cv2.imwrite(os.path.join(save_dir, "left_{:0=3d}.png".format(i)), frameL)
                cv2.imwrite(os.path.join(save_dir, "right_{:0=3d}.png".format(i)), frameR)
                i += 1
            writerL.write(frameL)
            writerR.write(frameR)
        capL.release()
        capR.release()
        cv2.destroyAllWindows()

    @staticmethod
    def get_video_info(video_cap):
        width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        numFrames = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(video_cap.get(cv2.CAP_PROP_FPS))
        return width, height, numFrames, fps

    @staticmethod
    def get_video_writer(save_path, width, height, fps):
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        frameSize = (int(width), int(height))
        video_writer = cv2.VideoWriter(save_path, fourcc, fps, frameSize)
        print("video:width:{},height:{},fps:{}".format(width, height, fps))
        return video_writer

    @staticmethod
    def create_file(parent_dir, dir1=None, filename=None):
        out_path = parent_dir
        if dir1:
            out_path = os.path.join(parent_dir, dir1)
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        if filename:
            out_path = os.path.join(out_path, filename)
        return out_path

if __name__ == '__main__':
    stereo = StereoCamera(8, 11, detect=True)
    left_video = 1  # 左摄像头的设备 ID
    right_video = 2  # 右摄像头的设备 ID
    save_dir = "data/camera"  # 确保这个目录存在
    stereo.capture2(left_video=left_video, right_video=right_video, save_dir=save_dir)