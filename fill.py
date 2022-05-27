import os

import cv2
import numpy as np

file_input="output_outline/"
file_output="output_filled/"
img_type=".png"

files = os.listdir(file_input)

def fill_img(img):
    path=False
    for y in range(img.shape[1]):
        path=False
        for x in range(img.shape[0]):
            if img[x][y][0]==255:
                path=True
            img[x][y]=(255*path,255*path,255*path)
    return img

i = 0

for file in files:
    img=cv2.imread(file_input+file)
    i += 1
    print(f'{i}/{len(files)}')
    # print(file_output+file)
    img=fill_img(img)
    # cv2.imshow("a", img)
    # cv2.waitKey(0)
    cv2.imwrite(file_output+file, img)
