import sys
import threading
from time import sleep

import cv2
import numpy as np
import process
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage
from beepy.make_sound import beep
import pyttsx3

class Window(QMainWindow):
    def __init__(self):
        self.engine = pyttsx3.init()
        super(Window, self).__init__()
        loadUi('GUImain.ui', self)
        with open("style.css", "r") as css:
            self.setStyleSheet(css.read())
        self.face_decector, self.eye_detector, self.detector = process.init_cv()
        self.startButton.clicked.connect(self.start_webcam)
        self.stopButton.clicked.connect(self.stop_webcam)
        self.camera_is_running = False
        self.previous_right_keypoints = None
        self.previous_left_keypoints = None
        self.previous_right_blob_area = None
        self.previous_left_blob_area = None
        self.detect_eye_time_start = None
        self.detect_eye_time_end = None
        self.can_play = True
        self.right_can_play = True
        self.is_left_detected = False
        self.is_right_detected = False


    def start_webcam(self):
        if not self.camera_is_running:
            # self.capture = cv2.VideoCapture(cv2.CAP_DSHOW)  # VideoCapture(0) sometimes drops error #-1072875772
            self.capture = cv2.VideoCapture(0)  # VideoCapture(0) sometimes drops error #-1072875772
            if self.capture is None:
                self.capture = cv2.VideoCapture(0)
            self.camera_is_running = True
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(2)

    def stop_webcam(self):
        if self.camera_is_running:
            self.capture.release()
            self.timer.stop()
            self.camera_is_running = not self.camera_is_running

    def update_frame(self):  # logic of the main loop

        _, base_image = self.capture.read()
        self.display_image(base_image)

        processed_image = cv2.cvtColor(base_image, cv2.COLOR_RGB2GRAY)

        face_frame, face_frame_gray, left_eye_estimated_position, right_eye_estimated_position, distance, _, _ = process.detect_face(
            base_image, processed_image, self.face_decector)

        if face_frame is not None:
            self.distanseText.setText(distance)
            left_eye_frame, right_eye_frame, left_eye_frame_gray, right_eye_frame_gray = process.detect_eyes(face_frame,
                                                                                                             face_frame_gray,
                                                                                                             left_eye_estimated_position,
                                                                                                             right_eye_estimated_position,
                                                                                                             self.eye_detector)
            if (left_eye_frame is None and right_eye_frame is None):
                self.can_play = True
                self.right_can_play = True
            if right_eye_frame is not None:
                if self.rightEyeCheckbox.isChecked():
                    right_eye_threshold = self.rightEyeThreshold.value()
                    right_keypoints, self.previous_right_keypoints, self.previous_right_blob_area = self.get_keypoints(
                        right_eye_frame, right_eye_frame_gray, right_eye_threshold,
                        previous_area=self.previous_right_blob_area,
                        previous_keypoint=self.previous_right_keypoints)
                    process.draw_blobs(right_eye_frame, right_keypoints)
                    if self.can_play:
                        t3 = threading.Thread(target=self.sound_play_async, kwargs={'notif':True})
                        t3.start()
                        sleep(.5)
                        self.is_left_detected = True
                        self.can_play = False

                right_eye_frame = np.require(right_eye_frame, np.uint8, 'C')
                self.display_image(right_eye_frame, window='right')

            if left_eye_frame is not None:
                if self.leftEyeCheckbox.isChecked():
                    left_eye_threshold = self.leftEyeThreshold.value()
                    left_keypoints, self.previous_left_keypoints, self.previous_left_blob_area = self.get_keypoints(
                        left_eye_frame, left_eye_frame_gray, left_eye_threshold,
                        previous_area=self.previous_left_blob_area,
                        previous_keypoint=self.previous_left_keypoints)
                    process.draw_blobs(left_eye_frame, left_keypoints)
                    if self.right_can_play:
                        t2 = threading.Thread(target=self.sound_play_async, kwargs={'notif':True},name= 'notif')
                        t2.start()
                        sleep(.5)
                        self.is_right_detected = True
                        self.right_can_play = False
                left_eye_frame = np.require(left_eye_frame, np.uint8, 'C')
                self.display_image(left_eye_frame, window='left')
            msg = ''
            if self.is_left_detected:
                msg = 'left eye'
            if self.is_right_detected:
                msg = 'right eye'
            if self.is_right_detected and self.is_left_detected:
                msg = 'left and right eyes'
            if msg:
                msg = msg + ' detected'
                t1 = threading.Thread(target=self.sound_play_async, kwargs={'dis': distance, 'msg': msg})
                t1.start()
                sleep(.5)
            self.is_right_detected = False
            self.is_left_detected = False

        if self.pupilsCheckbox.isChecked():  # draws keypoints on pupils on main window
            self.display_image(base_image)

    def sound_play_async(self, msg=None, notif=None, sleep_time=0, say_distance=True, dis='0'):
            if sleep_time == 14:
                sleep_time = 15
            sleep(sleep_time)
            if not notif:
                self.engine.say(msg if sleep_time == 0 else '{} in {} seconds'.format(msg, sleep_time))
                self.engine.runAndWait()
                if say_distance:
                    sleep(0.2)
                    self.engine.say('distance between webcam and you is about')
                    self.engine.say(dis)
                    self.engine.say('centimeters')
                    self.engine.runAndWait()
                if sleep_time < 8:
                    self.sound_play_async(msg, notif, sleep_time + 7, say_distance=False)
            else:
                beep(sound=1)



    def get_keypoints(self, frame, frame_gray, threshold, previous_keypoint, previous_area):

        keypoints = process.process_eye(frame_gray, threshold, self.detector,
                                        prevArea=previous_area)
        if keypoints:
            previous_keypoint = keypoints
            previous_area = keypoints[0].size
        else:
            keypoints = previous_keypoint
        return keypoints, previous_keypoint, previous_area

    def display_image(self, img, window='main'):
        # Makes OpenCV images displayable on PyQT, displays them
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:  # RGBA
                qformat = QImage.Format_RGBA8888
            else:  # RGB
                qformat = QImage.Format_RGB888

        out_image = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)  # BGR to RGB
        out_image = out_image.rgbSwapped()
        if window == 'main':  # main window
            self.baseImage.setPixmap(QPixmap.fromImage(out_image))
            self.baseImage.setScaledContents(True)
        if window == 'left':  # left eye window
            self.leftEyeBox.setPixmap(QPixmap.fromImage(out_image))
            self.leftEyeBox.setScaledContents(True)
        if window == 'right':  # right eye window
            self.rightEyeBox.setPixmap(QPixmap.fromImage(out_image))
            self.rightEyeBox.setScaledContents(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.setWindowTitle("Eye gaze Detection")
    window.show()
    sys.exit(app.exec_())
