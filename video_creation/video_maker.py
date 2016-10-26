import math, time, sys, os
from ken_audio_video import *
from auto_ken_runner import *

def make_total_vid(name, arr_arr_images, arr_audio):
    split_name = name.split(' ')
    vid_name = ''
    for i in range(0, len(split_name)):
        vid_name = vid_name + split_name
        if i != (len(split_name) - 1):
            vid_name = vid_name + '_'

    vid_only_name = vid_name + '_vid.mp4'
    aud_only_name = vid_name + '_aud.mp4'
    vid_name = vid_name + '.mp4'

    print "Video Name: " + vid_name
    print "Video Only Name: " + vid_only_name

    #call thing to make the video
    overall_runner(vid_only_name, arr_arr_image, arr_audio)

    #combine all audio into a single audio file
    concat_audio(aud_only_name, arr_audio)

    #combine audio and video
    combine_av(vid_only_name, aud_only_name, vid_name)


if __name__ == '__main__':
    return 0
