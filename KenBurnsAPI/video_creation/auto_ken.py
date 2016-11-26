import sys, os, glob
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math, random
from PIL import Image
from ken_effects import *
import urllib



def get_img_file(f_url):
    # f_path = 'video_creation/images/' + filename
    # print "Name: " + str(f_path)
    # img = cv2.imread(f_path, 1)
    print "URL:" + f_url
    res = urllib.urlopen(str(f_url))
    image = np.asarray(bytearray(res.read()), dtype="uint8")
    img = cv2.imdecode(image, cv2.IMREAD_COLOR)

    if img == None:
        return [None, -1, -1, -1]
    face_boxes = face_detect_boxes(img)
    print "ROWS: " + str(len(img)) + " COLS: " + str(len(img[0]))
    print "Loaded image file into openCV"
    return [img, len(img), len(img[0]), face_boxes]

#creates an array of the same image of the size 24 FPS * number of seconds
def generate_img_array(img, num_sec):
    img_arr = []
    print str(num_sec)
    num_frames = int(float(num_sec) * float(24))
    for i in range(0, num_frames):
        img_arr.append(img)

    return img_arr

def random_box_with_ratio(w_px, h_px):
    aspect_ratio = float(w_px) / float(h_px)
    box_height = int((float(random.randint(60, 100)) / float(100)) * float(h_px))
    box_width = int(aspect_ratio * float(box_height))
    if (w_px - box_width - 1) > 1:
        box_x = random.randint(0, w_px - box_width - 1)
    else:
        box_x = random.randint(0, 1)

    if (h_px - box_height - 1) > 1:
        box_y = random.randint(0, h_px - box_height - 1)
    else:
        box_y = random.randint(0, 1)

    return [box_x, box_y, box_width, box_height]

def pan_box(w_px, h_px, side):
    #can't pan on an image that is more square than 1920 x 1080
    box_x = 0
    box_y = 0
    box_w = h_px
    box_h = h_px
    if side == 'right':
        box_x = w_px - box_w - 1

    return [box_x, box_y, box_w, box_h]

def zoom_box(w_px, h_px, f_box = []):
    if len(f_box) != 0:
        zoom_w = random.randint(f_box[2], w_px)
        zoom_h = random.randint(f_box[3], h_px)
        zoom_x = random.randint(0, f_box[0])
        zoom_y = random.randint(0, f_box[1])

        return [zoom_x, zoom_y, zoom_w, zoom_h]
    else:
        return random_box_with_ratio(w_px, h_px)

def first_last_boxes(w_px, h_px, faces, effect = 'no_effect'):
    start_list = [0, 0, 0, 0]
    end_list = [0, 0, 0, 0]
    if effect.find('no_effect') != -1:
        print "no effect"
        start_list = [0, 0, w_px, h_px]
        end_list = [0, 0, w_px, h_px]
        return [start_list, end_list]

    if effect.find('zoom') != -1:
        temp_list = zoom_box(w_px, h_px, faces[0])
        if effect.find('in') != -1: #zoom in effect
            start_list = [0, 0, w_px, h_px]
            end_list = temp_list
        else: #zoom out
            start_list = temp_list
            end_list = [0, 0, w_px, h_px]
        return [start_list, end_list]

    if effect.find('pan') != -1:
        #change left_list, right_list defs to be real things
        left_list = pan_box(w_px, h_px, 'left')
        right_list = pan_box(w_px, h_px, 'right')
        # left right, maybe change earlier params
        if effect.find('left to right') != -1: #pan right to left
            return [left_list, right_list]
        else:  #pan left to right
            return [right_list, left_list]

    start_list = random_box_with_ratio(w_px, h_px)
    end_list = random_box_with_ratio(w_px, h_px)
    return [start_list, end_list]

def box_interpolate(w_px, h_px, num_sec, faces, prev_effect = 'random'):
    num_end_interps = 24
    num_interps = int(float(num_sec - 2) * float(24))
    print "number of interpolations: " + str(num_interps)

    [effect, faces] = pick_effect(w_px, h_px, faces, prev_effect)

    [start_box, end_box] = first_last_boxes(w_px, h_px, faces, effect)
    [box_x_start, box_y_start, box_w_start, box_h_start] = start_box
    [box_x_end, box_y_end, box_w_end, box_h_end] = end_box
    if (box_h_start == 0) or (box_h_end == 0):
        print "INITIAL DIVIDE BY 0 -- pls fix"

    box_arr = []
    print 'START: ' + str([box_x_start, box_y_start, box_w_start, box_h_start])
    print 'END: ' + str([box_x_end, box_y_end, box_w_end, box_h_end])
    x_delta = int((box_x_end - box_x_start) / num_interps)
    y_delta = int((box_y_end - box_y_start) / num_interps)
    width_delta = int((box_w_end - box_w_start) / num_interps)
    if(width_delta <= 0):
        print "tooo"
    height_delta = int((box_h_end - box_h_start) / num_interps)
    if(height_delta <= 0):
        print "tooooo"

    for i in range(0, num_end_interps):
        box_arr.append([box_x_start, box_y_start, box_w_start, box_h_start])

    for i in range(0, num_interps):
        if (box_arr[num_end_interps + i-1][0] + x_delta) > 0:
            curr_x = box_arr[num_end_interps + i-1][0] + x_delta
        else:
            curr_x = box_arr[num_end_interps + i-1][0]

        if (box_arr[num_end_interps + i-1][1] + y_delta) > 0:
            curr_y = box_arr[num_end_interps + i-1][1] + y_delta
        else:
            curr_y = box_arr[num_end_interps + i-1][1]

        curr_w = box_arr[num_end_interps + i-1][2] + width_delta
        if (box_arr[num_end_interps + i-1][3] + height_delta > (h_px / 4)):
            curr_h = box_arr[num_end_interps + i-1][3] + height_delta
        else:
            curr_h = box_arr[num_end_interps + i-1][3]
        if curr_h == 0:
            print "DIV BY 0 ERROR -- pls fix"
        box_arr.append([curr_x, curr_y, curr_w, curr_h])

    for i in range(0, num_end_interps):
        box_arr.append(box_arr[num_end_interps + num_interps + i - 1])

    return [vid_wiggle(box_arr, w_px, h_px), effect]
    # return box_arr

def ken_crop_with_ratio(img_arr, box_arr):
    len_arr = len(img_arr)
    #print "Box arr: " + str(box_arr)

    for i in range(0, len_arr):
        #print str(i)
        curr_img = img_arr[i]
        curr_box = box_arr[i]
        border = [0, 0, 0, 0] #top, bottom, left, right
        #crop and then store in size 1920 x 1080 so all images are same size
        size = [1920, 1080]
        if abs(((float(curr_box[2]) / float(curr_box[3])) - (float(1920)/float(1080)))) < 0.1:
            #print "SAMEEE"
            size = size
        elif (float(curr_box[2]) / float(curr_box[3])) < (float(1920)/float(1080)):
            #print "MORE SQ"
            size[0] = int(float(curr_box[2]) / float(curr_box[3]) * 1080)
            size[1] = 1080
        else:
            #print "LONG"
            size[0] = 1920
            size[1] = int(float(curr_box[3]) / float(curr_box[2]) * 1920)

        border[0] = int(math.floor((1080 - size[1]) / 2))
        #border[1] = int(math.ceil((1080 - size[1]) / 2))
        border[1] = 1080 - (border[0] + size[1])
        border[2] = int(math.floor((1920 - size[0]) / 2))
        #border[3] = int(math.ceil((1920 - size[0]) / 2))
        border[3] = 1920 - (border[2] + size[0])
        # print "SIZE: " + str(size),
        try:
            # print "(" + str(curr_box[0]) + "," + str(curr_box[0] + curr_box[2]) + "," +  str(curr_box[1]) + "," + str(curr_box[1] + curr_box[3]) + ")"
            temp_img = cv2.resize(curr_img[curr_box[1]:curr_box[1] + curr_box[3], curr_box[0]:curr_box[0] + curr_box[2]], (size[0], size[1]))
            #print "TEMP SHAPE: " + str(temp_img.shape)
        except (cv2.error):
            temp_img = np.zeros((size[1], size[0], 3))

        BLACK = [0, 0, 0]
        img_arr[i] = cv2.copyMakeBorder(temp_img, border[0], border[1], border[2], border[3], cv2.BORDER_CONSTANT,value=BLACK)
        #print "SHAPE: " + str(img_arr[i].shape)
        img_arr[i] = cv2.cvtColor(img_arr[i], cv2.COLOR_BGR2RGB)
        #print "SHAPE 2222: " + str(img_arr[i].shape)

    print "KB DONE in images"
    print " "
    return img_arr[:(len_arr - 1)]

def save_images(cropped_arr):
    num_frames = len(cropped_arr)
    for i in range(0, num_frames):
        #print str(i)
        cv2.imwrite('test' + str(i) + ".jpg", cropped_arr[i])

    print "Saved"
    return 0

def make_vid(cropped_arr):
    test_vid = cv2.VideoWriter('test_pup_2.avi', cv2.cv.CV_FOURCC('m', 'p', '4', 'v'), 24, (1920,1080), False)
    num_frames = len(cropped_arr)
    for i in range(0, num_frames):
        print str(i) + str(cropped_arr[i].shape)
        test_vid.write(cropped_arr[i])

    test_vid.release()


if __name__ == '__main__':
    num_seconds = 4
    [image, height_px, width_px] = get_img_file('pup.jpg')
    print "WIDTH: " + str(width_px) + " HEIGHT: " + str(height_px)
    # cv2.imshow('image', image)
    i_arr = generate_img_array(image, num_seconds)
    print "LENGTH: " + str(len(i_arr))
    b_a = box_interpolate(width_px, height_px, num_seconds)
    print "BOX INTERP LEN: " + str(len(b_a))
    # cropped_arr = ken_crop(i_arr, b_a)
    cropped_arr = ken_crop_with_ratio(i_arr, b_a)
    # save_images(cropped_arr)
    make_vid(cropped_arr)
    print "DONE"
