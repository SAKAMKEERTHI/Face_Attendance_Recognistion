import os
from deepface import DeepFace

db_path = "D:/new_face_attendance/know_faces"

# Use any image from the folder to trigger embedding
sample_image = os.listdir(db_path)[0]
DeepFace.find(
    img_path=os.path.join(db_path, sample_image),
    db_path=db_path,
    model_name="VGG-Face",
    detector_backend="opencv",
    enforce_detection=False
)
