import cv2
import mediapipe as mp
import numpy as np
import time
import os
import urllib.request
import pyautogui
from collections import deque

# ------------------- WORD LIST & AUTOCOMPLETE -------------------
WORDS_FILE = "words.txt"
if not os.path.exists(WORDS_FILE):
    print("Downloading word list...")
    url = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
    urllib.request.urlretrieve(url, WORDS_FILE)
    print("Download complete.")

with open(WORDS_FILE, 'r') as f:
    words = [w.strip().upper() for w in f.readlines()]
words.sort()


def get_suggestions(prefix, max_suggestions=10):
    import bisect
    prefix = prefix.upper()
    i = bisect.bisect_left(words, prefix)
    suggestions = []
    while i < len(words) and words[i].startswith(prefix) and len(suggestions) < max_suggestions:
        suggestions.append(words[i])
        i += 1
    return suggestions


# ------------------- VIRTUAL KEYBOARD SETUP -------------------
KEYS = [
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    list("ZXCVBNM")
]
SPECIAL_KEYS = ["SPACE", "BKSP", "ENTER"]

# Simple keyboard mapping
keyboard_positions = {}
start_x, start_y = 100, 300
key_w, key_h = 60, 60
gap = 10
for row_idx, row in enumerate(KEYS):
    for col_idx, key in enumerate(row):
        keyboard_positions[key] = (
            start_x + col_idx*(key_w+gap), start_y + row_idx*(key_h+gap), key_w, key_h)
# Special keys
keyboard_positions["SPACE"] = (
    start_x, start_y + 3*(key_h+gap), 5*key_w + 4*gap, key_h)
keyboard_positions["BKSP"] = (
    start_x + 6*(key_w+gap), start_y + 2*(key_h+gap), 4*key_w+3*gap, key_h)
keyboard_positions["ENTER"] = (
    start_x + 5*(key_w+gap), start_y + 3*(key_h+gap), 3*key_w+2*gap, key_h)

# ------------------- MEDIAPIPE FACE & EYE DETECTION -------------------
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(max_num_faces=1, refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

# Eye landmarks (iris)
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

# Blink detection params
BLINK_RATIO_THRESHOLD = 0.25
blink_buffer = deque(maxlen=5)

# ------------------- HELPER FUNCTIONS -------------------


def eye_aspect_ratio(landmarks, upper_idx, lower_idx):
    top = np.mean([(landmarks[i].x, landmarks[i].y)
                  for i in upper_idx], axis=0)
    bottom = np.mean([(landmarks[i].x, landmarks[i].y)
                     for i in lower_idx], axis=0)
    return abs(top[1]-bottom[1])


def get_eye_center(landmarks, iris_idx):
    points = np.array([[landmarks[i].x, landmarks[i].y] for i in iris_idx])
    return np.mean(points, axis=0)


def map_to_screen(eye_pos, frame_shape):
    # eye_pos normalized to frame (0-1), map to screen
    screen_w, screen_h = pyautogui.size()
    x = int(eye_pos[0]*screen_w)
    y = int(eye_pos[1]*screen_h)
    return x, y


def find_key(x, y):
    for key, (kx, ky, kw, kh) in keyboard_positions.items():
        if kx <= x <= kx+kw and ky <= y <= ky+kh:
            return key
    return None


# ------------------- MAIN LOOP -------------------
cap = cv2.VideoCapture(0)
selected_key = None
dwell_start = None
DWELL_TIME = 0.6  # seconds

typed_text = ""
current_suggestions = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    screen_w, screen_h = pyautogui.size()

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        # Eye centers
        left_eye = get_eye_center(landmarks, LEFT_IRIS)
        right_eye = get_eye_center(landmarks, RIGHT_IRIS)
        eye_center = ((left_eye+right_eye)/2)

        # Map to screen coordinates
        cursor_x, cursor_y = map_to_screen(eye_center, frame.shape)
        pyautogui.moveTo(cursor_x, cursor_y)

        # Blink detection (simple vertical distance of eyelids)
        left_ratio = eye_aspect_ratio(
            landmarks, [386, 387, 388], [374, 373, 390])
        right_ratio = eye_aspect_ratio(
            landmarks, [159, 160, 161], [145, 144, 163])
        blink = (left_ratio+right_ratio)/2 < BLINK_RATIO_THRESHOLD
        blink_buffer.append(blink)
        # require 3 frames for stable blink
        blink_detected = sum(blink_buffer) > 3

        # Dwell-based selection
        key_under_cursor = find_key(cursor_x, cursor_y)
        if key_under_cursor != selected_key:
            selected_key = key_under_cursor
            dwell_start = time.time()
        else:
            if key_under_cursor and time.time() - dwell_start >= DWELL_TIME and blink_detected:
                if key_under_cursor == "SPACE":
                    typed_text += " "
                elif key_under_cursor == "BKSP":
                    typed_text = typed_text[:-1]
                elif key_under_cursor == "ENTER":
                    typed_text += "\n"
                else:
                    typed_text += key_under_cursor
                dwell_start = time.time()  # reset dwell
                # Update suggestions
                current_suggestions = get_suggestions(
                    typed_text.split()[-1] if typed_text.split() else "")

        # Draw virtual keyboard and highlight key
        for key, (kx, ky, kw, kh) in keyboard_positions.items():
            color = (0, 255, 0) if key == selected_key else (255, 255, 255)
            cv2.rectangle(frame, (kx, ky), (kx+kw, ky+kh), color, 2)
            cv2.putText(frame, key, (kx+5, ky+int(kw/2)+5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        # Display typed text
        cv2.rectangle(frame, (50, 50), (screen_w-50, 100), (50, 50, 50), -1)
        cv2.putText(frame, typed_text, (60, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Display suggestions
        for i, sugg in enumerate(current_suggestions):
            cv2.putText(frame, sugg, (50, 120+30*i),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Eye-Control Keyboard", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
