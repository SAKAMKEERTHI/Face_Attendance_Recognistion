import os
from PIL import Image
import numpy as np

dataset_path = "dataset"

for filename in os.listdir(dataset_path):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(dataset_path, filename)
        try:
            img = Image.open(image_path)
            print(f"{filename}: mode={img.mode}, size={img.size}")
            if img.mode != "RGB":
                print(f"⚠️ {filename} is not RGB. Converting...")
                rgb_img = img.convert("RGB")
                rgb_img.save(image_path)
        except Exception as e:
            print(f"❌ Error with {filename}: {e}")
