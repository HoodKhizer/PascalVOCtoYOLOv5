import xml.etree.ElementTree as ET
import glob
import os
import json


def xml_to_yolo_bbox(bbox, w, h):
    # xmin, ymin, xmax, ymax
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]


def yolo_to_xml_bbox(bbox, w, h):
    # x_center, y_center width heigth
    w_half_len = (bbox[2] * w) / 2
    h_half_len = (bbox[3] * h) / 2
    xmin = int((bbox[0] * w) - w_half_len)
    ymin = int((bbox[1] * h) - h_half_len)
    xmax = int((bbox[0] * w) + w_half_len)
    ymax = int((bbox[1] * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]

# classes_with_attr = ['Prefix_char', 'Platenum_char', 'State']
classes_to_find = ['belt', 'no belt', 'steering wheel', 'mobile', 'Car', 'Plate']

# This is relevant to output and should be this way, otherwise labels can be misalligned leading
# to poor accuracy
classes = ['belt', 'no belt', 'mobile', 'car', 'steering wheel', 'plate'] # Order is important
input_dir = "/home/red/Repos/IVMS/Dataset/LabelledDataForPlatesandVehicles/IVMSFrontPlates1Day/Annotations/"
output_dir = "/home/red/Repos/IVMS/Dataset/LabelledDataForPlatesandVehicles/IVMSFrontPlates1Day/Yolov5/labels/"
image_dir = "/home/red/Repos/IVMS/Dataset/LabelledDataForPlatesandVehicles/IVMSFrontPlates1Day/JPEGImages"

# create the labels folder (output directory)
os.makedirs(output_dir,exist_ok=True)

# identify all the xml files in the annotations folder (input directory)
files = glob.glob(os.path.join(input_dir, '*.xml'))
# loop through each 
for fil in files:
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]
    # check if the label contains the corresponding image file
    imagepath = os.path.join(image_dir, f"{filename}.jpeg")
    if not os.path.exists(imagepath):
        print(f"{filename} image does not exist!")
        continue

    result = []

    # parse the content of the xml file
    print(fil)
    tree = ET.parse(fil)
    root = tree.getroot()
    width = int(root.find("size").find("width").text)
    height = int(root.find("size").find("height").text)

    for obj in root.findall('object'):
        if obj.find("name").text in classes_to_find:
            label = obj.find("name").text.lower()
            # check for new classes and append to list
            if label not in classes:
                classes.append(label)
            print(classes)
            index = classes.index(label)
            print(index, label)
            pil_bbox = [int(x.text.split('.')[0]) for x in obj.find("bndbox")]
            yolo_bbox = xml_to_yolo_bbox(pil_bbox, width, height)
            # convert data to string
            bbox_string = " ".join([str(x) for x in yolo_bbox])
            result.append(f"{index} {bbox_string}")

    if result:
        # generate a YOLO format text file for each xml file
        with open(os.path.join(output_dir, f"{filename}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(result))

# generate the classes file as reference
with open('Plate_Det_Data/classes.txt', 'w', encoding='utf8') as f:
    f.write(json.dumps(classes))


        # if obj.find("name").text in classes_with_attr:
        #     for attrib in obj.findall('attributes'):
        #         print(attrib.find("attribute").find("value").text)
        # print("=============")