# -*- coding: utf-8 -*-
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
from simple_wikipedia import *
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

    

    earlyEdu = generateEarlyEdu(param)
    earlyEdu.insert(0, "Early Life")

    pageContent = parseContent(param)

    earlyWork = generateEarlyWork(pageContent)
    earlyWork.insert(0, "Early Work")

    #return earlyWork


    summarized = []

    # for i in range(0, len(pageContent)):
    #     try:
    #         summarized.append([ pageContent[i][0] , summarize(pageContent[i][1]) ])
    #     except:
    #         continue

    summarized.insert(0, earlyEdu)
    summarized.insert(0, earlyWork)
    return callVideoMaker(param, summarized)

def callVideoMaker(name, content):

    id = 0
    #print "Content length: " + str(content)
    arr_audio = []
    total_text = ''
    for each in content:
        if each[1] == '':
            each[1] = '.'
        try:
<<<<<<< HEAD
            tts = gTTS(text = each[1], lang = 'en')
            total_text = total_text + str(each[1])
=======
            print each[1]
            tts = gTTS(text = each[1], lang = 'en-uk')
>>>>>>> 86d04065a1126f653daab4ff1b7ea924db544b0a
        except:
            #print each
            continue

        save_string = "video_creation/audio/%s"%(name + str(id)+".mp3")
        tts.save(save_string)

        arr_audio.append(name + str(id)+".mp3")
        id += 1

    print total_text
    try:
        tts = gTTS(text = total_text, lang = 'en')
    except:
        print "Total text error"

    save_string = "video_creation/audio/%s"%(name + "_total.mp3")
    tts.save(save_string)

    arr_arr_images = []
    for each in content:
        topic = each[0]

        query_topic = name + " " + topic

        bing_image = PyBingImageSearch(BING_API_KEY, query_topic, image_filters= IMAGE_FILTER)
        first_fifty_result= bing_image.search(limit=7, format='json') #1-50
        #print "DOES BING RETURN ANYTHING????" + str(first_fifty_result)

        media = [x.media_url for x in first_fifty_result]

        arr_arr_images.append(media)
    vid_res = ''
    vid_res = video_maker.make_total_vid(name, arr_arr_images, arr_audio)
    #try:
    #    vid_res = video_maker.make_total_vid(name, arr_arr_images, arr_audio)
    #except:


    video_maker.delete_audio_files()
    return vid_res
#def make_total_vid(name, arr_arr_images, arr_audio):

def summarize(content):

    fs = FrequencySummarizer()
    return str(fs.summarize(content, 2))

def generateEarlyEdu(param):
    simple_page = simple_wikipedia.page(param)
    content = simple_page.content
    content = string.replace(content, "====", '|')
    content = string.replace(content, "===", '|')
    content = string.replace(content, "==", '|')
    content = string.replace(content, "=", '|')

    firstSplit = content.split("|")
    pageContent = []
    eduEarlyIndexs = []
    pair = 0
    for i in range(1,len(firstSplit), 2):

        topic = firstSplit[i].strip()
        if re.match('early',topic, re.IGNORECASE):
            eduEarlyIndexs.append(pair)
        if re.match('education',topic, re.IGNORECASE):
            eduEarlyIndexs.append(pair)

        content = firstSplit[i+1].strip()
        pageContent.append([topic.encode('ascii', 'ignore'), content.encode('ascii', 'ignore')])
        pair += 1 
    
    retContent = [""+re.sub('\[[^)]*\]', "", pageContent[x][1]) for x in eduEarlyIndexs]
    singular = ""
    for each in retContent:
        singular += each
    return [singular]

def parseContent(param):

    page = wikipedia.page(param)
    content = page.content

    content = string.replace(content, "====", '|')
    content = string.replace(content, "===", '|[Parent Node]')
    content = string.replace(content, "==", '|[Parent Node]')
    content = string.replace(content, "=", '|')

    #return content
    firstSplit = content.split("|")

    pageContent = []
    #reachedEarly = False
    for i in range(1,len(firstSplit), 2):

        topic = firstSplit[i].strip()
        #if re.match('early',topic, re.IGNORECASE):
            #reachedEarly = True
        #if reachedEarly:
        content = firstSplit[i+1].strip()
        pageContent.append([topic.encode('ascii', 'ignore'), content.encode('ascii', 'ignore')])
    return pageContent

def generateEarlyWork(content):
    workRelatedString = ""
    keyWords = ['employ', 'work', 'career', 'taught', 'directed', 'elected', 'director', 'teacher', 'professor', 'lawyer', 'worker', 'employer', 'intern', 'internship']
    contentKeys = ['career', 'early']
    sectionIndex = 0
    for section in content:
        #print section[0], re.match("\[Parent Node\]",section[0], re.IGNORECASE)
        chainOut = False;
        if re.match("\[Parent Node\]",section[0], re.IGNORECASE):
            for cont in contentKeys:
                for substr in section[0].split():
                    if re.match(cont,substr, re.IGNORECASE):
                        workRelatedString += naiveSearch(content, sectionIndex, keyWords)
                        chainOut = True
                        break
                if chainOut:
                    break
                
        sectionIndex += 1
    return [workRelatedString]

def naiveSearch(content, sectionIndex, triggers):
    retScentence = ""

    scentences = split_into_sentences(content[sectionIndex][1])
    for scentence in scentences:
        for key in triggers:
            if findWholeWord(key)(scentence):
                retScentence += scentence

    childIndices = findChildren(content, sectionIndex)
    for child in childIndices:
        scentences = split_into_sentences(content[child][1])
        for scentence in scentences:
            for key in triggers:
                if findWholeWord(key)(scentence):
                    retScentence += scentence

    return retScentence

def findChildren(content, sectionIndex):
    childIndices = []
    for i in range(sectionIndex + 1, len(content)):
        if re.match("\[Parent Node\]",content[i][0], re.IGNORECASE):
            print childIndices
            return childIndices
        else:
            childIndices.append(i)



#Globals for Scentence Splitting
caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
if __name__ == '__main__':
    #app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
	app.run(debug=True)
