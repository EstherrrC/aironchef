import onnxruntime as ort
import numpy as np
import cv2
import os

onnx_model_path = "efficientnet_b4.onnx"
session = ort.InferenceSession(onnx_model_path)

classes = []
with open("imagenet_class.txt", "r") as file:
  for line in file:
    classes.append(line.strip())

def preprocess_image(image_path) -> np.ndarray:
  img = cv2.imread(image_path)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  img = cv2.resize(img, (224, 224))
  img = img.astype(np.float32) / 255.0
  img = np.transpose(img, (2, 0, 1))
  img = np.expand_dims(img, axis=0)
  return img

def classify_images_in_folder(folder_path, output_file):
    input_name = session.get_inputs()[0].name
    image_files = [f for f in os.listdir(folder_path) if f.endswith((".jpg", ".png", ".jpeg"))]

    with open(output_file, "w") as f:
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            input_tensor = preprocess_image(image_path)

            output = session.run(None, {input_name: input_tensor})

            class_idx = np.argmax(output[0])
            class_label = classes[class_idx]

            f.write(f"{image_file}: {class_label}\n")
            print(f"Image: {image_file} | Predicted class: {class_label}")

image_folder_path = "./image"
output_txt_file = "fridge_ingredient.txt"

classify_images_in_folder(image_folder_path, output_txt_file)
