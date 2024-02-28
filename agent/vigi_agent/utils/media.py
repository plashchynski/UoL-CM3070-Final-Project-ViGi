# This module contains utility functions for working with media files.

import cv2

def read_video_file_meta(video_path):
    """
    Read the metadata of a video file and return it as a dictionary.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = int(frame_count / fps)

    cap.release()

    return {
        "frame_width": frame_width,
        "frame_height": frame_height,
        "fps": fps,
        "frame_count": frame_count,
        "duration": duration
    }
