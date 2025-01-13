import os
from ultralytics import YOLO
from pathlib import Path
import cv2

# Load YOLOv8 model
model_path = "AAObjectDetectorV3.pt"
model = YOLO(model_path)

# Paths
test_folder = Path("test_imgs_V3")
output_folder = test_folder.parent / "detections"

# Create output folder if it doesn't exist
output_folder.mkdir(exist_ok=True)

# Supported image extensions
supported_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}

# Loop through all images in the test_detection_imgs folder
for image_file in test_folder.iterdir():
    if image_file.suffix.lower() in supported_extensions:
        print(f"Processing: {image_file.name}")

        # Run detection
        results = model.predict(source=str(image_file), save=True, save_txt=False, save_conf=False)

        # Save detected images
        for result in results:
            # `result.plot()` creates an image with detections
            detected_img = result.plot()

            # Save the image
            detection_save_path = output_folder / image_file.name
            cv2.imwrite(str(detection_save_path), detected_img)
            print(f"Saved detection: {detection_save_path}")

print("Detection completed!")
