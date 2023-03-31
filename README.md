# PascalVOCtoYOLOv5
Script to convert Pascal VOC labels to YOLOv5 format for training the model. I dont know how many times I have written this script... This is one last attempt to save it somewhere I would remember, LOL.
Thankfully I found this post on TDS, so this is adopted (well, more than 90% is taken from here)
https://towardsdatascience.com/convert-pascal-voc-xml-to-yolo-for-object-detection-f969811ccba5 


Don't forget to create dataset.yaml as described in the Yolov5 repo docs by ultralytics.
Yolov5 is trained using centerx, centery, width, height and Pascal VOC format uses xmin, ymix, xmax, ymax format, so the main conversion is between these co-ordinate types. Also in the resulting yolov5 files there, the first column reperesents class number which needs to be defined in the dataset.yaml file under names: tag. Below is the format for dataset.yaml file
'''
# Train/val/test sets as 1) dir: path/to/imgs, 2) file: path/to/imgs.txt, or 3) list: [path/to/imgs1, path/to/imgs2, ..]
path: ../datasets/coco128  # dataset root dir
train: images/train2017  # train images (relative to 'path') 128 images
val: images/train2017  # val images (relative to 'path') 128 images
test:  # test images (optional)

# Classes (80 COCO classes)
names:
  0: person
  1: bicycle
  2: car
  ...
  77: teddy bear
  78: hair drier
  79: toothbrush
  '''