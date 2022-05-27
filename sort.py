import os

import cv2
import numpy as np
import shutil

file_data = "input/"
file_input="output_filled/"
file_output="output_sorted/"
labels = ["bad", "drive", "head", "no field"]
img_type=".png"

files = os.listdir(file_input)
files_out = []

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


for label in labels:
    dir = file_output + label
    
    dir_in = dir + "/input/"
    dir_out = dir + "/output/"

    ensure_dir(dir_in)
    ensure_dir(dir_out)

    files_out.append(os.listdir(dir_out))
    # files_out.append(os.listdir(dir_in))

def label_file(name, label_index):
    input_source_path = file_data + name.replace("_labeled", "")
    output_source_path = file_input + name
    dest_path = file_output + labels[label_index] + "/"
    # print(f"Labeling {input_source_path}")
    # print(f"Labeling {output_source_path}")
    # print(f"Labeling {dest_path}")

    shutil.copyfile(input_source_path, os.path.abspath(dest_path + "input/" + name))
    shutil.copyfile(output_source_path, os.path.abspath(dest_path + "output/" + name))

i = 0

for file in files:

    i += 1
    print(f"{i}/{len(files)}")

    labeled = False
    for label in files_out:
        for labeled_file in label:
            if labeled_file == file:
                print(f"Skipped {file.split('.')[0]}")
                labeled = True
    
    # print(labeled)

    if labeled:
        continue

    img_in=cv2.imread(file_data+file.replace("_labeled", ""))
    img_out=cv2.imread(file_input+file)
    cv2.imshow(file + " out", img_out)
    cv2.imshow(file + " in", img_in)
    
    label_index = cv2.waitKey(0) - 48

    if label_index > len(labels):
        print("Invalid Label")
        exit()

    label_file(file, label_index)

    cv2.destroyAllWindows()