import os

import cv2
import numpy as np

file_input="input/"
file_output="output_outline/"
# img_type=".jpeg"
img_type=".png"

files = os.listdir(file_input)
files_out = os.listdir(file_output)
global factor, hud_size, button_down, width, height, old_move_x, old_move_y, move_x, move_y
width, height=(1919,1029)
button_down=False
hud_size=50
factor=1
drawing = False  # true if mouse is pressed
etching=False
ix, iy = -1, -1
old_x, old_y=-1,-1
old_move_x, old_move_y = -1, -1
move_x, move_y = -1, -1

def nothing(x):
    pass


def draw_rect():
    for i in range(img.shape[1]):
        for j in range(img.shape[0]):
            x = i
            y = j
            if img[int(y)][int(x)][0]==0 and img[int(y)][int(x)][1]==0 and img[int(y)][int(x)][2]==0:
                img[int(y)][int(x)] = img_original[int(y)][int(x)]

# Create a function based on a CV2 Event (Left button click)
def drawing_function(event, x, y, flags, param):
    global ix, iy, old_x, old_y, drawing, factor, etching, size, next, reset, etching_thickness, rubber, rubber, hud, button_down, img1, img, moving, pos_y, pos_x, move_img, height, width, old_move_x, old_move_y, move_x, move_y, background, imbg_copy
    if y>hud_size:#int((old_y+hud_size)*factor)>hud_size or int((iy+hud_size)*factor)> hud_size:
        if moving:
            if event == cv2.EVENT_LBUTTONDOWN:  # and event == cv2.EVENT_MOUSEMOVE:
                move_img = True

            elif event == cv2.EVENT_LBUTTONUP:
                move_img = False
            elif move_img:
                pos_x+=int(move_x-old_move_x)
                pos_y+=int(move_y-old_move_y)
        else:
            if not rubber:
                if event == cv2.EVENT_LBUTTONDOWN:  # and event == cv2.EVENT_MOUSEMOVE:
                    drawing = True

                elif event == cv2.EVENT_LBUTTONUP:
                    drawing = False
                elif drawing == True:
                    #cv2.line(img, (ix, iy), (old_x, old_y), (255, 255, 255), thickness=int(2))
                    cv2.line(img1, (ix, iy), (old_x, old_y), (255, 255, 255), thickness=int(2))

            else:
                if event == cv2.EVENT_LBUTTONDOWN:  # and event == cv2.EVENT_MOUSEMOVE:
                    etching = True

                elif event == cv2.EVENT_LBUTTONUP:
                    #draw_rect()
                    etching = False
                if etching == True:
                    #cv2.line(img, (ix, iy), (old_x, old_y), (0, 0, 0), thickness=int((etching_thickness)))
                    cv2.line(img1, (ix, iy), (old_x, old_y), (0, 0, 0),
                             thickness=int((etching_thickness)))
                    # draw_rect((ix, iy), (old_x, old_y), 20)#pts1, pts2, thickness
    else:
        if event == cv2.EVENT_LBUTTONDOWN:
            button_down=True
            if x<=79:
                reset=True
            elif x<=160:
                next=True
            elif x<=241:
                if rubber:
                    rubber=False
                else:
                    rubber=True
            elif x<=924 and x>=844:
                if moving:
                    moving=False
                else:
                    moving=True
            elif x<=1005:
                if width==1919:
                    height, width=(1549, 2559)
                else:
                    height, width = (1029, 1919)
                background = np.zeros((height, width, 3), np.uint8)
                cv2.rectangle(background, (0, 0), (width, height), (66, 66, 66), cv2.FILLED)
                hud = np.zeros((49, width, 3), np.uint8)
                cv2.rectangle(hud, (0, 0), (79, 48), (255, 255, 0))
                cv2.rectangle(hud, (80, 0), (160, 48), (0, 255, 255))
                cv2.rectangle(hud, (161, 0), (241, 48), (255, 0, 255))
                cv2.rectangle(hud, (242, 0), (442, 48), (0, 126, 255))
                cv2.rectangle(hud, (443, 0), (843, 48), (0, 179, 30))
                cv2.rectangle(hud, (844, 0), (924, 48), (85, 0, 255))
                cv2.rectangle(hud, (925, 0), (1005, 48), (255, 0, 85))
        elif event == cv2.EVENT_LBUTTONUP:
            button_down=False
        if button_down:
            if x <= 241:
                return
            elif x <= 442:
                etching_thickness=int((x-242)/4)
            elif x <= 843:
                size=int((int(x)-443)*2)
                if size<1:
                    size=1
    old_move_x, old_move_y=move_x,move_y
    move_x, move_y=x,y
    old_x, old_y = int(ix), int(iy)
    ix, iy = int((x-pos_x)/factor), int((y-hud_size-pos_y)/factor)

def image_labeling(file):
  
    global move_y, move_x, img, img1, img_original, factor, size, next, reset, etching_thickness, rubber, hud, pos_y, pos_x, height, width, background, img_copy

    background=np.zeros((height, width, 3), np.uint8)
    cv2.rectangle(background,(0,0), (width,height), (66,66,66), cv2.FILLED)


    img_original = cv2.imread(file_input+file)
    img=img_original.copy()
    img1 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    barrier = np.zeros((img.shape[0], 9, 3), np.uint8)
    cv2.line(barrier, (4, 0), (4, img.shape[0]), (0, 0, 255), thickness=10)

    img_copy = cv2.resize(img, (int(img_original.shape[1] * factor), int(img_original.shape[0] * factor)),
                          interpolation=cv2.INTER_LINEAR)
    img1_copy = cv2.resize(img1, (int(img_original.shape[1] * factor), int(img_original.shape[0] * factor)),
                           interpolation=cv2.INTER_LINEAR)
    barrier = cv2.resize(barrier, (9, int(img_original.shape[0] * factor)), interpolation=cv2.INTER_LINEAR)
    hud = np.zeros((49, width, 3), np.uint8)
    cv2.rectangle(hud,(0,0), (79, 48), (255,255,0))
    cv2.rectangle(hud, (80, 0), (160, 48), (0, 255, 255))
    cv2.rectangle(hud, (161, 0), (241, 48), (255, 0, 255))
    cv2.rectangle(hud, (242, 0), (442, 48), (0, 126, 255))
    cv2.rectangle(hud, (443, 0), (843, 48), (0, 179, 30))
    cv2.rectangle(hud, (844, 0), (924, 48), (85, 0, 255))
    cv2.rectangle(hud, (925, 0), (1005, 48), (255, 0, 85))
    cv2.putText(hud, "reset", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0))
    cv2.putText(hud, "next", (80, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255))
    #for i in range (img.shape[0]):
    #    for y in range(10):
    #        img1[i][y]=img[i][y]

    cv2.namedWindow(file, cv2.WINDOW_FREERATIO)
    #cv2.createTrackbar('size', file, size, 799, nothing)
    #cv2.createTrackbar('rubber', file, rubber, 49, nothing)
    #cv2.createTrackbar('etching', file, etching_True_False, 1, nothing)
    #cv2.createTrackbar('reset', file, reset, 1, nothing)
    #cv2.createTrackbar('next', file, next, 1, nothing)

    #window = np.concatenate((img, barrier, img1), axis=1)
    #cv2.imshow(file, window)
    # cv2.moveWindow(file, 0, 0)
    while True:
        background_copy=background.copy()
        cv2.namedWindow(file, cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(file, drawing_function)
        if etching:
            cv2.circle(img_copy, (move_x - pos_x, move_y - pos_y - hud_size), int(etching_thickness * factor / 2),
                   (255, 0, 0))
        img_copy=cv2.add(img1_copy,img_copy)
        window = np.concatenate((img_copy, barrier, img1_copy), axis=1)

        position_y,position_x=(pos_y,pos_x)
        if window.shape[0]>height:
            window=window[0:height, 0:window.shape[1]]
        if window.shape[1] > width:
            window = window[0:window.shape[0], 0:width]
        if pos_x<0:
            position_x=0
            window = window[0:window.shape[0], pos_x*-1:window.shape[1]]
        if pos_y<0:
            position_y=0
            window = window[pos_y*-1:window.shape[0], 0:window.shape[1]]
        if pos_x>width-window.shape[1]:
            if pos_x > width:
                position_x=width
                window = window[0:window.shape[0], 0:0]
            window = window[0:window.shape[0], 0:width-pos_x]
        if pos_y>height-window.shape[0]:
            if pos_y > height:
                position_y=height
                window = window[0:0, 0:window.shape[1]]
            window = window[0:height-pos_y, 0:window.shape[1]]
        background_copy[position_y:position_y+window.shape[0], position_x:position_x+window.shape[1]]=window
        window = np.concatenate((hud, background_copy), axis=0)
        if factor!= (size)/100:
            factor=(size)/100
            barrier = cv2.resize(barrier, (9, int(img_original.shape[0]*factor)), interpolation=cv2.INTER_LINEAR)
        img_copy = cv2.resize(img, (int(img_original.shape[1] * factor), int(img_original.shape[0] * factor)),
                              interpolation=cv2.INTER_LINEAR)
        img1_copy = cv2.resize(img1, (int(img_original.shape[1] * factor), int(img_original.shape[0] * factor)),
                               interpolation=cv2.INTER_LINEAR)
        cv2.imshow(file, window)
        key=cv2.waitKey(1)

        if key==ord("q") or next:
            next=False
            return
        elif key==ord("r") or reset:
            #factor = (size) / 100
            img = img_original.copy()#cv2.imread(file_input + file)  # np.zeros((512, 512, 3), np.uint8)
            #img = cv2.resize(img_original, (int(img_original.shape[1] * factor), int(img_original.shape[0] * factor)),
            #                 interpolation=cv2.INTER_LINEAR)
            img1 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
            reset=False
        if rubber:
            cv2.rectangle(hud, (162, 1), (240, 47), (0, 0, 0), cv2.FILLED)
            cv2.putText(hud, "rubber", (161, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255))
        else:
            cv2.rectangle(hud, (162, 1), (240, 47), (0, 0, 0),cv2.FILLED)
            cv2.putText(hud, "pencil", (161, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255))
        if moving:
            cv2.rectangle(hud, (845, 1), (923, 47), (0, 0, 0), cv2.FILLED)
            cv2.putText(hud, "moving", (844, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (85,0,255))
        else:
            cv2.rectangle(hud, (845, 1), (923, 47), (0, 0, 0), cv2.FILLED)
            cv2.putText(hud, "working", (844, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (85,0,255))
        if height==1029:
            cv2.rectangle(hud, (926, 1), (1004, 47), (0, 0, 0), cv2.FILLED)
            cv2.putText(hud, "1920x 1080", (925, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (85,0,255))
        else:
            cv2.rectangle(hud, (926, 1), (1004, 47), (0, 0, 0), cv2.FILLED)
            cv2.putText(hud, "2560x 1600", (925, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (85,0,255))
        cv2.putText(hud, "reset", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0))
        cv2.putText(hud, "next", (80, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255))
        cv2.rectangle(hud, (243, 1), (441, 47), (0, 0, 0), cv2.FILLED)
        cv2.rectangle(hud, (int(242+etching_thickness*4), 10), (int(242+etching_thickness*4), 38), (0, 126, 255), cv2.FILLED)
        cv2.rectangle(hud, (444, 1), (842, 47), (0, 0, 0), cv2.FILLED)
        cv2.rectangle(hud, (int(443 + size /2), 10), (int(443 + size /2), 38),(0, 179, 30), cv2.FILLED)


#cv2.namedWindow('controls')
#cv2.createTrackbar('size', 'controls', 99, 799, nothing)
#cv2.createTrackbar('rubber', 'controls', 9, 49, nothing)
#cv2.createTrackbar('etching', 'controls', 0, 1, nothing)
#cv2.createTrackbar('reset', 'controls', 0, 1, nothing)
#cv2.createTrackbar('next', 'controls', 0, 1, nothing)

global size, next, reset, etching_thickness, rubber, pos_x, pos_y, moving, move_img
move_img=False
pos_x, pos_y=(0,0)
next=False
reset=False
rubber=False
moving=False
etching_thickness=10
size=100

for file in files:
    if not file.endswith(img_type):
        continue

    print(f"Checking file {file.split('.')[0]}")

    labeled = False
    for label in files_out:
        if label.split('_')[0] == file.split('.')[0]:
            print("Skiped")
            labeled = True
    
    if labeled:
        continue

    print(f"Labeling file {file.split('.')[0]}")

    image_labeling(file)
    #rubber = cv2.getTrackbarPos('rubber', file)
    #etching_True_False = cv2.getTrackbarPos('etching', file)
    cv2.destroyWindow(file)#optional
    save= str(file_output+file).replace(img_type, "_labeled"+img_type) #####Kann ich auch noch gerne überarbeiten, halte ich aber für unnötig
    print(f"Created Label {save}")
    img1 = cv2.resize(img1, (int(img_original.shape[1]), int(img_original.shape[0])), interpolation=cv2.INTER_LINEAR)
    img1=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    cv2.imwrite(save, img1)