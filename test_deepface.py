from deepface import DeepFace

# Compare two images
result = DeepFace.verify(
    img1_path="D:/new_face_attendance/dataset/keerthi/keerthi_1.jpg",
    img2_path="D:/new_face_attendance/dataset/keerthi/keerthi_1.jpg",  # Use same image for test
    model_name="Facenet"
)

print("✅ DeepFace result:")
print(result)
