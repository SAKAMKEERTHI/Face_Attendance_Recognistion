from deepface import DeepFace
import os
import datetime
import pandas as pd
import cv2

db_path = "D:/new_face_attendance/know_faces"
img_path = "D:/new_face_attendance/dataset/keerthi/keerthi_1.jpg"
log_path = "D:/new_face_attendance/attendance/attendance.csv"

# Run face matching
results = DeepFace.find(
    img_path=img_path,
    db_path=db_path,
    model_name="Facenet",
    detector_backend="opencv"
)

# Log attendance
if len(results) > 0 and not results[0].empty:
    matched_file = results[0].iloc[0]["identity"]
    name = os.path.splitext(os.path.basename(matched_file))[0]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create attendance folder if missing
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Append to CSV
    if not os.path.exists(log_path):
        df = pd.DataFrame(columns=["Name", "Timestamp"])
    else:
        df = pd.read_csv(log_path)

    # Avoid duplicate entries for same person in same session
    if not ((df["Name"] == name) & (df["Timestamp"].str.startswith(timestamp[:10]))).any():
        df.loc[len(df)] = [name, timestamp]
        df.to_csv(log_path, index=False)
        print(f"✅ {name} marked present at {timestamp}")
    else:
        print(f"ℹ️ {name} already marked today")
else:
    print("❌ No match found")
