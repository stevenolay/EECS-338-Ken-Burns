
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
     abort, render_template, flash, jsonify

from jinja2 import Environment, FileSystemLoader
import os

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

BING_API_KEY = 'wrtWDMR91PXsFFEHRYN1ZQSObkZMFvHJRljl6zyNiCI'
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

    page = wikipedia.page(tempParam)
    content = page.content

    content = string.replace(content, "====", '|')
    content = string.replace(content, "===", '|')
    content = string.replace(content, "==", '|')
    content = string.replace(content, "=", '|')

    firstSplit = content.split("|")

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

    summarized = []

    for i in range(0, len(pageContent)):
        try:
            summarized.append([ pageContent[i][0] , summarize(pageContent[i][1]) ])
        except:
            continue

    img = '<img src="%s" alt="Mountain View" style="width:304px;height:228px;">'%(page.images[3])

    #return str(summarized)
    return callVideoMaker(param, summarized)

def callVideoMaker(name, content):

    id = 0
    arr_audio = []
    for each in content:
        tts = gTTS(text = each[1], lang = 'en')
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

        media = [x.media_url for x in first_fifty_result]

        arr_arr_images.append(media)

    video_maker.make_total_vid(name, arr_arr_images, arr_audio)
    return str("success")
#def make_total_vid(name, arr_arr_images, arr_audio):




def summarize(content):

    fs = FrequencySummarizer()
    return str(fs.summarize(content, 2))

if __name__ == '__main__':
    #app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
	app.run(debug=True)
