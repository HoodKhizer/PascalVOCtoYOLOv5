import xml.etree.ElementTree as ET
import glob
import os
import cv2
import utils


classes_inside_plates = ['Prefix_char', 'Platenum_char', 'State', 'Platenum', 'Prefix']
list_of_deviants = ['police', 'taxi', 'other', 'consul']
out_classes = []
# classes_to_find = []
# classes_to_find = ['belt', 'no belt', 'mobile', 'car', 'steering wheel', 'plate'] # Order is important
anno_input_dir = "Data/Dxb_plates_all/Annotations"
# anno_output_dir = "Dubai_Job_1/Cropped_Plates_Anno"
image_input_dir = "Data/Dxb_plates_all/JPEGImages"
# image_output_dir = "Dubai_Job_1/Cropped_Plates_Img"
labels_to_crop_for = ['Plate'] 
# create the labels folder (output directory)
# os.makedirs(anno_output_dir, exist_ok=True)
# os.makedirs(image_output_dir, exist_ok=True)

# identify all the xml files in the annotations folder (input directory)
anno_files = glob.glob(os.path.join(anno_input_dir, '*.xml'))
# anno_images = glob.glob(os.path.join(anno_input_dir, '*.jpg'))
files_to_correct = []
for anno_path in anno_files:
    basename = os.path.basename(anno_path)
    filename = os.path.splitext(basename)[0]
    # check if the label contains the corresponding image file
    image_path = os.path.join(image_input_dir, f"{filename}.jpeg")
    if not os.path.exists(image_path):
        image_path = os.path.join(image_input_dir, f"{filename}.jpg")
        if not os.path.exists(image_path):   
            print(f"{image_path} jpeg or jpg image does not exist!")
            continue
    base_image_name = os.path.basename(image_path)
    tree = ET.parse(anno_path)
    root = tree.getroot()
    anno_width = int(root.find("size").find("width").text)
    anno_height = int(root.find("size").find("height").text)
    full_img_pixels = cv2.imread(image_path)
    img_height, img_width, _ = full_img_pixels.shape
    if img_height != anno_height and img_width != anno_width:
        print(f"{image_path} conflict of resolution between annotation and image")

    list_of_objects = root.findall('object')
    list_plate_bboxes = []
    for obj in list_of_objects:
        if obj.find("name").text in labels_to_crop_for:
            label = obj.find("name").text.lower()
            pil_bbox = [int(x.text.split('.')[0]) for x in obj.find("bndbox")]
            list_plate_bboxes.append(pil_bbox) 
            crop_img_pixels = full_img_pixels[pil_bbox[1]:pil_bbox[3], pil_bbox[0]:pil_bbox[2]]

    for plate_bbox in list_plate_bboxes:
        list_new_bbox = []
        for obj in list_of_objects:
            if obj.find("name").text in classes_inside_plates:
                pil_bbox = [int(x.text.split('.')[0]) for x in obj.find("bndbox")]
                contains = utils.contain_check(plate_bbox, pil_bbox)
                if contains:
                    new_bbox = utils.transform_coords(plate_bbox, pil_bbox)
                    list_new_bbox.append(new_bbox)
                    class_from_attrib = utils.find_attribute(obj)
                    if not class_from_attrib:
                        found = False
                        for word in list_of_deviants:
                            if word in obj.find('name').text.lower():
                                found = True
                                break   
                        if found and basename not in files_to_correct:
                            files_to_correct.append(base_image_name) 
                        if obj.find('name').text in ['Prefix_char', 'Platenum_char', 'State']:
                            print(class_from_attrib, obj.find('name').text, anno_path)
                            base_image_name = os.path.basename(image_path)
                            if not base_image_name in files_to_correct:
                                files_to_correct.append(base_image_name)
                    else:
                        if class_from_attrib == 'OTHERS':
                            print("Found", base_image_name)  
                        
                        found = False
                        for word in list_of_deviants:
                            if word in class_from_attrib.lower():
                                found = True
                                break

                        if  found and basename not in files_to_correct:
                            files_to_correct.append(base_image_name)        
                              
print(files_to_correct)
                        # files_to_correct.append(anno_path)
                    


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
# with open('classes.txt', 'w', encoding='utf8') as f:
#     f.write(json.dumps(classes))


