from naoqi import ALProxy
import time
import os
import scp
import sys
import Robot
import RobotGlobals
import Robot_Speech
from PIL import Image
import paramiko
from scp import SCPClient

paramiko.util.log_to_file("filename.log")
res_wait_time = 0.1
user = "nao"
password = "nao"
max_failed = 20

# def createSSHClient(server, user, password):
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     client.connect(server, username=user, password=password, look_for_keys=False, timeout=60)
#     return client


def main():
    robot = Robot.Robot()

    # client = createSSHClient(robot.IP, user, password)
    # client = SCPClient(ssh.get_transport())
    # Set Up
    # client = scp.SCPClient(host=robot.IP, user=user, password=password)

    # Start Main Loop
    robot.say("Hello! I am nao robot and I will try to detect your emotions!")

    # record_data(robot, client)

    crt_failed = 0
    while (crt_failed < max_failed):
        save_image(robot)
        emotion = get_processed_response()
        if emotion == "None" or emotion is None:
            robot.say("Sorry. I dont see any face.")
            crt_failed += 1

            # robot.say("So far, I did not see any face in {} times.".format(crt_failed))
            # robot.say("If I can not see any face in {} times, I will stop work.".format(max_failed))
        else:
            crt_failed = 0
            robot.say("Wow. I found a {} face".format(emotion))
        print(crt_failed)
        time.sleep(1)
    robot.say("Thanks! Bye!")


def save_image(robot):
    while True:
        nao_img = robot.get_image()
        if nao_img is not None:
            imageWidth = nao_img[0]
            imageHeight = nao_img[1]
            array = nao_img[6]

            # Create a PIL Image from our pixel array.
            im = Image.frombytes("RGB", (imageWidth, imageHeight), array)
            while os.path.exists("./data/emotion.png"):
                time.sleep(res_wait_time)
            im.save("./data/emotion.png", "PNG")
            print("image saved")
            break


def get_processed_response():

    # Get first file and open
    while not os.path.exists("./data/emotion.txt"):
        time.sleep(res_wait_time)
    emotion_file = open("./data/emotion.txt", "r")

    # Read data
    emotion = emotion_file.readlines()[0]
    emotion_file.close()
    # Delete Processed Data
    os.remove("./data/emotion.txt")
    # except:
    #     return None
    print("txt removed")
    return emotion


def end_program():
    file = open(RobotGlobals.RAW_DIR + "end.txt", "w")
    file.close()


if __name__ == "__main__":
    main()
