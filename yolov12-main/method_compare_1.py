# -*- coding: utf-8 -*-
from ultralytics import YOLO

if __name__ == '__main__':
    # Load a model
    model = YOLO(model=r'D:\yolov12-main\yolov12n.pt')

    # Define the video sources
    video_sources = [
        r'D:\yolov12-main\video\WeChat_20250324123249.mp4',
        r'D:\yolov12-main\video\WeChat_20250324123257.mp4',
        r'D:\yolov12-main\video\WeChat_20250324123304.mp4',
        r'D:\yolov12-main\video\WeChat_20250324123309.mp4',
        r'D:\yolov12-main\video\WeChat_20250324123314.mp4'
    ]
    # Process each video
    for video_path in video_sources:
        print(f"Processing video: {video_path}")
        # Perform prediction on the current video
        model.predict(
            source=video_path,
            save=True,  # Save the output video with detections
            show=True,  # Show the output video with detections
        )