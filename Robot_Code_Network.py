from EmotionProcessing import EmotionDetectionEngine
import time
import os
import shutil

def main():
    emotion_model = EmotionDetectionEngine()

    print("Finished Opening Models")
    cnt = 1
    while True:
        while not os.path.exists("./data/emotion.png"):
            time.sleep(0.05)
        ret = emotion_model.detect_emotion("./data/emotion.png")

        # if ret is not None:
        ret = "None" if ret is None else ret
        while os.path.exists("./data/emotion.txt"):
            time.sleep(0.05)
        file_out = open("./data/emotion.txt", "w")

        file_out.write(ret)
        file_out.close()
        print(time.time())
        time.sleep(0.7)


if __name__ == "__main__":
    main()
