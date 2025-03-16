import onnxruntime as ort
import numpy as np
import cv2
import os

class ImageClassifier:
    def __init__(self, model_path="efficientnet_b4.onnx", class_labels_file="imagenet_class.txt"):
        self.session = ort.InferenceSession(model_path)

        self.classes = []
        with open(class_labels_file, "r") as file:
            for line in file:
                self.classes.append(line.strip())
    
    def preprocess_image(self, image_path) -> np.ndarray:
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0)
        return img

    def classify_images(self, image_paths: list) -> str:
        results = []
        input_name = self.session.get_inputs()[0].name

        for image_path in image_paths:
            if not os.path.exists(image_path):
                results.append(f"{image_path}: File not found")
                continue

            input_tensor = self.preprocess_image(image_path)
            output = self.session.run(None, {input_name: input_tensor})

            class_idx = np.argmax(output[0])
            class_label = self.classes[class_idx]
            results.append(f"{image_path}: {class_label}")
            #print(f"Image: {image_path} | Predicted class: {class_label}")

        return "\n".join(results)
