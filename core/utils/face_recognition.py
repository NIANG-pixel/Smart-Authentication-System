    @staticmethod
    def verify_face(reference_image_path):

        known_image = face_recognition.load_image_file(reference_image_path)
        known_encoding = face_recognition.face_encodings(known_image)[0]

        cap = cv2.VideoCapture(0)

        print("Capture visage...")

        ret, frame = cap.read()

        cap.release()
        cv2.destroyAllWindows()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        encodings = face_recognition.face_encodings(rgb)

        if len(encodings) == 0:
            return False

        result = face_recognition.compare_faces(
            [known_encoding],
            encodings[0]
        )[0]

        return result