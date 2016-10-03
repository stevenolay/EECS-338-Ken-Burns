import sys, os, glob
import cv2
import numpy
from matplotlib import pyplot 
import math, random
from PIL import Image
from gtts import gTTS

def test_string():
    test_str = "Northwestern 38 Iowa 31 let's go Northwestern! Bruh bruh lmao lol gotem gg"
    return test_str

def create_audio(input_str):
    tts = gTTS(text = input_str, lang = 'en')
    tts.save('test.mp3')


if __name__ == '__main__':
    stringy = test_string()
    create_audio(stringy)
