from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
import os

class EmotionDetectionEngine:
    def __init__(self):
        self.face_model_path = 'model/haarcascade_frontalface_default.xml'
        self.emotion_model_path = 'model/_mini_XCEPTION.102-0.66.hdf5'
        self.cnt = 1
        # hyper-parameters for bounding boxes shape
        # loading models
        try:
            self.face_detection = cv2.CascadeClassifier(self.face_model_path)
            self.emotion_classifier = load_model(self.emotion_model_path, compile=False)
        except:
            print("Can not load Model files.")
            exit(0)
        self.EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

    def detect_emotion(self, file):
        frame = cv2.imread(file)
        #reading the frame
        if frame is None:
            return None
        os.remove(file)
        frame = imutils.resize(frame,width=300)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_detection.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)

        if len(faces) > 0:
            faces = sorted(faces, reverse=True,
            key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = faces
            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            preds = self.emotion_classifier.predict(roi)[0]
            emotion_probability = np.max(preds)
            label = self.EMOTIONS[preds.argmax()]
            frame = cv2.putText(frame, label, (fX, fY), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 2, cv2.LINE_AA)
            frame = cv2.rectangle(frame, (fX, fY), (fX+fW, fY+fH), (0, 0, 255), 1)
            cv2.imwrite("./test/{}.png".format(self.cnt), frame)
            self.cnt += 1
            return label
        cv2.imwrite("./test/{}.png".format(self.cnt), frame)
        self.cnt += 1
        return None

