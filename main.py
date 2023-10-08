import cv2
import mediapipe as mp
from math import hypot
from pynput.keyboard import Key, Controller
import time

# Initialize the camera and hand detection
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
detect_hands = True
keyboard = Controller()

# Initialize detection and gesture variables
pause_start_time = None
pausing = False

next_start_time = None
v_next = False

previous_start_time = None
v_previous = False

volUP_start_time = None
v_volUP = False

volDO_start_time = None
v_VolDO = False

mute_star_time = None
v_mute = False

while True:
    # Capture a frame from the camera and process hand detection
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

    # Process gestures if hand landmarks are detected
    if lmList != []:
        x1, y1 = lmList[4][1], lmList[4][2] #Thumb
        x2, y2 = lmList[8][1], lmList[8][2] #Index
        x3, y3 = lmList[12][1], lmList[12][2] #Middle
        x4, y4 = lmList[16][1],lmList[16][2] #Ring
        x5, y5 = lmList[20][1],lmList[20][2] #Pinky

        cv2.circle(img, (x1, y1), 13, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 13, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x3, y3), 13, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x4, y4), 13, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x5, y5), 13, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

        length_volUP = hypot(x2 - x1, y2 - y1)
        length_volDO = hypot(x5 - x1, y5 - y1)
        length_pause = hypot(x3 - x2, y3 - y2)
        length_next = hypot(x3 - x1, y3 - y1)
        length_previous = hypot(x4 - x1, y4 - y1)
        length_mute = hypot(x4 - x3, y4 - y3)

        # Increase volume
        if length_volUP < 30:
            if not v_volUP:
                volUP_start_time = time.time()
                v_volUP = True
            else:
                elapsed_time = time.time() - volUP_start_time
                if elapsed_time >= 0.1:
                    keyboard.press(Key.media_volume_up)
                    keyboard.release(Key.media_volume_up)
                    v_volUP = False
        else:
            v_volUP = False

        # Decrease volume
        if length_volDO < 30:
            if not v_VolDO:
                volDO_start_time = time.time()
                v_VolDO = True
            else:
                elapsed_time = time.time() - volDO_start_time
                if elapsed_time >= 0.1:
                    keyboard.press(Key.media_volume_down)
                    keyboard.release(Key.media_volume_down)
                    v_VolDO = False
        else:
            v_VolDO = False

        # Pause control
        if length_pause < 25:
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

        # Next song
        if length_next < 30:
            if not v_next:
                next_start_time = time.time()
                v_next = True
            else:
                elapsed_time = time.time() - next_start_time
                if elapsed_time >= 1:
                    keyboard.press(Key.media_next)
                    keyboard.release(Key.media_next)
                    v_next = False
        else:
            v_next = False

        # Previous song
        if length_previous < 30:
            if not v_previous:
                previous_start_time = time.time()
                v_previous = True
            else:
                elapsed_time = time.time() - previous_start_time
                if elapsed_time >= 1:
                    keyboard.press(Key.media_previous)
                    keyboard.release(Key.media_previous)
                    v_previous = False
        else:
            v_previous = False

        # Mute
        if length_mute < 32:
            if not v_mute:
                mute_star_time = time.time()
                v_mute = True
            else:
                elapsed_time = time.time() - mute_star_time
                if elapsed_time >= 1:
                    keyboard.press(Key.media_volume_mute)
                    keyboard.release(Key.media_volume_mute)
                    v_mute = False
        else:
            v_mute = False

    # Resize the image and display it in a window
    img = cv2.resize(img, dsize=(640, 480))
    cv2.imshow('Image Camera', img)

    # Capture keyboard events
    key = cv2.waitKey(1) & 0xff

    if key == ord('d'):
        detect_hands = not detect_hands

    if key == ord(' '):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()



