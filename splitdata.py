import random
import glob
import os
import shutil


def copyfiles(fil, root_dir):
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]
    print(basename, filename, fil, root_dir)
    # copy image
    src = fil
    dest = os.path.join(out_dir, root_dir, image_dir, f"{filename}.jpg")
    shutil.copyfile(src, dest)

    # # copy annotations
    src = os.path.join(in_anno_dir, f"{filename}.txt")
    dest = os.path.join(out_dir, root_dir, label_dir, f"{filename}.txt")
    if os.path.exists(src):
        shutil.copyfile(src, dest)

in_image_dir = "Data/OCR_Data/Cropped_Plates_Img"
in_anno_dir = "Data/OCR_Data/Cropped_Plates_Anno"

out_dir = "Data/OCR_Data"

label_dir = "labels/"
image_dir = "images/"

lower_limit = 0

img_file_path_list = glob.glob(os.path.join(in_image_dir, '*.jpg'))

random.shuffle(img_file_path_list)

folders = {"train": 0.8, "val": 0.1, "test": 0.1}
check_sum = sum([folders[x] for x in folders])

assert check_sum == 1.0, "Split proportion is not equal to 1.0"

for folder in folders:
    os.mkdir(os.path.join(out_dir, folder))
    temp_label_dir = os.path.join(out_dir, folder, label_dir)
    os.mkdir(temp_label_dir)
    temp_image_dir = os.path.join(out_dir, folder, image_dir)
    os.mkdir(temp_image_dir)

    limit = round(len(img_file_path_list) * folders[folder])
    for fil in img_file_path_list[lower_limit:lower_limit + limit]:
        copyfiles(fil, folder)
    lower_limit = lower_limit + limit
