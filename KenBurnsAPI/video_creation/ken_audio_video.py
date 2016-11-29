import sys, os, glob, math, time, shutil
import cv2
import numpy as np
import moviepy.editor as mp
import ffmpy
from collections import OrderedDict

def combine_av(vid_name, audio_name, out_name):
    input_vid = 'videos_no_audio/' + vid_name
    input_aud = 'audio_no_video/' + audio_name
    output_fname = 'output_videos/' + out_name
    ff = ffmpy.FFmpeg(inputs={input_vid : None, input_aud : None}, outputs={output_fname : None})
    ff.run()

# def concat_audio(aud_name, aud_arr):
def concat_audio(vid_name, aud_arr, out_name):
    #concatenate all the audio into a single file
    #aud_path = 'audio_no_video/' + aud_name
    #f = open(output_path, 'wb')
    # shutil.copyfileobj(open(f))
    input_vid = 'video_creation/videos_no_audio/' + vid_name
    output_fname = 'static/output_videos/' + out_name
    input_a = [(input_vid, None)]
    for i in range(0, len(aud_arr)):
        print "HERE + str audio:" + str(aud_arr)
        input_a.append(('video_creation/audio/' + str(aud_arr[i]), None))
    print str(input_a)

    ff = ffmpy.FFmpeg(inputs = OrderedDict(input_a), outputs = {output_fname : None})
    ff.run()


if __name__ == '__main__':
    print str(0)
