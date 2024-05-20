# [Detect Movement]
"""
    Main purpose:
        Detect if there is movement, and detect if there is a face in that movement.
        If so then return the face, if not return None (because no face...).

    [1] <Source was used as a Python tutorial on how to use OpenCV generally>
    Alhamed. (2023). Face Detection on Raspberry Pi 4 using OpenCV and Camera Module. 
            Retrieved 20 May, 2024 from https://www.cytron.io/tutorial/face-detection-on-raspberry-pi4-using-opencv-and-camera-module
    [2] <Source was needed to figure out how to get training data onto Raspberry Pi 4B.
    Training data for Haar Cascades can be downloaded from GitHub and pointed to in program.>
    OpenCV-Python Tutorials. (2016). Face Detection using Haar Cascades. eastWillow. 
            Retrieved 13 May, 2024 from https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html#face-detection
"""

import cv2
import numpy as np
import time
from cv2 import data

"""Constants

:const CHECK_FREQUENCY: How frequently (seconds) program needs to check for movement.
:const MOVEMENT_THRESHOLD: The minimum euclidian distance between frames until considered movement.
"""
CHECK_FREQUENCY = 0.5
MOVEMENT_THRESHOLD = 3000

"""Handle detection for movement and face detection 
"""
class Detection:
    @staticmethod
    def check_frequency(time_p):
        """Check the time elapsed between last frame checked for a face.
        If it is more than the CHECK_FREQUENCY then it is time to check again.

        :param time_p: Previous time check.
        :return: True if time to check for face again, else false.
        """
        return (time.time() - time_p) > CHECK_FREQUENCY

    @staticmethod
    def haar_cascades(frame_c):
        """Uses Haar Cascades for person/face detection.

        :param frame_c: Current frame.
        :return: Sequence [x, y, w, h] for ROI occupied by a face, if no face then tuple().
        """
        face = cv2.CascadeClassifier(data.haarcascades + 'haarcascade_frontalface_default.xml')
        frame_c = cv2.cvtColor(frame_c, cv2.COLOR_RGB2GRAY)
        return face.detectMultiScale(frame_c, scaleFactor=1.1, minNeighbors=9)

    @staticmethod
    def draw_ROI_rectangle(frame_c, haar_cascade):
        """Draw box around face.

        :param frame_c: Current frame.
        :param haar_cascade: Sequence [x, y, w, h] for ROI occupied by a face. 
        :return: Updated frame with rectangle drawn.
        """
        if type(haar_cascade) is tuple: raise TypeError
        x, y, w, h = haar_cascade[0]
        return cv2.rectangle(frame_c, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    @staticmethod
    def isolate_ROI(frame_c, haar_cascade):
        """Get image of face from image.
        Given that the ROI is relative to the given data from the haar_cascade,
        this also doubles as a nifty face tracker! 
        <Idea>: You can take this, coupled with the above haar_cascades method and you'll
        have a stabilized video-stream with the face always at the center.  

        :param frame_c: Current frame.
        :param haar_cascade: Sequence [x, y, w, h] for ROI occupied by a face. 
        :return: Cropped image with face in center.
        """
        res = 256 # Resolution of cropped image 
        if type(haar_cascade) is tuple: raise TypeError
        x, y, w, h = haar_cascade[0]
        adj_c = np.float32([[x-w, y-h], [x+w*2, y-h], [x-w, y+h*2], [x+w*2, y+h*2]])
        map_c = np.float32([[0, 0], [res, 0], [0, res], [res, res]])
        M = cv2.getPerspectiveTransform(adj_c, map_c)
        return cv2.warpPerspective(frame_c, M, (res, res)) 

    @staticmethod
    def check_movement(frame_p, frame_c):
        """Check if there is movement between frames
        by calculating euclidian distances. ~Movement~ is classified by the distance
        value if it is greater than the MOVEMENT_THRESHOLD global constant.
        If there is, then check for a face using haar cascades method.
        If there is, then return a cropped image of the face.

        :param frame_c: Current frame.
        :param frame_p: Previous frame.
        :returns: Cropped image of the face if face exists, else None.
        """
        # Take image and turn into numpy matrix array
        frame_pf, frame_cf = np.asarray(frame_p).flatten(), np.asarray(frame_c).flatten()

        # If euclidian distance is greater than threshold, try haar cascades.
        if MOVEMENT_THRESHOLD < np.sqrt(np.sum(np.square(frame_pf - frame_cf))):
            haar_c = Detection.haar_cascades(frame_c)
            return None if type(haar_c) is tuple \
              else Detection.isolate_ROI(frame_c, haar_cascade=haar_c)
        
        # Not enough movement, possibly no-one at the door :(
        else: return None