import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)  # Use the default webcam
def detect_gesture(hand_landmarks):
    finger_tips = [4, 8, 12, 16, 20]  # Thumb to Pinky
    fingers = []

    for tip in finger_tips:
        x, y = hand_landmarks.landmark[tip].x, hand_landmarks.landmark[tip].y
        x_base, y_base = hand_landmarks.landmark[tip - 2].x, hand_landmarks.landmark[tip - 2].y
        if y < y_base:
            fingers.append(1)
        else:
            fingers.append(0)

    if fingers == [1, 0, 0, 0, 0]:  # Open palm
        return "Play"
    elif fingers == [0, 0, 0, 0, 0]:  # Fist
        return "Pause"
    elif fingers == [0, 1, 1, 0, 0]:  # Two fingers (index and middle)
        return "Volume Up"
    elif fingers == [0, 0, 0, 1, 1]:  # Ring and pinky fingers
        return "Volume Down"
    elif fingers == [0, 0, 0, 0, 1]:  # Pinky only
        return "Next Video"
    elif fingers == [1, 1, 1, 1, 0]:  # All except pinky
        return "Previous Video"
    else:
        return None
    
    cooldown = 0
cooldown = 0  # initial cooldown timestamp
cooldown_time = 2  # 2 seconds cooldown duration


#cooldown_time = 1  # Time in seconds to prevent repeated actions

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            gesture = detect_gesture(hand_landmarks)
            if gesture and time.time() - cooldown > cooldown_time:
                cooldown = time.time()
                if gesture == "Play":
                    pyautogui.press('space')
                elif gesture == "Pause":
                    pyautogui.press('space')
                elif gesture == "Volume Up":
                    pyautogui.press('up')
                elif gesture == "Volume Down":
                    pyautogui.press('down')
                elif gesture == "Next Video":
                    pyautogui.press('nexttrack')
                elif gesture == "Previous Video":
                    pyautogui.press('prevtrack')

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('YouTube Gesture Controller', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()