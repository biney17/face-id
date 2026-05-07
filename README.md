<div align="center">

# 🔐 Face ID — Facial Recognition Door System

**AI-powered access control using DeepFace & Arduino**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![DeepFace](https://img.shields.io/badge/DeepFace-VGG--Face-FF6B6B?style=flat)](https://github.com/serengil/deepface)
[![Arduino](https://img.shields.io/badge/Arduino-Compatible-00979D?style=flat&logo=arduino&logoColor=white)](https://arduino.cc)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

A real-time facial recognition system that controls a physical door lock via servo motor using an Arduino board.

</div>

---

## ✨ Features

- 🎥 Real-time face detection and recognition via webcam
- 🧠 AI identification powered by DeepFace (VGG-Face model)
- 🔒 Servo motor door control via Arduino Serial
- 👤 In-app face registration (no coding required)
- ⚙️ Configurable unlock duration and recognition sensitivity

---

## 📂 Project Structure

```
face_id_project/
├── face_id.py               # Main application
├── requirements.txt         # Python dependencies
├── known_faces/             # Authorized face images (auto-created)
└── arduino_servo/
    └── arduino_servo.ino    # Arduino firmware (C++)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Arduino IDE
- A USB webcam
- Arduino Uno + servo motor

---

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/face-id.git
cd face-id
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install tf-keras
```

> ⏳ `deepface` may take 5–10 minutes to install.  
> 🤖 On first launch, DeepFace downloads AI model weights (~500 MB) — this is normal.

### 3. Flash Arduino Firmware

1. Open `arduino_servo/arduino_servo.ino` in **Arduino IDE**
2. Select your board (e.g., Arduino Uno) and port (e.g., COM3)
3. Click **Upload**

### 4. Configure

Open `face_id.py` and update the settings at the top:

```python
SERIAL_PORT       = "COM3"   # Your Arduino COM port (check Device Manager)
DOOR_OPEN_SECONDS = 15       # Seconds the door stays unlocked
```

### 5. Run

```bash
python face_id.py
```

---

## 👤 Registering Faces

**Method 1 — In-App (Recommended)**

| Step | Action |
|------|--------|
| 1 | Run the program |
| 2 | Press `R` while the camera window is active |
| 3 | Type the person's name in the terminal → press **Enter** |
| 4 | Press `SPACE` 5 times to capture face photos |
| ✅ | Person is now registered and recognized automatically |

**Method 2 — Manual**

Place a clear, front-facing photo in the `known_faces/` folder and name it after the person:

```
known_faces/
├── ahmed.jpg
└── sara.png
```

Restart the program to apply changes.

---

## 🎮 Keyboard Controls

| Key | Action |
|-----|--------|
| `R` | Register a new face |
| `SPACE` | Capture photo (during registration) |
| `ESC` | Cancel registration |
| `Q` | Quit the program |

---

## 🔌 Hardware Wiring

### Arduino Uno — Servo Motor

| Servo Wire | Arduino Pin |
|------------|-------------|
| Red (VCC) | 5V |
| Brown / Black (GND) | GND |
| Orange / White (Signal) | Pin 9 |

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| No camera found | Change `CAMERA_INDEX = 1` in `face_id.py` |
| Serial connection failed | Verify COM port in **Device Manager** |
| Face not recognized | Use a well-lit, front-facing photo in `known_faces/` |
| Recognition too slow | Increase `RECOGNITION_INTERVAL = 15` in `face_id.py` |
| Program freezes on startup | Normal — DeepFace is downloading model weights. Wait 2–3 min |
| Installation error | Run `pip install deepface tf-keras` manually |

---

## 📦 Dependencies

| Library | Purpose |
|---------|---------|
| `deepface` | Face recognition (VGG-Face model) |
| `opencv-python` | Camera capture & image processing |
| `tf-keras` | DeepFace backend |
| `pyserial` | Arduino serial communication |

Install all at once:

```bash
pip install -r requirements.txt
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Built with ❤️ by [Isra Brahimi](https://github.com/biney17)

</div>