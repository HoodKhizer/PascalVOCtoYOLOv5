from PIL import Image, ImageDraw
import glob
import random
import os

classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 
  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", 
  "u", "v", "w", "x", "y", "z", "dxb", "uaq", "shj",
  "auh", "ajm", "fuj", "rak", "prefix", "platenum",
  "others", "taxi"]


print(len(classes))
def yolo_to_xml_bbox(bbox, w, h):
    # x_center, y_center width heigth
    w_half_len = (bbox[2] * w) / 2
    h_half_len = (bbox[3] * h) / 2
    xmin = int((bbox[0] * w) - w_half_len)
    ymin = int((bbox[1] * h) - h_half_len)
    xmax = int((bbox[0] * w) + w_half_len)
    ymax = int((bbox[1] * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]


def draw_image(img, bboxes, classes_idxes):
    draw = ImageDraw.Draw(img)
    for bbox, class_idx in zip(bboxes,classes_idxes):
        draw.rectangle(bbox, outline="red", width=2)
        print(class_idx)
        if not class_idx == '44':
            class_name = classes[int(class_idx)]
            draw.text((bbox[0], bbox[1] - 10), class_name.upper(), fill=(0, 255, 0))
    img.save("example.jpg")
    img.show()


# image_filename = "Data/OCR_Data/Cropped_Plates_Img/0010100015220906171354.jpg"
# label_filename = "Data/OCR_Data/Cropped_Plates_Anno/0010100015220906171354.txt"

img_dir = 'Data/OCR_Data/Cropped_Plates_Img/'
anno_dir = 'Data/OCR_Data/Cropped_Plates_Anno/'

file_list = glob.glob(img_dir + "/*")

image_filename = random.choice(file_list)
label_filename = os.path.join(anno_dir,
                              os.path.basename(image_filename).split('.')[0] + '.txt')

bboxes = []
classes_idxs = []
img = Image.open(image_filename)

print(label_filename)
with open(label_filename, 'r', encoding='utf8') as f:
    for line in f:
        
        data = line.strip().split(' ')
        print(data)
        # bbox = [float(x) for x in data[1:] if data[0] == '5']
        bbox = [float(x) for x in data[1:]]
        class_idx = data[0]
        if class_idx:
            classes_idxs.append(class_idx)
        if bbox:
            bboxes.append(yolo_to_xml_bbox(bbox, img.width, img.height))

draw_image(img, bboxes, classes_idxs)