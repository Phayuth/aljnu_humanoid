import numpy as np
import cv2


class HeadVision:

    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to capture frame from camera")
        return frame

    def release(self):
        self.cap.release()

    def move_pan_tilt(self, pan_angle, tilt_angle):
        print(
            f"Moving pan to {pan_angle} degrees and tilt to {tilt_angle} degrees"
        )


if __name__ == "__main__":
    head_vision = HeadVision()
    try:
        while True:
            frame = head_vision.get_frame()
            cv2.imshow("Head Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        head_vision.release()
        cv2.destroyAllWindows()
