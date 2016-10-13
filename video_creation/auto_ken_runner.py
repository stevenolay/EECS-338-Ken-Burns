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

def make_full_vid(vid_arr, output_name):
    start_vid = time.clock()
    output_folder = 'output_videos/'
    output_path = output_folder + output_name
    #vid = cv2.VideoWriter('combo_new_vid.avi', cv2.cv.CV_FOURCC('m', 'p', '4', 'v'), 24, (1920,1080), False)
    clips_arr = []
    for i in range(0, len(vid_arr)):
        start_img = time.clock()
        print "Image Number: " + str(i)
        clips_arr.append(mp.ImageSequenceClip(vid_arr[i], fps = 24))

        end_img = time.clock()
        print "Finished image " + str(i) + " in " + str(end_img - start_img) + " seconds."

    final_clip = mp.concatenate_videoclips(clips_arr)
    # print "VID DURATION: " + str(final_clip)
    # aud = mp.AudioFileClip("audio/Carrie.mp3")
    # print "INIT aud duration: " + str(aud.duration)
    # aud.set_duration(5)
    # print "FINAL aud duration: " + str(aud.duration)

    final_clip.write_videofile(output_path)
    #real_clip = final_clip.set_audio(aud)
    # real_clip.write_videofile("moviepy_test_new.mp4")
    #vid.release()
    # print "Finished video in " + str(end_img - start_img) + " seconds."
    return 0


def all_ken_runner(f_names, time_arr, output_name = 'KB Video.mp4'):
    ### remove these 2 lines when actual filenames are inputted as a list
    # f_names = ['pup.jpg', 'scene1.jpg', 'ytho.jpg', 'scene2.jpg']
    # time_arr = [4, 3, 5, 4]
    vid_imgs_arr = []
    for i in range(0, len(f_names)):
        vid_imgs_arr.append(single_auto_ken_runner(f_names[i], time_arr[i]))

    make_full_vid(vid_imgs_arr, output_name)
    print "DONE"


if __name__ == '__main__':
    output_fname = raw_input("Please enter an output filename: ")
    all_ken_runner(['scene1.jpg', 'scene3.jpg', 'scene2.jpg'], [12, 14, 13], output_fname)
