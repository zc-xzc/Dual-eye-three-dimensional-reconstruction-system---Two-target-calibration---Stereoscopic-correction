# Stereo 3D Reconstruction System

Dual-camera stereo vision system for 3D reconstruction, calibration, and distance measurement.

## Components

| Directory | Description |
|-----------|-------------|
| stereo_reconstruction_working/ | Working stereo reconstruction pipeline |
| stereo_reconstruction_custom/ | Custom implementation of stereo algorithms |
| hand_eye_calibration/ | Hand-eye calibration and coordinate transforms |
| hand_eye_download/ | Downloaded hand-eye calibration resources |
| label_optimization/ | Label point optimization tools |
| data_augmentation/ | Dataset augmentation and enhancement |
| ile_config_utils/ | File renaming and configuration tools |
| method_comparison/ | Algorithm comparison charts |
| 
elated_code/ | Related utility code |
| plotting/ | Data visualization and charts |
| paper_figures/ | Publication-quality figures |
| yolov12-main/ | YOLOv12 object detection integration |

## Features

- Stereo camera calibration (Zhang's method)
- Stereo rectification and correspondence
- Depth/disparity map computation
- 3D point cloud reconstruction
- Hand-eye calibration (eye-in-hand)
