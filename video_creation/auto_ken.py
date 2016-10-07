import sys, os, glob
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math, random
from PIL import Image


#NOTES: - still to do
    #fix aspect ratio images by applying crops by image's aspect ratio,
    #then put black boxes on the outside

    #facial recognition

def get_img_file(filename):
    f_path = 'images/' + filename
    img = cv2.imread(f_path, 1)
    print "ROWS: " + str(len(img)) + " COLS: " + str(len(img[0]))
    print "Loaded image file into openCV"
    return [img, len(img), len(img[0])]

#creates an array of the same image of the size 24 FPS * number of seconds
def generate_img_array(img, num_sec):
    img_arr = []
    num_frames = int(float(num_sec) * float(24))
    for i in range(0, num_frames):
        img_arr.append(img)

    return img_arr

def random_bounding_box(w_px, h_px):
    box_height = int((float(random.randint(50, 100)) / float(100)) * float(h_px))
    #box_width must be kept at 16/9 of height to maintain aspect ratio
    box_width = int((float(16) / float(9)) * float(box_height))
    if box_width > w_px:
        box_width = int((float(random.randint(50, 100)) / float(100)) * float(w_px))
        box_height = int((float(9) / float(16)) * float(box_width))

    box_x = random.randint(0, w_px - box_width)
    box_y = random.randint(0, h_px - box_height)

    return [box_x, box_y, box_width, box_height]

#(2,6) or (3,7)
def vid_wiggle(box_arr, freq = 2, move_scale = 6):
    num_effects = 24 * freq
    num_frames_per_effect = int(len(box_arr) / num_effects)
    effects = []
    for i in range(0, num_effects):
        effect_x = int((float(random.randint(0, 100)) / float(100)) * float(move_scale))
        effect_y = int((float(random.randint(0, 100)) / float(100)) * float(move_scale))
        for j in range(0, num_frames_per_effect):
            box_arr[num_frames_per_effect * i + j][0] = box_arr[num_frames_per_effect * i + j][0] + effect_x
            box_arr[num_frames_per_effect * i + j][1] = box_arr[num_frames_per_effect * i + j][1] + effect_y

    return box_arr


def random_box_with_ratio(w_px, h_px):
    aspect_ratio = float(w_px) / float(h_px)
    box_height = int((float(random.randint(60, 100)) / float(100)) * float(h_px))
    box_width = int(aspect_ratio * float(box_height))
    box_x = random.randint(0, w_px - box_width - 1)
    box_y = random.randint(0, h_px - box_height - 1)

    return [box_x, box_y, box_width, box_height]


def box_interpolate(w_px, h_px, num_sec):
    # [box_x_start, box_y_start, box_w_start, box_h_start] = random_bounding_box(w_px, h_px)
    # [box_x_end, box_y_end, box_w_end, box_h_end] = random_bounding_box(w_px, h_px)
    [box_x_start, box_y_start, box_w_start, box_h_start] = random_box_with_ratio(w_px, h_px)
    print "START: " + str([box_x_start, box_y_start, box_w_start, box_h_start])
    [box_x_end, box_y_end, box_w_end, box_h_end] = random_box_with_ratio(w_px, h_px)
    print "END: " + str([box_x_end, box_y_end, box_w_end, box_h_end])
    num_interps = int(float(num_sec) * float(24))

    # x_np_array = np.linspace(box_x_start, box_x_end, num_interps)
    # y_np_array = np.linspace(box_y_start, box_y_end, num_interps)
    # w_np_array = np.linspace(box_w_start, box_w_end, num_interps)
    # h_np_array = np.linspace(box_h_start, box_h_end, num_interps)
    box_arr = []
    # for i in range(0, num_interps):
    #     box_arr.append([int(round(x_np_array[i])), int(round(y_np_array[i])), int(round(w_np_array[i])), int(round(h_np_array[i]))])

    box_arr.append([box_x_start, box_y_start, box_w_start, box_h_start])
    x_delta = int((box_x_end - box_x_start) / num_interps)
    y_delta = int((box_y_end - box_y_start) / num_interps)
    width_delta = int((box_w_end - box_w_start) / num_interps)
    height_delta = int((box_h_end - box_h_start) / num_interps)

    for i in range(1, num_interps + 1):
        if (box_arr[i-1][0] + x_delta) > 0:
            curr_x = box_arr[i-1][0] + x_delta
        else:
            curr_x = box_arr[i-1][0]

        if (box_arr[i-1][1] + y_delta) > 0:
            curr_y = box_arr[i-1][1] + y_delta
        else:
            curr_y = box_arr[i-1][1]

        curr_w = box_arr[i-1][2] + width_delta
        curr_h = box_arr[i-1][3] + height_delta
        box_arr.append([curr_x, curr_y, curr_w, curr_h])

    box_arr.append([box_x_end, box_y_end, box_w_end, box_h_end])

    return vid_wiggle(box_arr)
    # return box_arr

def ken_crop(img_arr, box_arr):
    len_arr = len(img_arr)

    for i in range(0, len_arr):
        #print str(i)
        curr_img = img_arr[i]
        curr_box = box_arr[i]
        #crop and then store in size 1920 x 1080 so all images are same size
        img_arr[i] = cv2.resize(curr_img[curr_box[1]:curr_box[1] + curr_box[3], curr_box[0]:curr_box[0] + curr_box[2]], (1920, 1080))
        img_arr[i] = cv2.cvtColor(img_arr[i], cv2.COLOR_RGB2GRAY)

    return img_arr

def ken_crop_with_ratio(img_arr, box_arr):
    len_arr = len(img_arr)

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
        #print "SIZE: " + str(size)
        try:
            # print "(" + str(curr_box[0]) + "," + str(curr_box[0] + curr_box[2]) + "," +  str(curr_box[1]) + "," + str(curr_box[1] + curr_box[3]) + ")",
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
    return img_arr[:(len_arr - 1)]

def displayIMG(orig_img, crop_start, crop_end):
    input_fig = plt.figure(1)
    # plt.subplot(221)
    plt.imshow(orig_img, cmap='gray')
    plt.title('Original Image')
    plt.xticks([]), plt.yticks([])
    input_fig.show()

    edge_fig = plt.figure(2)
    # plt.subplot(222)
    plt.imshow(crop_start, cmap='gray')
    plt.title('Crop Start')
    plt.xticks([]), plt.yticks([])
    edge_fig.show()

    # plt.subplot(223)
    h_fig = plt.figure(3)
    plt.imshow(crop_end, cmap='gray')
    plt.title('Crop End')
    plt.xticks([]), plt.yticks([])
    h_fig.show()

    # KEEP IMAGES OPEN
    print("Press any character and enter to close")
    raw_input()

    return 0

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
