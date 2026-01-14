import cv2
from ultralytics import YOLO

if __name__ == '__main__':
    # Load a model
    model = YOLO(model=r'D:\yolov12-main\yolov12n.pt')

    # Define the video sources
    video_sources = [
        r'D:\yolov12-main\video\WeChat_20250324123314.mp4',
        r'D:\yolov12-main\video\WeChat_20250324123314.mp4'
    ]

    for video_path in video_sources:
        # Define the output video path
        output_path = video_path.replace('.mp4', '_output.mp4')  # 修改输出文件名

        # Open the video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video {video_path}")
            continue

        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Create a VideoWriter object to save the output video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用 mp4v 编码器
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        print(f"Processing video: {video_path}")
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB (PIL format)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            from PIL import Image
            frame_pil = Image.fromarray(frame_rgb)

            # Predict on the frame
            results = model.predict(frame_pil)

            # Extract bounding boxes and draw them on the frame
            if results.boxes is not None:
                for box in results.boxes:
                    x1, y1, x2, y2 = map(int, box[:4])  # 提取边界框坐标
                    conf = box[4]  # 提取置信度
                    cls = int(box[5])  # 提取类别索引

                    # Draw bounding box and label
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f'{model.names[cls]} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Write the frame to the output video
            out.write(frame)

        # Release the video capture and writer
        cap.release()
        out.release()
        print(f"Processed video saved to: {output_path}")

    cv2.destroyAllWindows()
