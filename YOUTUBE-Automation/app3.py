import cv2
import mediapipe as mp
import pyautogui
import time
import speech_recognition as sr
import math
import webbrowser

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize speech recognition
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Cooldown mechanisms
cooldown = 0
cooldown_time = 1  # Time in seconds to prevent repeated actions from gestures
cooldown_voice = 0
cooldown_time_voice = 2  # Time in seconds to prevent repeated voice commands

# Function to detect gestures
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
    elif fingers == [1, 0, 0, 0, 1]:  # Thumbs Up
        return "Like"
    elif fingers == [0, 0, 0, 0, 1] and hand_landmarks.landmark[4].y > hand_landmarks.landmark[8].y:  # Thumbs Down
        return "Dislike"
    else:
        return None

# Function to get finger angle
def get_finger_angle(hand_landmarks, tip, dip, pip, mcp):
    x_tip, y_tip = hand_landmarks.landmark[tip].x, hand_landmarks.landmark[tip].y
    x_dip, y_dip = hand_landmarks.landmark[dip].x, hand_landmarks.landmark[dip].y
    x_pip, y_pip = hand_landmarks.landmark[pip].x, hand_landmarks.landmark[pip].y
    x_mcp, y_mcp = hand_landmarks.landmark[mcp].x, hand_landmarks.landmark[mcp].y

    angle = math.degrees(math.atan2(y_dip - y_tip, x_dip - x_tip) - math.atan2(y_mcp - y_pip, x_mcp - x_pip))
    angle = abs(angle) % 360

    return angle

# Function to recognize voice commands
def recognize_voice():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        return command
    except sr.UnknownValueError:
        return None

# Function to open YouTube and search for a video
def open_youtube_and_search(query):
    webbrowser.open('https://www.youtube.com')
    time.sleep(5)  # Wait for the page to load
    pyautogui.click(1000, 100)  # Click on the search bar (adjust coordinates as needed)
    pyautogui.typewrite(query)
    pyautogui.press('enter')
    time.sleep(5)  # Wait for search results
    pyautogui.click(1000, 300)  # Click on the first video (adjust coordinates as needed)

# Function to skip ads
def skip_ads():
    try:
        # Locate the "Skip Ad" button and click it
        skip_ad_button = pyautogui.locateOnScreen('skip_ad_button.png', confidence=0.8)
        if skip_ad_button:
            pyautogui.click(skip_ad_button)
    except Exception as e:
        print(f"Error skipping ad: {e}")

# Main loop
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
                elif gesture == "Like":
                    pyautogui.press('l')
                elif gesture == "Dislike":
                    pyautogui.press('d')

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if time.time() - cooldown_voice > cooldown_time_voice:
        cooldown_voice = time.time()
        command = recognize_voice()
        if command:
            if "play" in command:
                pyautogui.press('space')
            elif "pause" in command:
                pyautogui.press('space')
            elif "volume up" in command:
                pyautogui.press('up')
            elif "volume down" in command:
                pyautogui.press('down')
            elif "next video" in command:
                pyautogui.press('nexttrack')
            elif "previous video" in command:
                pyautogui.press('prevtrack')
            elif "like" in command:
                pyautogui.press('l')
            elif "dislike" in command:
                pyautogui.press('d')
            elif "search" in command:
                open_youtube_and_search(command.replace("search", "").strip())
            elif "skip ad" in command:
                skip_ads()

    cv2.imshow('YouTube Gesture Controller', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()