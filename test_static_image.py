import face_recognition
from PIL import Image
import numpy as np

# Load and convert image
image_path = "dataset/Keerthi/keerthi_1.jpg"  # Use a real image path
pil_image = Image.open(image_path).convert("RGB")
rgb_image = np.array(pil_image)

print(f"Image dtype: {rgb_image.dtype}, shape: {rgb_image.shape}")

try:
    # Use the lower-level API directly
    face_locations = face_recognition.api.face_locations(rgb_image)
    print(f"✅ Detected {len(face_locations)} face(s)")
except Exception as e:
    print(f"❌ Face recognition error: {e}")
