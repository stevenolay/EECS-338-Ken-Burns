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

def concat_audio(aud_name, aud_arr):
    #concatenate all the audio into a single file
    output_path = 'audio_no_video/' + aud_name
    f = open(output_path, 'wb')
    # shutil.copyfileobj(open(f))
    input_a = []
    for i in range(0, len(aud_arr)):
        print "HERE"
        input_a.append(('audio/' + str(aud_arr[i]), None))

    ff = ffmpy.FFmpeg(inputs = OrderedDict(input_a), outputs = {output_path: None})
    ff.run()


if __name__ == '__main__':
    #combine_av("yoooo.mp4", "Carrie.mp3", "test_output.mp4")
    concat_audio("test_combo1.mp3", ["test.mp3", "Carrie.mp3"])
