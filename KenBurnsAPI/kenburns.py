
import sys
from sys import path
import ast
import json
import string
import copy
import io
import random

#Imports for Audio and Images
from gtts import gTTS
from py_bing_search import PyBingImageSearch

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify, send_from_directory

from jinja2 import Environment, FileSystemLoader
import os, glob

import re, urllib2

import requests
import random

# EXTERNAL API IMPORTS
import wikipedia
from Summary import *
from video_creation import video_maker
#from video_maker import *


# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
MEDIA_FOLDER = 'video_creation/output_videos'

# BING_API_KEY = 'wrtWDMR91PXsFFEHRYN1ZQSObkZMFvHJRljl6zyNiCI'
BING_API_KEY = 'b4lZYRDZJ/ya1EhblueNnTukTRxUBArSz66fIfz0lys'

IMAGE_FILTER = 'Size:Large+Color:Color+Style:Photo'

# create our little application :)
app = Flask(__name__)

app.config.from_object(__name__)

@app.route('/')
def show_vanilla_home():
    return render_template('index.html') #Loads Welcome Page


@app.route('/fetch/<param>')
def fetchBio(param):

    tempParam = "Barack Obama"

    split_name = param.split(' ')
    vid_name = ''
    for i in range(0, len(split_name)):
        vid_name = vid_name + str(split_name[i])
        if i != (len(split_name) - 1):
            vid_name = vid_name + '_'

    vid_name = vid_name + '_test.mp4'
    #check if the video of the person exists already -> then don't make video
    vid_exists = False
    curr_dir = os.getcwd()
    dir_mp4 = str(curr_dir) + '/static/output_videos/*.mp4'
    vids = glob.glob(dir_mp4)
    for f_name in vids:
        # print "NAME:" + str(f_name)
        if vid_name in f_name:
            print "TRUUUUUUUUUUu"
            vid_exists = True
            return vid_name
    print "Did not find previously made video - making new bio"
    page = wikipedia.page(param)
    content = page.content



    content = string.replace(content, "====", '|')
    content = string.replace(content, "===", '|')
    content = string.replace(content, "==", '|')
    content = string.replace(content, "=", '|')

    firstSplit = content.split("|")
    # print "FIRST SPLIT: " + str(firstSplit)
    #pageContent = [['Summary', firstSplit[0].encode('ascii', 'ignore')]]
    pageContent = []
    #reachedEarly = False
    for i in range(1,len(firstSplit), 2):

        topic = firstSplit[i].strip()
        #if re.match('early',topic, re.IGNORECASE):
            #reachedEarly = True
        #if reachedEarly:
        content = firstSplit[i+1].strip()
        pageContent.append([topic.encode('ascii', 'ignore'), content.encode('ascii', 'ignore')])

    #print "PAGE CONTENT LEN: " + str(len(pageContent))
    summarized = []

    for i in range(0, len(pageContent)):
        try:
            summarized.append([ pageContent[i][0] , summarize(pageContent[i][1]) ])
        except:
            continue

    #print "summarized len: " + str(len(summarized))
    img = '<img src="%s" alt="Mountain View" style="width:304px;height:228px;">'%(page.images[3])

    #return str(summarized)
    return callVideoMaker(param, summarized)

def callVideoMaker(name, content):

    id = 0
    #print "Content length: " + str(content)
    arr_audio = []

    for each in content:
        if each[1] == '':
            each[1] = '.'
        try:
            tts = gTTS(text = each[1], lang = 'en')
        except:
            print each

        save_string = "video_creation/audio/%s"%(name + str(id)+".mp3")
        tts.save(save_string)

        arr_audio.append(name + str(id)+".mp3")
        id += 1

    arr_arr_images = []
    for each in content:
        topic = each[0]

        query_topic = name + " " + topic

        bing_image = PyBingImageSearch(BING_API_KEY, query_topic, image_filters= IMAGE_FILTER)
        first_fifty_result= bing_image.search(limit=50, format='json') #1-50
        #print "DOES BING RETURN ANYTHING????" + str(first_fifty_result)

        media = [x.media_url for x in first_fifty_result]

        arr_arr_images.append(media)
    vid_res = ''
    # vid_res = video_maker.make_total_vid(name, arr_arr_images, arr_audio)
    try:
        vid_res = video_maker.make_total_vid(name, arr_arr_images, arr_audio)
    except:
        print "video maker failed"

    video_maker.delete_audio_files()
    return vid_res
#def make_total_vid(name, arr_arr_images, arr_audio):




def summarize(content):

    fs = FrequencySummarizer()
    return str(fs.summarize(content, 2))

if __name__ == '__main__':
    #app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
	app.run(debug=True)
