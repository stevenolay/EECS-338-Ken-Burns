import math, time, sys, os
from ken_audio_video import *
from auto_ken_runner import *

def make_total_vid(name, arr_arr_images, arr_audio):
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
    concat_audio(vid_only_name, arr_audio, vid_name)

if __name__ == '__main__':
    # all_ken_runner(['obama.jpg', 'obama_1.jpg', 'obama_2.jpg', 'obama_3.jpg', 'obama_4.jpg', 'obama_5.jpg'], [12, 10, 13, 10, 12, 14], output_fname)
    make_total_vid("Barack Obama", [['obama.jpg', 'obama_3.jpg'], ['obama_4.jpg', 'obama_5.jpg']], ["jimmy2.mp3", 'jimmy2.mp3'])
