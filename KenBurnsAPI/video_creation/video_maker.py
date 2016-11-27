import math, time, sys, os
from ken_audio_video import *
from auto_ken_runner import *

def make_total_vid(name, arr_arr_images, arr_audio):
    # name  = "Barack Obama"
    # CHANGE THIS HERE TO GET LONGER VIIDEOSSSSSS
    # FIX MULTIPLE AUDIO PROBLEM
    # arr_arr_images = [['obama.jpg', 'obama_3.jpg'], ['obama_4.jpg', 'obama_5.jpg']]
    # print "arr_arr_image: BEFORE" + str(arr_arr_images)
    arr_arr_images = [arr_arr_images[0], arr_arr_images[1], arr_arr_images[2], arr_arr_images[3], arr_arr_images[4], arr_arr_images[5]]
    # print "arr_arr_image:" + str(arr_arr_images)
    total_aud = arr_audio[len(arr_audio) - 1]
    arr_audio = arr_audio[0:6]

    split_name = name.split(' ')
    vid_name = ''
    for i in range(0, len(split_name)):
        vid_name = vid_name + str(split_name[i])
        if i != (len(split_name) - 1):
            vid_name = vid_name + '_'

    vid_only_name = vid_name + '_vid.mp4'
    aud_only_name = vid_name + '_aud.mp4'
    vid_name = vid_name + '_test.mp4'

    print "Video Name: " + vid_name
    print "Video Only Name: " + vid_only_name

    #call thing to make the video
    overall_runner(vid_only_name, arr_arr_images, arr_audio)

    #combine all audio into a single audio file
    concat_audio(vid_only_name, [total_aud], vid_name)

    delete_audio_files()

    return vid_name

def delete_audio_files():
    # dp = 'video_creation/audio/'
    # f_list = os.listdir(dp)
    # for f_name in f_list:
    #     os.remove(dp + f_name)
    # print "all audio files removed"

    # dp = 'video_creation/videos_no_audio/'
    # f_list = os.listdir(dp)
    # for f_name in f_list:
    #     os.remove(dp + f_name)
    # print "all videos_no_audio files removed"
    return 0

if __name__ == '__main__':
    # all_ken_runner(['obama.jpg', 'obama_1.jpg', 'obama_2.jpg', 'obama_3.jpg', 'obama_4.jpg', 'obama_5.jpg'], [12, 10, 13, 10, 12, 14], output_fname)
    # make_total_vid("Barack Obama", [['obama.jpg', 'obama_3.jpg'], ['obama_4.jpg', 'obama_5.jpg']], ["jimmy2.mp3", 'jimmy2.mp3'])
    delete_audio_files()
