import os
from ultralytics import YOLO
from pathlib import Path
import cv2

temp_picture = "\\test_imgs_V3\\screenshotV3_1_p4 (1).png
test = YOLO("AAObjectDetectorV3.pt")
results = test.predict(source=str(""), save=True, save_txt=False, save_conf=False)
for result in results:
    dir(results)
# Load YOLOv8 model
class objectDetector:
    def __init__(self):
        model_path = "AAObjectDetectorV3.pt"
        self.model = YOLO(model_path)
    def detect_img(self, img):
        labels = []
        results = self.model.predict(source=str(img), save=False, save_txt=False, save_conf=False)
        for result in results:
            boxes = result.boxes
            for label in boxes.cls:
                labels.append(int(label))
        return labels
