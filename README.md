#VisionKeys — HackHarvard 2025

Repository: adityaraj457/VisionKeys
Event: HackHarvard 2025
Authors: Harry Du, Aditya Raj, Jose Feliz Cuevas
Tagline: VisionKeys — an eye and head-controlled typing interface designed to give everyone the power to communicate hands-free.

🚀 Overview

VisionKeys is a web-based eye and head gaze typing system that allows users to type on an on-screen keyboard through eye movement and blinks — no hands, no external hardware.
It combines MediaPipe’s Face Landmarker with custom gaze fusion algorithms and a real-time dwell selection system, all running directly in the browser.

🎯 Built for accessibility, affordability, and assistive innovation — VisionKeys empowers users with motor disabilities to communicate using just a webcam.

⭐ Key Features

👁️ Eye & Head Fusion Tracking – Stable and precise pointer control using both eye and head vectors.

💬 Dwell Typing – Select characters by holding gaze (configurable dwell time).

🫰 Blink Selection – Trigger selection with short, intentional blinks.

🧲 Key Magnetization – Cursor “snaps” to nearest key center to reduce errors.

🔊 Audio Feedback – Optional sound cues for visual confirmation.

🧠 9-Point Calibration System – Personalized accuracy stored locally.

💾 Client-Side Only – Everything runs in-browser; no data leaves your device.

🪞 Preview Overlay – Small live camera window showing gaze tracking in real time.

⚡ Lightweight – Powered by WebAssembly and WebGL for smooth performance.

🎯 Why VisionKeys

People with limited motor control or temporary hand injuries often face barriers when using traditional input devices.
VisionKeys bridges that gap using only a laptop webcam — transforming any device into a powerful assistive communication tool.

At HackHarvard 2025, VisionKeys showcases how accessible AI and computer vision can democratize technology for everyone.

🧰 Tech Stack

HTML / CSS / JavaScript (ES Modules)

MediaPipe Tasks Vision – FaceLandmarker (WASM + GPU)

WebAssembly / WebGL for real-time inference

LocalStorage for calibration persistence

Vanilla JS UI — no backend required

🧠 How to Run Locally

Clone the repository

git clone https://github.com/adityaraj457/VisionKeys.git
cd VisionKeys


Start a local development server
(needed because the FaceLandmarker WASM model can’t run from file://)

python -m http.server 8000
# or
npx http-server -p 8000


Open your browser

http://localhost:8000


Allow camera access and press c to calibrate.
Then, start typing with your gaze!

🎛️ Controls & Shortcuts
Key / Action	Function
c	-> Start 9-point calibration
x -> 	Reset calibration data
v ->	Toggle preview camera
t	-> Toggle tracking overlay
] / [	-> Adjust vertical offset
🔊 Button	Enable or disable sound

⚙️ Calibration & Fine-Tuning

Run c to begin calibration. Follow on-screen dots with your eyes.

Adjust vertical offset with ] or [ keys.

Modify key constants in JS for further control:

DWELL_MS → dwell duration (default 1000 ms)

GAZE_Y_LIFT_PX → vertical lift correction

BLINK_MIN_MS / BLINK_MAX_MS → blink sensitivity

Use v to hide preview if it overlaps with the keyboard.

🌐 Deploying to GitHub Pages

Commit and push your code to GitHub.

Go to: Settings → Pages → Source → Main Branch / Root.

GitHub will automatically host at
🔗 https://adityaraj457.github.io/VisionKeys/

🔐 Privacy & Security

VisionKeys processes all data locally — no cloud or API calls.

Camera feed never leaves the user’s device.

Calibration data is saved only to browser localStorage.

🧭 Vision & Social Impact

“Typing made possible — without hands.”

VisionKeys is designed to bring independence and dignity to users with limited mobility.
Its low-cost, open-source framework allows schools, clinics, and developers to adopt and improve upon the system easily.

Potential applications:

ALS & paralysis communication aids

Rehabilitation tools

Hands-free input for sterile or hazardous environments

🧱 Future Roadmap

🌎 Multilingual keyboard layouts

🤖 Local word prediction model integration

⚙️ Adaptive dwell time (AI-adjusted per user)

☁️ Optional cloud sync for profiles

🧪 Collaboration with accessibility researchers

👤 Authors
Name	GitHub / Profile
Harry Du	-----------

Aditya Raj	@adityaraj457

Jose Feliz Cuevas	---------

🧾 Quick Summary
git clone https://github.com/Harry-Du1/Eye-tracking-typer
cd VisionKeys
python -m http.server 8000
# Open http://localhost:8000
# Press 'c' to calibrate, 'v' to hide preview, and '🔊' for sound.
