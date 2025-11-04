import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logs

from deepface import DeepFace
import cv2
import datetime
import pandas as pd
import logging
import sys
import contextlib

# Suppress DeepFace logs
logging.getLogger("deepface").setLevel(logging.ERROR)

@contextlib.contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

# ✅ Use your actual dataset folder here
db_path = "D:/new_face_attendance/dataset"
log_path = "D:/new_face_attendance/attendance/attendance.csv"
os.makedirs(os.path.dirname(log_path), exist_ok=True)

# Load attendance log
if os.path.exists(log_path):
    df = pd.read_csv(log_path)
else:
    df = pd.DataFrame(columns=["Name", "Timestamp"])

# Start webcam
video = cv2.VideoCapture(0)
if not video.isOpened():
    exit()

while True:
    ret, frame = video.read()
    if not ret or frame is None:
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    try:
        with suppress_stdout():
            faces = DeepFace.extract_faces(img_path=rgb_frame, detector_backend="opencv", enforce_detection=False)

        for face in faces:
            facial_area = face["facial_area"]
            x, y, w, h = facial_area["x"], facial_area["y"], facial_area["w"], facial_area["h"]
            face_crop = rgb_frame[y:y+h, x:x+w]

            name = "Unknown"
            with suppress_stdout():
                results = DeepFace.find(
                    img_path=face_crop,
                    db_path=db_path,
                    model_name="VGG-Face",
                    detector_backend="opencv",
                    distance_metric="cosine",
                    enforce_detection=False,
                    threshold=0.4,
                    silent=True
                )

            if len(results) > 0 and not results[0].empty:
                matched_file = results[0].iloc[0]["identity"]
                name = os.path.splitext(os.path.basename(matched_file))[0]

                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                df.loc[len(df)] = [name, timestamp]
                df.to_csv(log_path, index=False)
                print(f"✅ {name} marked present at {timestamp}")

            # Draw box and label
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            label = f"Known: {name}" if name != "Unknown" else "Unknown"
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    except:
        pass

    cv2.imshow("Face Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
