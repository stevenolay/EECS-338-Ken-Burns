import sys, os, glob
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math, random, time
from PIL import Image
from auto_ken import *
import moviepy.editor as mp

def single_auto_ken_runner(filename, num_seconds):
    [image, height_px, width_px] = get_img_file(filename)
    i_arr = generate_img_array(image, num_seconds)
    b_a = box_interpolate(width_px, height_px, num_seconds)
    cropped_arr = ken_crop_with_ratio(i_arr, b_a)

    return cropped_arr

def make_full_vid(vid_arr):
    start_vid = time.clock()
    #vid = cv2.VideoWriter('combo_new_vid.avi', cv2.cv.CV_FOURCC('m', 'p', '4', 'v'), 24, (1920,1080), False)
    clips_arr = []
    for i in range(0, len(vid_arr)):
        start_img = time.clock()
        print "Image Number: " + str(i)
        clips_arr.append(mp.ImageSequenceClip(vid_arr[i], fps = 24))

        end_img = time.clock()
        print "Finished image " + str(i) + " in " + str(end_img - start_img) + " seconds."

    final_clip = mp.concatenate_videoclips(clips_arr)
    aud = mp.AudioFileClip("Carrie.mp3")
    aud.set_duration(final_clip.duration)
    real_clip = final_clip.set_audio(aud)
    real_clip.write_videofile("moviepy_test.mp4")
    #vid.release()
    print "Finished video in " + str(end_img - start_img) + " seconds."
    return 0


def all_ken_runner(f_names, time_arr):
    ### remove these 2 lines when actual filenames are inputted as a list
    # f_names = ['pup.jpg', 'scene1.jpg', 'ytho.jpg', 'scene2.jpg']
    # time_arr = [4, 3, 5, 4]
    vid_imgs_arr = []
    for i in range(0, len(f_names)):
        vid_imgs_arr.append(single_auto_ken_runner(f_names[i], time_arr[i]))

    make_full_vid(vid_imgs_arr)
    print "DONE"


if __name__ == '__main__':
    all_ken_runner(['pup.jpg', 'scene1.jpg', 'ytho.jpg', 'scene2.jpg'], [4, 3, 5, 4])
    print "DONE 2"
