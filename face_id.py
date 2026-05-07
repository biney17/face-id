"""
========================================
  FACE ID - Facial Recognition System
  Fresh Start - Clean Code
  Compatible: Windows (Arduino Serial)
  Author: Isra Nour El Yakine Brahimi
========================================

USAGE:
  - Press [R] to register a new face
  - Press [Q] to quit the program
"""

import cv2
import os
import sys
import time
from deepface import DeepFace

# ─────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────

SERIAL_PORT = "COM4"
SERIAL_BAUD = 9600
DOOR_OPEN_SECONDS = 15
KNOWN_FACES_DIR = "known_faces"
CAMERA_INDEX = 0
RECOGNITION_INTERVAL = 5  # Check every 5 frames

# Serial connection
serial_conn = None

try:
    import serial
    serial_conn = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1)
    time.sleep(2)
    print(f"[OK] Serial connected on {SERIAL_PORT}")
except Exception as e:
    print(f"[WARNING] Serial not available: {e}")


# ─────────────────────────────────────────────
#  DOOR CONTROL
# ─────────────────────────────────────────────

def open_door():
    """Open door via Arduino"""
    if serial_conn:
        try:
            serial_conn.write(b'O')
            serial_conn.flush()
            print("[DOOR] 🔓 Opening...")
        except Exception as e:
            print(f"[ERROR] Serial failed: {e}")


def close_door():
    """Close door via Arduino"""
    if serial_conn:
        try:
            serial_conn.write(b'C')
            serial_conn.flush()
            print("[DOOR] 🔒 Closing...")
        except Exception as e:
            print(f"[ERROR] Serial failed: {e}")


# ─────────────────────────────────────────────
#  FACE RECOGNITION
# ─────────────────────────────────────────────

def extract_name(filename):
    """Extract name from filename (ahmed_1.jpg -> ahmed)"""
    base = os.path.splitext(filename)[0]
    parts = base.rsplit('_', 1)
    return parts[0] if len(parts) > 1 and parts[1].isdigit() else base


def load_known_faces():
    """Load list of registered people"""
    if not os.path.exists(KNOWN_FACES_DIR):
        os.makedirs(KNOWN_FACES_DIR)
        return []

    people = []
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            name = extract_name(filename)
            if name not in people:
                people.append(name)
                print(f"[OK] Loaded: {name}")
    
    return people


def recognize_face(frame):
    """
    Recognize a face in the frame
    Returns: (name, confidence_score)
    """
    try:
        tmp_path = "tmp_face.jpg"
        cv2.imwrite(tmp_path, frame)

        # Search for face in database
        results = DeepFace.find(
            img_path=tmp_path,
            db_path=KNOWN_FACES_DIR,
            model_name="VGG-Face",
            enforce_detection=False,
            silent=True
        )

        # No results = Unknown face
        if not results or len(results) == 0:
            return "Unknown", 0.0
        
        if results[0].empty:
            return "Unknown", 0.0

        # Get best match
        best = results[0].iloc[0]
        
        # Get confidence score (higher = better match)
        confidence = best.get('confidence', 0.0)
        
        # Get distance (lower = better match)
        distance = best.get('distance', 1.0)
        
        # VGG-Face: distance < 0.4 is usually a good match
        if distance < 0.4:
            identity_path = best["identity"]
            name = extract_name(os.path.basename(identity_path))
            return name, confidence
        
        return "Unknown", 0.0

    except Exception as e:
        print(f"[ERROR] Recognition failed: {e}")
        return "Unknown", 0.0


# ─────────────────────────────────────────────
#  FACE REGISTRATION
# ─────────────────────────────────────────────

def register_face(camera):
    """Register a new person with 5 photos"""
    
    name = input("\n[REGISTER] Enter person's name: ").strip()
    if not name:
        print("[ERROR] Name cannot be empty!")
        return

    print(f"[INFO] Taking 5 photos of {name}")
    print("[INFO] SPACE = capture | ESC = cancel")

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    count = 0
    while count < 5:
        ret, frame = camera.read()
        if not ret:
            break

        # Draw instructions
        cv2.putText(frame, f"Register: {name}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, f"Photo {count+1}/5", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # Detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.1, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Face Registration", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC
            print("[INFO] Registration cancelled")
            cv2.destroyWindow("Face Registration")
            return
        
        elif key == 32:  # SPACE
            if len(faces) > 0:
                path = os.path.join(KNOWN_FACES_DIR, f"{name}_{count+1}.jpg")
                cv2.imwrite(path, frame)
                print(f"[OK] Photo {count+1} saved")
                count += 1
            else:
                print("[WARNING] No face detected!")

    cv2.destroyWindow("Face Registration")

    # Clear cache so DeepFace rebuilds
    cache_file = os.path.join(KNOWN_FACES_DIR, "representations_vgg_face.pkl")
    if os.path.exists(cache_file):
        os.remove(cache_file)

    print(f"[OK] {name} registered successfully! ✅")


# ─────────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────────

def main():
    print("\n" + "="*50)
    print("  FACE ID - Facial Recognition System")
    print("="*50)
    print("  [R] = Register face")
    print("  [Q] = Quit")
    print("="*50 + "\n")

    # Load registered people
    load_known_faces()

    # Open camera
    camera = cv2.VideoCapture(CAMERA_INDEX)
    if not camera.isOpened():
        print("[ERROR] Cannot open camera!")
        sys.exit(1)

    # Variables
    door_open = False
    door_open_time = 0
    last_person = ""
    frame_count = 0
    display_name = "..."
    display_conf = 0.0

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    print("[INFO] Camera started. Press [Q] to quit, [R] to register.\n")

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        frame_count += 1
        
        # Detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.1, 5, minSize=(80, 80))

        # Recognize every N frames
        if frame_count % RECOGNITION_INTERVAL == 0 and len(faces) > 0:
            display_name, display_conf = recognize_face(frame)
            
            if display_name != "Unknown":
                print(f"[DETECTED] {display_name} (confidence: {display_conf:.3f})")
                
                if display_name != last_person or not door_open:
                    open_door()
                    door_open = True
                    door_open_time = time.time()
                    last_person = display_name
            else:
                # ⚠️ UNKNOWN PERSON DETECTED
                if door_open:
                    print(f"[ALERT] 🚨 Unknown person detected! Closing door immediately!")
                    close_door()
                    door_open = False
                    last_person = ""
                else:
                    last_person = ""

        # Draw face rectangles
        for (x, y, w, h) in faces:
            if display_name != "Unknown":
                color = (0, 255, 0)  # Green for match
                text = f"{display_name}"
            else:
                color = (0, 0, 255)  # Red for unknown
                text = "Unknown"
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.rectangle(frame, (x, y+h-30), (x+w, y+h), color, cv2.FILLED)
            cv2.putText(frame, text, (x+5, y+h-8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # Auto-close door after 15 seconds
        if door_open and (time.time() - door_open_time) > DOOR_OPEN_SECONDS:
            close_door()
            door_open = False
            last_person = ""
            display_name = "..."

        # Draw status
        status = "🔓 OPEN" if door_open else "🔒 CLOSED"
        status_color = (0, 255, 0) if door_open else (0, 0, 255)
        cv2.putText(frame, f"Door: {status}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        
        cv2.putText(frame, "[R] Register  [Q] Quit", (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        # Show frame
        cv2.imshow("Face ID System", frame)

        # Handle keyboard
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("[INFO] Exiting...")
            break
        elif key == ord('r'):
            register_face(camera)
            load_known_faces()

    # Cleanup
    camera.release()
    cv2.destroyAllWindows()
    
    if os.path.exists("tmp_face.jpg"):
        os.remove("tmp_face.jpg")
    
    if serial_conn:
        serial_conn.close()

    print("[INFO] Program closed ✅\n")


if __name__ == "__main__":
    main()