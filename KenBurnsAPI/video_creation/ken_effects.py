import sys, os, glob
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math, random
from PIL import Image

#(2,6) or (3,7)
def vid_wiggle(box_arr, w_px, h_px, freq = 2, move_scale = 5):
    move_scale_horiz = w_px * (float(move_scale) / float(1920))
    move_scale_vert = h_px * (float(move_scale) / float(1080))
    num_effects = 24 * freq
    num_frames_per_effect = int(len(box_arr) / num_effects)
    print "LEN: " + str(len(box_arr))
    print "TOT: " + str(num_frames_per_effect * num_effects)
    for i in range(0, num_effects):
        effect_x = int((float(random.randint(0, 100)) / float(100)) * float(move_scale_horiz))
        effect_y = int((float(random.randint(0, 100)) / float(100)) * float(move_scale_vert))
        for j in range(0, num_frames_per_effect):
            # print str(num_frames_per_effect * i + j)
            if ((num_frames_per_effect * i + j) <= 24) or ((num_frames_per_effect * i + j) > (num_frames_per_effect * num_effects - 24)):
                effect_x = int(effect_x / 2)
                effect_y = int(effect_y / 2)

            box_arr[num_frames_per_effect * i + j][0] = box_arr[num_frames_per_effect * i + j][0] + effect_x
            box_arr[num_frames_per_effect * i + j][1] = box_arr[num_frames_per_effect * i + j][1] + effect_y

    return box_arr

def face_detect_boxes(curr_img):
    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    face_boxes = face_classifier.detectMultiScale(cv2.cvtColor(curr_img, cv2.COLOR_BGR2GRAY), 1.5, 5)
    if len(face_boxes) == 0:
        print "Empty - no faces detected"
    else:
        # print str(face_boxes)
        print "Number of faces found: " + str(len(face_boxes))

    return face_boxes

def pick_effect(w_px, h_px, faces, prev_effect = 'random'):
    num_f = len(faces)
    effect = "random"
    if num_f == 0:
        if (float(w_px) / float(h_px)) > 1.5: #then pan
            if prev_effect.find("pan") == -1:
                r = ["pan left to right", "pan right to left"]
                effect = random.choice(r)
            else:
                #can't find left to right, prev was right to left -> curr should be left to right
                if prev_effect.find("left to right") == -1:
                    effect = "pan left to right"
                else:
                    effect = "pan right to left"
    elif num_f == 1: #zoom
        if prev_effect.find("zoom") == -1:
            r = ["zoom in", "zoom out"]
            effect = random.choice(r)
        else:
            if prev_effect.find("in") == -1:
                effect = "zoom in"
            else:
                effect = "zoom out"
    elif num_f <= 3:
        min_x = w_px
        max_x = 0
        min_y = h_px
        max_y = 0
        for i in range(0, num_f):
            if faces[i][0] < min_x:
                min_x = faces[i][0]
            if faces[i][1] < min_y:
                min_y = faces[i][1]
            if (faces[i][0] + faces[i][2]) > max_x:
                max_x = (faces[i][0] + faces[i][2])
            if (faces[i][1] + faces[i][3]) > max_y:
                max_y = (faces[i][1] + faces[i][3])
        faces = [[min_x, min_y, max_x - min_x, max_y - min_y]]
        print "2-3 faces big box: " + str(faces)

        if prev_effect.find("zoom") == -1:
            r = ["zoom in", "zoom out"]
            effect = random.choice(r)
        else:
            if prev_effect.find("in") == -1:
                effect = "zoom in"
            else:
                effect = "zoom out"
    else:
        if prev_effect.find("pan") == -1:
            r = ["pan left to right", "pan right to left"]
            effect = random.choice(r)
        else:
            #can't find left to right, prev was right to left -> curr should be left to right
            if prev_effect.find("left to right") == -1:
                effect = "pan left to right"
            else:
                effect = "pan right to left"

    return [effect, faces]

if __name__ == '__main__':
    filename = 'obama.jpg'
    f_path = 'images/' + filename
    img = cv2.imread(f_path, 1)
    face_detect_boxes(img)
