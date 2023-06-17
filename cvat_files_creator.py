import os
import json

# Path to the YOLOv5 output directory
yolov5_labels_dir = 'Data/CVAT_upload/labels/'
yolov5_images_dir = 'Data/CVAT_upload/images/'
# Path to the CVAT annotations output file
cvat_annotations_file = 'Data/CVAT_upload/cvat_annotations/annotations.json'

# Parse YOLOv5 output files
annotations = []
for filename in os.listdir(yolov5_labels_dir):
    if filename.endswith('.txt'):
        image_name = os.path.splitext(filename)[0] + '.jpg'
        image_path = os.path.join(yolov5_images_dir, image_name)
        if not os.path.exists(image_path):
            image_name = os.path.splitext(filename)[0] + '.jpeg'
            image_path = os.path.join(yolov5_images_dir, image_name)

        annotation_path = os.path.join(yolov5_labels_dir, filename)

        with open(annotation_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            class_id, x, y, w, h = map(float, line.strip().split())

            annotation = {
                'image': image_path,
                'label': 'class_name',  # Replace with actual class name based on class_id
                'x': x,
                'y': y,
                'width': w,
                'height': h
            }

            annotations.append(annotation)

# Save annotations in CVAT format
cvat_annotations = {
    'annotations': annotations
}

with open(cvat_annotations_file, 'w') as f:
    json.dump(cvat_annotations, f)