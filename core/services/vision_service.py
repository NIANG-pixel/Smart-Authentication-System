import cv2
import numpy as np
import face_recognition
import time


class VisionService:

    @staticmethod
    def check_liveness():

        cap = cv2.VideoCapture(0)

        print("Regardez la caméra... (liveness check)")

        motion_score = 0
        last_frame = None

        start_time = time.time()

        while True:

            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if last_frame is None:
                last_frame = gray
                continue

            diff = cv2.absdiff(last_frame, gray)
            threshold = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

            motion_score = np.sum(threshold)

            cv2.imshow("Liveness Check", frame)

            last_frame = gray

            # Condition 1 : mouvement détecté
            if motion_score > 500000:
                print("Mouvement détecté")

            # Condition 2 : temps minimum
            if time.time() - start_time > 3:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        # validation simple
        return motion_score > 500000