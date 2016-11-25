import sys, os, glob
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math, random, time
from PIL import Image
from auto_ken import *
import moviepy.editor as mp
from mutagen.mp3 import MP3

def single_auto_ken_runner(filename, num_seconds, prev_effect):
    [image, height_px, width_px, faces] = get_img_file(filename)
    if image == None:
        return [[], 'No Image Found']
    i_arr = generate_img_array(image, num_seconds)
    [b_a, effect] = box_interpolate(width_px, height_px, num_seconds, faces, prev_effect)
    cropped_arr = ken_crop_with_ratio(i_arr, b_a)

    return [cropped_arr, effect]

#possible performance improvement -- instead of creating clips just create a large array and then pass them to all_clips_arr
def make_full_clip(vid_arr):
    #start_vid = time.clock()
    #output_folder = 'videos_no_audio/'
    #output_path = output_folder + output_name
    clips_arr = []
    for i in range(0, len(vid_arr)):
        #start_img = time.clock()
        print "Image Number: " + str(i)
        clips_arr.append(mp.ImageSequenceClip(vid_arr[i], fps = 24))

        #end_img = time.clock()
        #print "Finished image " + str(i) + " in " + str(end_img - start_img) + " seconds."

    clippy = mp.concatenate_videoclips(clips_arr)
    return clippy

def make_full_vid(arr_arr_i, arr_audio):
    all_clips_arr = []
    for i in range(0, len(arr_arr_i)):
        curr_aud = MP3('video_creation/audio/' + str(arr_audio[i]))
        len_aud = int(curr_aud.info.length)
        print "AUD LEN: " + str(len_aud)
        curr_times = []
        num_images = len(arr_arr_i[i])
        print "i: " + str(i) + " num images in i: " + str(num_images)
        avg_time = len_aud / len(arr_arr_i[i])
        if avg_time <= 10:
            print "avg time shorter than 10"
            arr_arr_i[i] = arr_arr_i[i][:int(len_aud / 10)]
            avg_time = 10

        sum_time = 0
        num_images = len(arr_arr_i[i])
        for j in range(0, num_images):
            print " "
            if j == (num_images - 1):
                curr_times.append(len_aud - sum_time)
            else:
                curr_times.append(int(random.randint(avg_time - int(0.2 * avg_time), avg_time + int(0.2 * avg_time))))
        #is this right????
        print "TIMES: " + str(curr_times)
        all_clips_arr.append(all_ken_runner(arr_arr_i[i], curr_times))

    final_clip = mp.concatenate_videoclips(all_clips_arr)
    print "FINAL CLIP RETURNED"
    return final_clip


def write_vid(output_name, final_clip):
    output_folder = 'video_creation/videos_no_audio/'
    output_path = output_folder + output_name
    final_clip.write_videofile(output_path)

def all_ken_runner(f_names, time_arr):
    print "IN ALL KEN RUNNER"
    vid_imgs_arr = []
    vid_eff = ["random"]
    print "FNAMES:" + str(f_names)
    for i in range(0, len(f_names)):
        [arr, eff] = single_auto_ken_runner(f_names[i], time_arr[i], vid_eff[i-1])
        if arr != []:
            vid_imgs_arr.append(arr)
            vid_eff.append(eff)

    curr_clip = make_full_clip(vid_imgs_arr)
    print "EFFECTS: " + str(vid_eff)
    return curr_clip
    print "DONE"

def overall_runner(vid_name, arr_arr_images, arr_audio):
    final_v = make_full_vid(arr_arr_images, arr_audio)
    write_vid(vid_name, final_v)
    return 0

if __name__ == '__main__':
    output_fname = raw_input("Please enter an output filename: ")
    all_ken_runner(['obama.jpg', 'obama_1.jpg', 'obama_2.jpg', 'obama_3.jpg', 'obama_4.jpg', 'obama_5.jpg'], [12, 10, 13, 10, 12, 14], output_fname)
