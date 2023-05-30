import cv2
import os

# returns filename without extension
def get_filename(path):
    basename = os.path.basename(path)
    filename = os.path.splitext(basename)[0]
    return filename

# check if the image exists corresponding to xml file
def check_image_existence(image_input_dir, filename):
    image_path = os.path.join(image_input_dir, f"{filename}.jpeg")
    if not os.path.exists(image_path):
        image_path = os.path.join(image_input_dir, f"{filename}.jpg")
        if not os.path.exists(image_path):   
            print(f"{image_path} jpeg or jpg image does not exist!")
            return False
        
    return image_path

# get image width and height
def get_width_height(root, full_img_pixels):
    anno_width = int(root.find("size").find("width").text)
    anno_height = int(root.find("size").find("height").text)
    img_height, img_width, _ = full_img_pixels.shape
    return anno_width, anno_height, img_width, img_height

#
def get_plates_coords(list_of_objects, labels_to_crop_for):
    list_plate_bboxes = []
    for obj in list_of_objects:
        if obj.find("name").text in labels_to_crop_for:
            pil_bbox = [int(x.text.split('.')[0]) for x in obj.find("bndbox")]
            list_plate_bboxes.append(pil_bbox) 
    return list_plate_bboxes

def integer_conversion(in_str):
    try:
        out = int(in_str)
        return out
    except:
        return out
    
def find_attribute(obj):
    for attribs in obj.findall('attributes'):
        for attrib in attribs.findall('attribute'):
            if attrib.find('name').text != 'rotation':
                return attrib.find('value').text


def disp_img(img):
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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

# Check if to_check rectangle is inside ref.
# ref (reference) and to_check are two rectangles of the form
# xmin,ymin,xmax,ymax
def contain_check(ref, to_check):
    x1_1, y1_1, x2_1, y2_1 = to_check
    x1_2, y1_2, x2_2, y2_2 = ref
    # Check if rect1 is completely inside rect2
    if x1_1 >= x1_2 and y1_1 >= y1_2 and x2_1 <= x2_2 and y2_1 <= y2_2:
        return True
    else:
        return False

# Transform to_transform rectangle so the origin is inside ref
# ref (reference) and to_transform are two rectangles of the form
# xmin,ymin,xmax,ymax
def transform_coords(ref, to_transform):
    x1_1, y1_1, x2_1, y2_1 = to_transform
    x1_2, y1_2, x2_2, y2_2 = ref

    newx1 = x1_1 - x1_2
    newx2 = x2_1 - x2_2
    newy1 = y1_1 - y1_2
    newy2 = y2_1 - y2_2
    return [newx1, newx2, newy1, newy2]
