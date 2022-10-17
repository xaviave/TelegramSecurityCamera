import cv2
import datetime

import numpy as np


from handlers.TelegramHandler import TelegramHandler


class CameraHandler(TelegramHandler):
    # Utility
    end_time: datetime.datetime = None
    video_time: datetime.datetime = datetime.timedelta(seconds=30)
    cap: cv2.VideoCapture
    kernel: np.array = np.ones((5, 5))

    # Key and Signals
    exit: bool = False
    # Camera handling
    frame: np.array
    grey_frame: np.array
    last_grey_frame: np.array = None

    def _handle_key(self):
        key = cv2.waitKey(40)
        if key in [13, 27] or cv2.getWindowProperty("live camera", cv2.WND_PROP_VISIBLE) < 1.0:
            self.exit = True

    def _detect_motion(self):
        diff_frame = cv2.absdiff(src1=self.grey_frame, src2=self.last_grey_frame)
        return len(np.unique(diff_frame)) < 10

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)

    def launch_camera(self):
        while not self.exit:
            ret, self.frame = self.cap.read()
            if not ret:
                continue

            self.grey_frame = cv2.GaussianBlur(src=cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY), ksize=(5, 5), sigmaX=0)
            if self.end_time is not None:
                if self.last_grey_frame is not None and self._detect_motion():
                    self.end_time = datetime.datetime.now() + self.video_time
                if datetime.now() > self.end_time:
                    self.send_video()
                    self.end_time = None
            else:
                self.save_image(self.frame)

            self.last_grey_frame = self.grey_frame
            cv2.imshow("live camera", self.frame)
            self._handle_key()

    def __call__(self):
        self.launch_camera()
        self._clean_camera()

    def _clean_camera(self):
        self.cap.release()
        cv2.destroyAllWindows()
