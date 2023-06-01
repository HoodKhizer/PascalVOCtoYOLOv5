import xml.etree.ElementTree as ET
import glob
import os
import cv2
import utils
import json

# TODO, refactor this monster of a code :}, happy about this monster though, LOL
classes_inside_plates = ['Prefix_char', 'Platenum_char', 'State', 'Platenum', 'Prefix']

classes_without_attrib = ['Prefix_char', 'Platenum_char', 'State', 'dubai_police', 'taxi', 'consulate']

out_classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 
               'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'dxb', 'uaq', 'shj', 'auh', 'ajm', 'fuj', 
               'rak', 'prefix', 'platenum', 'others', 'taxi']

# classes_to_find = []
# classes_to_find = ['belt', 'no belt', 'mobile', 'car', 'steering wheel', 'plate'] # Order is important
anno_input_dir = "Data/Dxb_plates_all/Annotations"
anno_output_dir = "Data/OCR_Data/Cropped_Plates_Anno"
image_input_dir = "Data/Dxb_plates_all/JPEGImages"
image_output_dir = "Data/OCR_Data/Cropped_Plates_Img"
labels_to_crop_for = ['Plate'] 
# create the labels folder (output directory)
os.makedirs(anno_output_dir, exist_ok=True)
os.makedirs(image_output_dir, exist_ok=True)

# identify all the xml files in the annotations folder (input directory)
anno_files = glob.glob(os.path.join(anno_input_dir, '*.xml'))
# anno_images = glob.glob(os.path.join(anno_input_dir, '*.jpg'))
files_to_correct = []
for anno_path in anno_files:
    if '0010200026220906174159' in anno_path:
        continue
    result_anno = []
    filename = utils.get_filename(anno_path)
    # print(filename + '.jpg')
    
    # check if the label contains the corresponding image file
    image_path = utils.check_image_existence(image_input_dir, filename)
    if not image_path:
        print("File doesn't exist", image_path)
        continue

    tree = ET.parse(anno_path)
    root = tree.getroot()

    full_img_pixels = cv2.imread(image_path)
    base_image_name = os.path.basename(image_path)

    anno_width, anno_height, img_width, img_height = utils.get_width_height(root, full_img_pixels)
    assert anno_width == img_width, "image and annotation width should be equal"
    assert anno_height == img_height, "image and annotation height should be equal"

    list_of_objects = root.findall('object')

    list_plate_bboxes = utils.get_plates_coords(list_of_objects, labels_to_crop_for)

    for plate_index, plate_bbox in enumerate(list_plate_bboxes):
        prefix_char_count = 0
        prefix_count = 0
        fixed_plate_bbox= []
        for point in plate_bbox:
            if point < 0:
                point = 0
            fixed_plate_bbox.append(point)
        plate_bbox = fixed_plate_bbox
        crop_img_pixels = full_img_pixels[plate_bbox[1]:plate_bbox[3], plate_bbox[0]:plate_bbox[2]]
        crop_height, crop_width, _ = crop_img_pixels.shape
        # list_new_bbox = []
        for obj in list_of_objects:
            object_class = obj.find("name").text
            if not object_class in classes_inside_plates:
                continue
            pil_bbox = [int(x.text.split('.')[0]) for x in obj.find("bndbox")]
            contains = utils.contain_check(plate_bbox, pil_bbox)
            if contains:
                new_bbox = utils.transform_coords(plate_bbox, pil_bbox)
                class_from_attrib = utils.find_attribute(obj)
                if not class_from_attrib:
                    if object_class in classes_without_attrib:
                        print(class_from_attrib, obj.find('name').text, anno_path)
                        if not base_image_name in files_to_correct:
                            files_to_correct.append(base_image_name)
                            continue
                    else:
                        class_index = out_classes.index(object_class.lower())

                else:
                    class_index = out_classes.index(class_from_attrib.lower())

                print(base_image_name, crop_width, crop_height, object_class, class_from_attrib, plate_bbox)
                
                new_bbox = utils.xml_to_yolo_bbox(new_bbox, crop_width, crop_height)
                if object_class == 'Prefix_char':
                            prefix_char_count += 1
                            last_prefix_char_bbox = new_bbox
                if object_class == 'Prefix':
                    prefix_count += 1
                bbox_string = " ".join([str(x) for x in new_bbox])
                result_anno.append(f"{class_index} {bbox_string}")
        if prefix_count == 0:
            if prefix_char_count == 1:
                class_index = out_classes.index('prefix')
                bbox_string = " ".join([str(x) for x in last_prefix_char_bbox])
                result_anno.append(f"{class_index} {bbox_string}")
        else:
            if not base_image_name in files_to_correct:
                files_to_correct.append(base_image_name)
        
        if result_anno:
            anno_out_file_path = os.path.join(anno_output_dir, f"{filename}")
            img_out_file_path = os.path.join(image_output_dir, f"{filename}")
            if os.path.exists(anno_out_file_path):
                anno_out_file_path += f"_{plate_index}.txt"
                img_out_file_path += f"_{plate_index}.jpg"
            else:
                anno_out_file_path += f".txt"
                img_out_file_path += f".jpg"

            # print(anno_out_file_path)
            # print("", img_out_file_path)
            with open(anno_out_file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(result_anno))
                cv2.imwrite(img_out_file_path, crop_img_pixels)
        print("------------------")

if files_to_correct:
    with open("faultyfiles.txt", "a+", encoding="utf-8") as f:
        # f.write("\n".join(files_to_correct))
        f.write(str(files_to_correct))

with open('Data/OCR_Data/classes_ocr.txt', 'w', encoding='utf8') as f:
    f.write(json.dumps(out_classes))



################## USEFUL COMMENTS ##################

                # cv2.imwrite(img_out_file_path, crop_img_pixels)

                    # print(class_index, object_class, class_from_attrib)
                    
                    ## Decide on class names ##
                    # A - Z, 0 - 9, Prefix, Num, State #
                    


# print(files_to_correct, len(files_to_correct))
                # if not contains:
                #     print(anno_path)
                #     print(plate_bbox, contains)
                #     print(pil_bbox, contains)
                #     disp_img(full_img_pixels)
                #     print("===")

   
# loop through each 
# for fil in files:
#     basename = os.path.basename(fil)
#     filename = os.path.splitext(basename)[0]
#     # check if the label contains the corresponding image file
#     imagepath = os.path.join(image_dir, f"{filename}.jpeg")
#     if not os.path.exists(imagepath):
#         imagepath = os.path.join(image_dir, f"{filename}.jpg")
#         if not os.path.exists(imagepath):   
#             print(f"{filename} image does not exist!")
#             continue

#     result = []

#     # parse the content of the xml file
#     print(fil)
#     tree = ET.parse(fil)
#     root = tree.getroot()
#     width = int(root.find("size").find("width").text)
#     height = int(root.find("size").find("height").text)

#     for obj in root.findall('object'):
#         if obj.find("name").text in classes_to_find:
#             label = obj.find("name").text.lower()
#             if obj.find("name").text in classes_with_attr:
#                 for attrib in obj.findall('attributes'):
#                     print(attrib.find("attribute").find("value").text)
    
            # check for new classes and append to list
#             if label not in classes:
#                 classes.append(label)
#             print(classes)
#             index = classes.index(label)
#             print(index, label)
#             pil_bbox = [int(x.text.split('.')[0]) for x in obj.find("bndbox")]
#             yolo_bbox = xml_to_yolo_bbox(pil_bbox, width, height)
#             # convert data to string
#             bbox_string = " ".join([str(x) for x in yolo_bbox])
#             result.append(f"{index} {bbox_string}")

#     if result:
#         # generate a YOLO format text file for each xml file
#         with open(os.path.join(output_dir, f"{filename}.txt"), "w", encoding="utf-8") as f:
#             f.write("\n".join(result))
# # generate the classes file as reference
# with open('classes_plates.txt', 'w', encoding='utf8') as f:
#     f.write(json.dumps(classes))


