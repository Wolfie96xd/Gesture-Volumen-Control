# Hand Gesture Media Control
This is my first publication of a software made by me. It is mainly a way to control the media of your device through manual gestures. At the moment it is somewhat rudimentary and I hope to be able to update it with better features.   You could say that it is my first contact with the world of computer vision.

## How it works
Firstly, based on the first hand that is detected, the structure or "**virtual skeleton**" of the hand can be visualized and its connection nodes, which total 21 per hand, can be identified.

We will focus on the tips of your fingers following the next instructions: 

- **Stop/Play**: INDEX + MIDDLE 
- **Volume UP**: INDEX + THUMB
- **Volume Down**: PINKY + THUMB
- **Next**: MIDDLE + THUMB
- **Previous**: RING + THUMB
- **Mute**: MIDDLE + RING


### Dependencies/Packages
- Mediapipe
- CV2
- Math
- Time
- Pynput
