import sys, os, glob
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math, random
from PIL import Image

#(2,6) or (3,7)
def vid_wiggle(box_arr, freq = 2, move_scale = 6):
    num_effects = 24 * freq
    num_frames_per_effect = int(len(box_arr) / num_effects)
    print "LEN: " + str(len(box_arr))
    print "TOT: " + str(num_frames_per_effect * num_effects)
    for i in range(0, num_effects):
        effect_x = int((float(random.randint(0, 100)) / float(100)) * float(move_scale))
        effect_y = int((float(random.randint(0, 100)) / float(100)) * float(move_scale))
        for j in range(0, num_frames_per_effect):
            # print str(num_frames_per_effect * i + j)
            if ((num_frames_per_effect * i + j) <= 24) or ((num_frames_per_effect * i + j) > (num_frames_per_effect * num_effects - 24)):
                effect_x = int(effect_x / 2)
                effect_y = int(effect_y / 2)

            box_arr[num_frames_per_effect * i + j][0] = box_arr[num_frames_per_effect * i + j][0] + effect_x
            box_arr[num_frames_per_effect * i + j][1] = box_arr[num_frames_per_effect * i + j][1] + effect_y

    return box_arr
