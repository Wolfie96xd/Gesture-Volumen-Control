# Gesture Volumen Control
This is my first publication of a software made by me. It is mainly a way to control the volume of your device through manual gestures. At the moment it is somewhat rudimentary and I hope to be able to update it with better features.   You could say that it is my first contact with the world of computer vision.

## How it works
Firstly, based on the first hand that is detected, the structure or "**virtual skeleton**" of the hand can be visualized and its connection nodes, which total 21 per hand, can be identified.

We will focus on the tips of the index, middle and thumb fingers. 
- When the index finger and thumb are joined together, the volume meter starts to increase (when it reaches 100, it starts again from 0).
- Pressing the index and middle finger together for approximately 3 seconds pauses the video or music.

### Requirements


### Dependencies/Packages
- Mediapipe
- CV2
- Math
- Numpy
- Time
- Pynput
- Pycaw
