import cv2
import numpy as np
from ultralytics import YOLO

def load_model(model_path):
    model = YOLO(model_path)
    return model

def detect(model, image_path, save_path='detected_image.jpg'):

    # Load the image using OpenCV
    image = cv2.imread(image_path)
    
    # Perform detection
    results = model.predict(image)
    
    # Extract class names and bounding box points
    class_names = []
    box_points = []
    for result in results[0].boxes:
        class_id = int(result.cls)
        class_name = results[0].names[class_id]
        bbox = result.xyxy.tolist()[0]
        class_names.append(class_name)
        box_points.append(bbox)
        
        # Draw bounding box and label on the image
        cv2.rectangle(image, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)
        cv2.putText(image, class_name, (int(bbox[0]), int(bbox[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Save the detected image
    cv2.imwrite(save_path, image)

    # Crop the image using the first bounding box
    # if box_points:
    #     x1, y1, x2, y2 = map(int, box_points[0])
    #     cropped_image = image[y1:y2, x1:x2]
    #     cv2.imwrite('crop_1st_box.jpg', cropped_image)
    
    return class_names, box_points

#test
# if __name__ == "__main__":
#     model_path = 'event.pt'  
#     image_path = 'frame.png'  
#     save_path = 'detected_image.jpg'
    
#     # Load the model
#     model = load_model(model_path)
    
#     # Perform detection and save the image
#     class_names, box_points = detect(model, image_path, save_path)
    
#     # Print the results
#     print("Detected class names:", class_names)
#     print("Bounding box points:", box_points)
