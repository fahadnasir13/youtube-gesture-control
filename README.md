🎥 YouTube Gesture Controller

> Control YouTube with your hands — no clicks, no keyboard, just gestures.

**Tech Stack**: Python · OpenCV · MediaPipe · PyAutoGUI

---

## ✨ Overview

This project lets you control YouTube videos using **real-time hand gestures** detected via your webcam.  
No need for mouse or keyboard — just wave, pause, like, skip, and more using simple gestures.

---

## 🖐️ Supported Gestures

| Gesture          | Action          |
|------------------|-----------------|
| ✋ Open Palm      | Play / Pause    |
| ✊ Fist           | Mute / Unmute   |
| 👍 Thumbs Up      | Like Video      |
| 👎 Thumbs Down    | Dislike Video   |
| 👉 Swipe Right    | Next Video      |
| 👈 Swipe Left     | Previous Video  |
| 🖐️ Two Fingers Up | Increase Volume |
| ✌️ Two Fingers Down | Decrease Volume |

> _(You can customize gestures easily in code!)_

---

## 🛠 Tech Stack

- **Python 3.9+**
- **OpenCV** – For webcam input and image processing
- **MediaPipe** – Hand detection and tracking
- **PyAutoGUI** – Sends keyboard/mouse actions to browser
- **Time / Math / OS / NumPy** – Standard utilities

---

## 📁 Folder Structure

youtube-gesture-controller/
├── gesture_controller.py # Main script
├── gestures/ # Custom gesture definitions (if any)
├── utils/ # Hand tracking logic
├── requirements.txt
├── README.md
└── demo.gif # Optional demo preview



## 🚀 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/fahadnasir13/youtube-gesture-controller.git
cd youtube-gesture-controller

# 2. Install requirements
pip install -r requirements.txt

# 3. Run the app
python gesture_controller.py
Make sure a browser with YouTube is open and focused before using the gestures.


🧠 Future Ideas
Add custom gestures

Expand to Netflix, VLC, or other platforms

Add voice + gesture hybrid control

Gesture-based drawing / cursor movement

👤 Creator
Fahad Nasir
AI & Full Stack Innovator

GitHub: https://github.com/fahadnasir13

LinkedIn: https://linkedin.com/in/fahadnasir15

Portfolio: https://fahadnasir.macaly-app.com

📄 License
MIT License – Feel free to use, modify, and enhance.

🙌 Contributions
PRs welcome!
Feel free to fork, star, and contribute to this hands-free experience.
