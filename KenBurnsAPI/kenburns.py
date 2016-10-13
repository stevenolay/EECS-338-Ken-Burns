
import sys
from sys import path
import ast
import json
import string
import copy
import io
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


# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def show_vanilla_home():
    return render_template('welcome.html', data = {'status': '', 'article_url': ''}) #Loads Welcome Page

@app.route('/fetch/<param>')
def fetchBio(param):

    tempParam = "Jimmy Hendrix"

    page = wikipedia.page(tempParam)

    firstSplit = page.content.split("==")

    pageContent = [['Summary', firstSplit[0].encode('ascii', 'ignore')]]

    for i in range(1,len(firstSplit), 2):
        topic = firstSplit[i]
        content = firstSplit[i+1]
        pageContent.append([topic.encode('ascii', 'ignore'), content.encode('ascii', 'ignore')])
    summarized = []

    #return  summarize(pageContent[0][1])

    for i in range(0, len(pageContent)):
        try:
            pageContent[i][0] = re.sub('[!@#$=\/]', '', pageContent[i][0].rstrip("\n"))
            pageContent[i][1] = re.sub('[!@#$=\/]', '', pageContent[i][1].rstrip("\n"))

            summarized.append([ pageContent[i][0] , summarize(pageContent[i][1]) ])
        except:
            continue
    img = '<img src="%s" alt="Mountain View" style="width:304px;height:228px;">'%(page.images[1])
    return str(summarized) 
    
def summarize(content):

    fs = FrequencySummarizer()
    return str(fs.summarize(content, 2))

if __name__ == '__main__':
    #app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
	app.run(debug=True)
