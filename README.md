# VirtualMouse

Control the mouse pointer with your hand through a webcam. MediaPipe tracks
21 hand landmarks per frame, the index fingertip moves the cursor (with
smoothing so it doesn't jitter), and a pinch between the index and middle
fingers clicks.

Built in 2022 as an improved take on the classic OpenCV + MediaPipe virtual
mouse.

## How it works

- `cv2.VideoCapture` reads frames from the webcam (`0` is the built-in camera,
  `1` an external one).
- `mediapipe.solutions.hands` finds one hand and returns its landmarks.
- Fingertip coordinates are mapped from the camera frame to the screen size
  (via `screeninfo`) and smoothed between frames.
- `pynput` moves the pointer and sends clicks.

## Run it

```bash
pip install opencv-python mediapipe numpy pynput screeninfo
python MyVmouse.py
```

On macOS, give your terminal Camera and Accessibility permissions
(System Settings → Privacy & Security), otherwise the pointer won't move.

To build a standalone macOS app with py2app:

```bash
pip install py2app
python setup.py py2app
```
