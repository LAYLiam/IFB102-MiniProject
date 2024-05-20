# [Main]
"""
    Main purpose:
        Main program loop, open camera
        check movement, if then check if face,
        if then alert.

        Movement checking handled by movement.py
        Message sending handled by sendmessage.py 

    Conventions: 
        In this codebase, generally 
            subscript p (or _p) refers to previous,
            subscript c (or _c) refers to current.
"""

import cv2
import numpy as np
import time
import movement as mv
import sendmessage as sm

def main():
    """Open camera stream     
    """
    video = cv2.VideoCapture(0) #, cv2.CAP_V4L2) Raspberry Pi 4B requires this parameter
    cv2.namedWindow('stream', cv2.WINDOW_NORMAL)

    """Load first frame in, and set initial variables.
    :var frame_p: The past frame which a current (frame_c) will be compared with for movement.
    :var time_p: The last time a frame was stored as frame_p.
    :var last_seen: The last time a person was detected. 
    """
    _, frame_c = video.read()
    frame_p = np.asarray(frame_c).flatten()
    time_p = time.time() 
    last_seen = time.time()

    """Open video stream. 
    """
    while (True):
        _, frame_c = video.read()

        """Check for movement
        """
        if mv.Detection.check_frequency(time_p):
            detection = mv.Detection.check_movement(frame_p, frame_c)
            detected = detection is not None 

            """If a face is detected, and the waiting period, wherein any 
            additional movement detected would be classified as from the same interaction,
            a message will be sent via Twilio (new_alert()) with the face (detection).
            """ 
            # if detected: cv2.imshow('egg', detection) # <!> Face centering show uncomment <!> """
            if detected and sm.ProcessMessage.new_alert(last_seen): 
                            sm.ProcessMessage.new_message(detection)
            if detected: 
                  last_seen = time.time()
                  print(f"Person detected. \t\t{last_seen}")

            """Update previous frame and time to current, for comparison. 
            """
            time_p = time.time()
            frame_p = frame_c

        """Display camera stream. For headless RASPI setup this not required.
        """
        cv2.imshow('stream', frame_c)
        if cv2.waitKey(10) == ord('q'): break

    """Release video when done.
    """
    video.release()
    cv2.destroyAllWindows()


"""Program always starts from here. 
"""
if __name__ == "__main__":
    main()
