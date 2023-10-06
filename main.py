import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
from pynput.keyboard import Key, Controller
import time

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volbar = 400
volper = 0
volMin, volMax = volume.GetVolumeRange()[:2]
keyboard = Controller()
detect_hands = True
pause_start_time = None
pausing = False

click_start_time = None
clicking = False

while True:
    if detect_hands:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(imgRGB)

        lmList = []
        if results.multi_hand_landmarks:
            for handlandmark in results.multi_hand_landmarks:
                for id, lm in enumerate(handlandmark.landmark):
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

    if lmList != []:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        x3, y3 = lmList[12][1], lmList[12][2]

        cv2.circle(img, (x1, y1), 13, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 13, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x3, y3), 13, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

        length_index = hypot(x2 - x1, y2 - y1)
        length_middle = hypot(x3 - x2, y3 - y2)

        if length_index < 30:
            if not clicking:
                click_start_time = time.time()
                clicking = True
            else:
                elapsed_time = time.time() - click_start_time
                if elapsed_time >= 3:
                    volume.SetMasterVolumeLevel(vol, None)
                    clicking = False
                else:
                    vol = np.interp(elapsed_time, [0, 3], [volMin, volMax])
                    volume.SetMasterVolumeLevel(vol, None)
                    volbar = np.interp(elapsed_time, [0, 3], [400, 150])
                    volper = np.interp(elapsed_time, [0, 3], [0, 100])
        else:
            clicking = False

        # Control de pausa
        if length_middle < 25:
            if not pausing:
                pause_start_time = time.time()
                pausing = True
            else:
                elapsed_time = time.time() - pause_start_time
                if elapsed_time >= 1:
                    keyboard.press(Key.media_play_pause)
                    keyboard.release(Key.media_play_pause)
                    pausing = False
        else:
            pausing = False

        cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 4)
        cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, f"{int(volper)}%", (10, 40), cv2.FONT_ITALIC, 1, (0, 255, 98), 3)

    img = cv2.resize(img, dsize=(640, 480))
    cv2.imshow('Image Camera', img)

    key = cv2.waitKey(1) & 0xff

    if key == ord('d'):
        detect_hands = not detect_hands

    if key == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()


