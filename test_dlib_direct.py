import dlib
from PIL import Image
import numpy as np

# Load and convert image
image_path = "D:/new_face_attendance/test_face.jpg"
pil_image = Image.open(image_path).convert("RGB")
rgb_image = np.array(pil_image)

print(f"Image dtype: {rgb_image.dtype}, shape: {rgb_image.shape}")

try:
    detector = dlib.get_frontal_face_detector()
    detected_faces = detector(rgb_image, 1)
    print(f"✅ Detected {len(detected_faces)} face(s) using dlib directly")
except Exception as e:
    print(f"❌ dlib error: {e}")
