import os
import face_recognition
import pickle
from PIL import Image
import numpy as np

dataset_path = "dataset"
known_encodings = []
known_names = []

for filename in os.listdir(dataset_path):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(dataset_path, filename)
        name = os.path.splitext(filename)[0]

        try:
            pil_img = Image.open(image_path).convert("RGB")
            rgb_img = np.array(pil_img)
            face_locations = face_recognition.face_locations(rgb_img)
            encodings = face_recognition.face_encodings(rgb_img, face_locations)

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(name)
                print(f"✅ Processed: {filename}")
            else:
                print(f"⚠️ No face found in {filename}, skipping.")

        except Exception as e:
            print(f"❌ Error in {filename}: {e}")

# Save encodings
with open("encodings.pkl", "wb") as f:
    pickle.dump((known_encodings, known_names), f)

print("✅ Encodings saved to encodings.pkl")
