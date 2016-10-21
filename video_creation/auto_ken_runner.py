import sys, os, glob
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math, random, time
from PIL import Image
from auto_ken import *
import moviepy.editor as mp

def single_auto_ken_runner(filename, num_seconds, prev_effect):
    [image, height_px, width_px, faces] = get_img_file(filename)
    # if image == -1:
    #     return [[], 'No Image Found']
    i_arr = generate_img_array(image, num_seconds)
    [b_a, effect] = box_interpolate(width_px, height_px, num_seconds, faces, prev_effect)
    cropped_arr = ken_crop_with_ratio(i_arr, b_a)

    return [cropped_arr, effect]

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
    #vid.release()
    return 0


def all_ken_runner(f_names, time_arr, output_name = 'KB Video.mp4'):
    ### remove these 2 lines when actual filenames are inputted as a list
    # f_names = ['pup.jpg', 'scene1.jpg', 'ytho.jpg', 'scene2.jpg']
    # time_arr = [4, 3, 5, 4]
    vid_imgs_arr = []
    vid_eff = ["random"]
    for i in range(0, len(f_names)):
        [arr, eff] = single_auto_ken_runner(f_names[i], time_arr[i], vid_eff[i-1])
        vid_imgs_arr.append(arr)
        vid_eff.append(eff)

    make_full_vid(vid_imgs_arr, output_name)
    print "EFFECTS: " + str(vid_eff)
    print "DONE"


if __name__ == '__main__':
    output_fname = raw_input("Please enter an output filename: ")
    # all_ken_runner(['scene1.jpg', 'scene3.jpg', 'scene2.jpg'], [12, 14, 13], output_fname)
    # all_ken_runner(['obama.jpg', 'obama_1.jpg', 'obama_2.jpg', 'obama_3.jpg', 'obama_4.jpg', 'obama_5.jpg'], [12, 14, 13, 10, 14, 9], output_fname)
    all_ken_runner(['obama.jpg', 'obama_1.jpg', 'obama_2.jpg', 'obama_3.jpg', 'obama_4.jpg', 'obama_5.jpg'], [12, 10, 13, 10, 12, 14], output_fname)
