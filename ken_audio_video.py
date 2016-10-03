import sys, os, glob, math, time
import cv2
import numpy as np
from auto_ken_runner import *
from ken_audio import *
import moviepy.editor as mp

def combine_av(vid_name, audio_name):
   vid = mp.VideoFileClip(vid_name)
   aud = mp.AudioFileClip(audio_name)
   vid.set_audio(aud.set_duration(vid.duration))
   vid.write_videofile("av_test.mp4")


if __name__ == '__main__':
    combine_av("combo_new_vid.avi", "test.mp3")
