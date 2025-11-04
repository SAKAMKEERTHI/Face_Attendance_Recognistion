import os
import cv2
import datetime
import pandas as pd
import logging
import sys
import contextlib
from deepface import DeepFace

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
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

db_path = "D:/new_face_attendance/dataset"
log_path = "D:/new_face_attendance/attendance/attendance.csv"
os.makedirs(os.path.dirname(log_path), exist_ok=True)

if os.path.exists(log_path):
    df = pd.read_csv(log_path)
else:
    df = pd.DataFrame(columns=["Name", "Timestamp"])

def process_frame(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_data = []

    try:
        with suppress_stdout():
            faces = DeepFace.extract_faces(img_path=rgb_frame, detector_backend="opencv", enforce_detection=False)

        print(f"🔍 Detected {len(faces)} face(s)")

        for face in faces:
            facial_area = face["facial_area"]
            x, y, w, h = facial_area["x"], facial_area["y"], facial_area["w"], facial_area["h"]
            face_crop = rgb_frame[y:y+h, x:x+w]

            name = "Unknown"
            status = "unknown"
            timestamp = ""

            try:
                with suppress_stdout():
                    results = DeepFace.find(
                        img_path=face_crop,
                        db_path=db_path,
                        model_name="Facenet",
                        detector_backend="opencv",
                        distance_metric="cosine",
                        enforce_detection=False,
                        threshold=0.6,
                        silent=True
                    )
                print(f"🔎 Matching result: {results[0] if len(results) > 0 else 'No result'}")
            except Exception as e:
                print(f"⚠️ DeepFace.find failed: {str(e)}")
                results = [pd.DataFrame()]

            if len(results) > 0 and not results[0].empty:
                matched_file = results[0].iloc[0]["identity"]
                name = os.path.splitext(os.path.basename(matched_file))[0]
                status = "known"
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                df.loc[len(df)] = [name, timestamp]
                df.to_csv(log_path, index=False)
                print(f"✅ {name} marked present at {timestamp}")
            else:
                print("❌ No match found")

            face_data.append({
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "name": name,
                "status": status,
                "timestamp": timestamp
            })

    except Exception as e:
        print(f"⚠️ Error in process_frame: {str(e)}")
        return {"error": str(e)}

    return {"faces": face_data}
