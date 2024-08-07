import cv2
import os
import shutil

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def convert_video_to_frames(video_path, output_folder, frame_limit):
    cap = cv2.VideoCapture(video_path)
    create_directory(output_folder)
    
    frame_count = 0
    while frame_count < frame_limit:
        ret, frame = cap.read()
        if not ret:
            break
        frame_filename = f"{output_folder}/frame_{frame_count:04d}.jpg"
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    cap.release()

def collect_images(folder):
    images = [f for f in os.listdir(folder) if f.endswith('.jpg')]
    return sorted(images)

def move_files(src_folder, dst_folder):
    create_directory(dst_folder)
    for filename in os.listdir(src_folder):
        src_file = os.path.join(src_folder, filename)
        dst_file = os.path.join(dst_folder, filename)
        shutil.move(src_file, dst_file)

def main():
    video_path = input("Enter the path of the video: ")
    video_path = os.path.abspath(video_path)  # Convert to absolute path
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_folder = os.path.join(".", video_name)
    
    convert_video_to_frames(video_path, output_folder, frame_limit=50)
    
    input("Delete bad frames then click enter to continue...")
    
    images = collect_images(output_folder)
    
    classes_input = input("Enter the classes (0-11) separated by space: ")
    class_mapping = {
        '0': 'HT&AT','1': 'SB','2':'Time','3': 'Event','4': 'NP',
        '5':'F-MUN','6':'F-MCI','7':'F-LIV','8':'F-CRY','9':'F-TOT','10':'F-CHE' , '11':'F-NEW' ,
    }
    classes = [c for c in classes_input.split() if c in class_mapping]
    
    # Collect bounding box information for each class
    bounding_boxes = {}
    for c in classes:
        print(f"Select bounding box for class '{class_mapping[c]}' on the displayed image.")
        image_path = os.path.join(output_folder, images[0])
        image = cv2.imread(image_path)
        
        height, width, _ = image.shape
        
        roi = cv2.selectROI("Select ROI", image, fromCenter=False, showCrosshair=True)
        x, y, w, h = roi
        cv2.destroyAllWindows()
                
        center_x = (x + w / 2) / width
        center_y = (y + h / 2) / height
        norm_width = w / width
        norm_height = h / height
        
        bounding_boxes[c] = (center_x, center_y, norm_width, norm_height)

    images_folder = os.path.join(output_folder, "images")
    labels_folder = os.path.join(output_folder, "labels")
    
    create_directory(images_folder)
    create_directory(labels_folder)
    
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, image)
        new_image_path = os.path.join(images_folder, f"{video_name}_{i:04d}.jpg")
        os.rename(image_path, new_image_path)
        
        label_path = os.path.join(labels_folder, f"{video_name}_{i:04d}.txt")
        with open(label_path, 'w') as f:
            for c in classes:
                center_x, center_y, norm_width, norm_height = bounding_boxes[c]
                f.write(f"{c} {center_x} {center_y} {norm_width} {norm_height}\n")
    
    print("Images and labels have been processed and moved to respective folders.")
    
    # Splitting into train, test, valid
    def split_data(images_folder, labels_folder, output_folder, split_ratio=(0.7, 0.2, 0.1)):
        images = sorted(os.listdir(images_folder))
        labels = sorted(os.listdir(labels_folder))
        
        total_images = len(images)
        train_end = int(split_ratio[0] * total_images)
        valid_end = train_end + int(split_ratio[1] * total_images)
        
        create_directory(os.path.join(output_folder, "train", "images"))
        create_directory(os.path.join(output_folder, "train", "labels"))
        create_directory(os.path.join(output_folder, "valid", "images"))
        create_directory(os.path.join(output_folder, "valid", "labels"))
        create_directory(os.path.join(output_folder, "test", "images"))
        create_directory(os.path.join(output_folder, "test", "labels"))
        
        def move_files(start, end, split_type):
            for i in range(start, end):
                os.rename(
                    os.path.join(images_folder, images[i]), 
                    os.path.join(output_folder, split_type, "images", images[i])
                )
                os.rename(
                    os.path.join(labels_folder, labels[i]), 
                    os.path.join(output_folder, split_type, "labels", labels[i])
                )
        
        move_files(0, train_end, "train")
        move_files(train_end, valid_end, "valid")
        move_files(valid_end, total_images, "test")
    
    split_data(images_folder, labels_folder, output_folder)
    
    print("Data has been split into train, test, and valid folders.")
    
    # Move files to dataset folder
    dataset_folder = "./dataset"
    move_files(os.path.join(output_folder, "train", "images"), os.path.join(dataset_folder, "train", "images"))
    move_files(os.path.join(output_folder, "train", "labels"), os.path.join(dataset_folder, "train", "labels"))
    move_files(os.path.join(output_folder, "test", "images"), os.path.join(dataset_folder, "test", "images"))
    move_files(os.path.join(output_folder, "test", "labels"), os.path.join(dataset_folder, "test", "labels"))
    move_files(os.path.join(output_folder, "valid", "images"), os.path.join(dataset_folder, "valid", "images"))
    move_files(os.path.join(output_folder, "valid", "labels"), os.path.join(dataset_folder, "valid", "labels"))
    
    print("Files have been moved to the dataset folder.")

if __name__ == "__main__":
    main()
