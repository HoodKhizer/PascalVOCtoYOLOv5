import json

out_classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 
               'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'dxb', 'uaq', 'shj', 'auh', 'ajm', 'fuj', 'rak',
               'prefix', 'platenum', 'others', 'taxi', 'dubai_police', 'consulate']

with open('Data/OCR_Data/ocr_classes.txt', 'w', encoding='utf8') as f:
    for cls in out_classes:
        f.write(cls+'\n')

