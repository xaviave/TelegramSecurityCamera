import os
import cv2
import time
import datetime

import numpy as np


class VideoHandler:
    fps: int = 25
    resolution: set = (1280, 720)
    fourcc = cv2.VideoWriter_fourcc("M", "P", "4", "V")

    video_path: str = None
    video_folder_path: str = "videos"

    @staticmethod
    def _delete_images(image_files: list):
        for f in image_files:
            os.remove(f)

    def __init__(self):
        print("video")
        if os.path.exists(self.video_folder_path):
            os.makedirs(self.video_folder_path)

    def create_video_path(self):
        self.video_path = os.path.join(self.video_folder_path, f"move_detected_{time.time()}")
        os.makedirs(self.video_path)

    def save_image(self, image: np.ndarray):
        cv2.imwrite(os.path.join(self.video_path, f"img_{datetime.datetime.now()}"), image)

    def save_video(self):
        images = [
            f
            for f in os.path.listdir(self.video_path)
            if os.path.isfile(os.path.join(self.video_path, f)) and f.endswith(".jpg")
        ]
        video = cv2.VideoWriter(
            os.path.join(self.video_path, "move_detected.mp4"),
            fourcc=self.fourcc,
            fps=self.fps,
            frame_size=self.resolution,
        )

        for image in images:
            video.write(cv2.imread(image))

        video.release()
        self._delete_images(images)
