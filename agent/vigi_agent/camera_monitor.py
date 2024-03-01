import threading
from datetime import datetime
import time
import logging

import cv2

from .motion_detector import MotionDetector

from vigi_agent.utils.fps_calculator import FPSCalculator
from .utils.pub_sub import PubSub


class CameraMonitor(threading.Thread):
    """
    A class that monitors the camera for motion and publishes the video stream from the camera.
    """

    def __init__(self, video_recorder = None, camera_id=0, max_errors=50, add_seconds_after_motion=3):
        """
        max_errors: int - the maximum number of consecutive errors when reading a frame from the camera
                            before the camera monitor stops. It's used to prevent the camera monitor from
                            creating a big number of small recordings on each small motion.
        add_seconds_after_motion: int - the number of seconds to add to the video after the motion is detected
        """
        super().__init__()

        self.camera_id = camera_id
        self.max_errors = max_errors
        self.add_seconds_after_motion = add_seconds_after_motion

        # Initialize the PubSub object to stream the frames from the camera
        # so other parts of the application can access the stream of frames
        self.frame_stream = PubSub()

        # Initialize the motion detector, when motion is detected, the motion_callback will be called
        self.motion_detector = MotionDetector(motion_callback=self.motion_callback)

        # video_recorder is used to save the video to a file when motion is detected
        self.video_recorder = video_recorder

        # save the start time of the camera monitor to calculate the uptime
        self.start_time = datetime.now()

        self.fps_calculator = FPSCalculator(max_history_size=50)

        # number of frames to add after the motion is over,
        # initially it's set to 0, but it could be assigned a value when the motion is detected
        # and decremented in each frame until it reaches 0
        self.add_frames = 0

    def current_fps(self):
        """
        Returns the current FPS of the system using the FPS calculator if it has calculated the FPS,
        otherwise returns the FPS of the camera.
        """
        fps = self.fps_calculator.current_fps()
        logging.info(f"Calculated FPS = {fps}")
        if fps is None:
            logging.warning(f"FPS is not calculated yet, using the camera's FPS = {self.fps}")
            fps = self.camera_fps

        return fps

    def motion_callback(self):
        logging.info("Motion detected!")

        self.add_frames = self.add_seconds_after_motion * self.current_fps()

        if self.video_recorder.is_recording():
            logging.info("Motion detected while the video is being recorded.")
            return

        # We need to determine the FPS of the camera to pass it to the video recorder
        # as FPS will be saved as metadata in the video file
        # if FPS will be overestimated, the video will be played faster than it should be
        # if FPS will be underestimated, the video will be played slower than it should be
        # Start recording the video:
        self.video_recorder.start_recording(frame_width=self.frame_width, frame_height=self.frame_height,
                                            fps=self.current_fps())

    def run(self):
        # Initialize the camera with OpenCV
        logging.info("Starting camera monitor... ")
        camera = cv2.VideoCapture(self.camera_id)  # Use 0 for the first webcam
        if camera.isOpened():
            logging.info("Camera opened successfully.")
        else:
            logging.error(f"Camera with ID={self.camera_id} could not be opened.")
            return

        self.frame_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frame_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.camera_fps = camera.get(cv2.CAP_PROP_FPS)
        logging.info(f"Camera parameters: frame width: {self.frame_width}, frame height: {self.frame_height}, FPS: {self.camera_fps}")

        error_count = 0
        while True:
            success, frame = camera.read()  # Read a frame from the camera
            if not success:
                # If the camera fails to read a frame:
                # - Increment the error count
                # - Print an error message
                # - Sleep for 1 second
                #
                # If the error count reaches the maximum number of consecutive errors:
                # - print an error message and break the loop

                error_count += 1
                if error_count >= self.max_errors:
                    logging.fatal(f"Maximum number of consecutive errors ({self.max_errors}) reached. Exiting.")
                    break

                logging.error(f"Failed to read a frame from the camera with ID={self.camera_id}")
                time.sleep(1)
                continue

            # Reset the error count if a frame is successfully read
            error_count = 0

            # Apply the motion detector to the frame
            frame = self.motion_detector.update(frame)

            # Publish the frame to the frame stream
            self.frame_stream.publish(frame)

            # if motion is not detected anymore and the video is being recorded, then stop the recording
            if not self.motion_detector.is_motion_detected() and self.video_recorder.is_recording():
                self.add_frames -= 1
                if self.add_frames <= 0:
                    self.video_recorder.еnd_recording()

            # here we send all frames to the video recorder, it's up to the video recorder to decide if
            # it should record the frame or not. It could decide to record additional frames before and after
            # the motion is detected
            self.video_recorder.add_frame(frame)
            self.fps_calculator.update()

        # OpenCV cleanup
        camera.release()
