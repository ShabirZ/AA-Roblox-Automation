import os
from ultralytics import YOLO
from pathlib import Path
import cv2

# Load YOLOv8 model
class objectDetector:
    def __init__(self):
        model_path = "AAObjectDetectorV3.pt"
        self.model = YOLO(model_path)
    def detect(self, img):
        #{0: 'defeat', 1: 'max', 2: 'replay', 3: 'towerUI', 4: 'yes'}
        labels = []
        results = self.model.predict(source=img, save=False, save_txt=False, save_conf=False, conf = .5)
        for result in results:
            boxes = result.boxes
            
            for idx in range(len(boxes)):
                label = boxes[idx].cls
                labels.append(int(label))
        return labels
       