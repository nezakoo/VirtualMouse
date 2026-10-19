# VirtualMouse

Control the mouse pointer with your hand through a webcam. MediaPipe tracks
21 hand landmarks per frame and the script maps finger gestures to mouse
actions.

## Gestures

| Fingers up | Action |
|---|---|
| Index only | Move the pointer |
| Index + middle | Left click |
| Index + middle, held close together | Double click |
| Index + middle + ring | Right click |
| All four fingers | Scroll in any direction |
| Middle only | Quit |

Press `q` in the webcam window to quit as well.

Built in 2022 as an improved take on the classic OpenCV + MediaPipe virtual
mouse.

## How it works

- `cv2.VideoCapture` reads frames from the webcam (`0` is the built-in camera,
  `1` an external one).
- `mediapipe.solutions.hands` finds one hand and returns its landmarks.
- The index fingertip is mapped from the camera frame to the screen size
  (via `screeninfo`).
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
