
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
#path.append("static/Summary.py")
#print path

#import Summary
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

    pageContent = [['Summary', firstSplit[0]]]

    for i in range(1,len(firstSplit), 2):
        topic = firstSplit[i]
        content = firstSplit[i+1]
        pageContent.append([topic, content])


    #summarize(pageContent[2][0], pageContent[2][1])

    #return summarize(' '.join(pageContent[4][0].split()), ' '.join(pageContent[4][1].split()))
    #return str(pageContent[6][1])
    return summarize("Jimmy Hendrix", 'In March 1964, Hendrix recorded the two-part single "Testify" with the Isley Brothers. Released in June, it failed to chart. In May, he provided guitar instrumentation for the Don Covay song, "Mercy Mercy". Issued in August by Rosemart Records and distributed by Atlantic, the track reached number 35 on the Billboard chart. Hendrix toured with the Isleys during much of 1964, but near the end of October, after growing tired of playing the same set every night, he left the band. Soon afterward, Hendrix joined Little Richards touring band, the Upsetters. During a stop in Los Angeles in February 1965, he recorded his first and only single with Richard, "I Dont Know What You Got (But Its Got Me)", written by Don Covay and released by Vee-Jay Records. Richards popularity was waning at the time, and the single peaked at number 92, where it remained for one week before dropping off the chart. Hendrix met singer Rosa Lee Brooks while staying at the Wilcox Hotel in Hollywood, and she invited him to participate in a recording session for her single, which included the Arthur Lee penned "My Diary" as the A-side, and "Utee" as the B-side. Hendrix played guitar on both tracks, which also included background vocals by Lee. The single failed to chart, but Hendrix and Lee began a friendship that lasted several years; Hendrix later became an ardent supporter of Lees band, Love. In July 1965, on Nashvilles Channel 5 Night Train, Hendrix made his first television appearance. Performing in Little Richards ensemble band, he backed up vocalists Buddy and Stacy on "Shotgun". The video recording of the show marks the earliest known footage of Hendrix performing. Richard and Hendrix often clashed over tardiness, wardrobe, and Hendrixs stage antics, and in late July, Richards brother Robert fired him. He then briefly rejoined the Isley Brothers, and recorded a second single with them, Move Over and Let Me Dance" backed with Have You Ever Been Disappointed Later that year, he joined a New York-based R&B band, Curtis Knight and the Squires, after meeting Knight in the lobby of a hotel where both men were staying. Hendrix performed with them for eight months. In October 1965, he and Knight recorded the single, "How Would You Feel" backed with "Welcome Home" and on October 15, Hendrix signed a three-year recording contract with entrepreneur Ed Chalpin. While the relationship with Chalpin was short-lived, his contract remained in force, which later caused legal and career problems for Hendrix. During his time with Knight, Hendrix briefly toured with Joey Dee and the Starliters, and worked with King Curtis on several recordings including Ray Sharpes two-part single, "Help Me". Hendrix earned his first composer credits for two instrumentals, "Hornets Nest" and "Knock Yourself Out", released as a Curtis Knight and the Squires single in 1966. Feeling restricted by his experiences as an R&B sideman, Hendrix moved to New York Citys Greenwich Village in 1966, which had a vibrant and diverse music scene. There, he was offered a residency at the Cafe Wha? on MacDougal Street and formed his own band that June, Jimmy James and the Blue Flames, which included future Spirit guitarist Randy California. The Blue Flames played at several clubs in New York and Hendrix began developing his guitar style and material that he would soon use with the Experience. In September, they gave some of their last concerts at the Cafe au Go Go, as John Hammond Jr.')


def summarize(title, content):

    fs = FrequencySummarizer()
    return str(fs.summarize(content, 2))

from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest

class FrequencySummarizer:
  def __init__(self, min_cut=0.1, max_cut=0.9):
    """
     Initilize the text summarizer.
     Words that have a frequency term lower than min_cut 
     or higer than max_cut will be ignored.
    """
    self._min_cut = min_cut
    self._max_cut = max_cut 
    self._stopwords = set(stopwords.words('english') + list(punctuation))

  def _compute_frequencies(self, word_sent):
    """ 
      Compute the frequency of each of word.
      Input: 
       word_sent, a list of sentences already tokenized.
      Output: 
       freq, a dictionary where freq[w] is the frequency of w.
    """
    freq = defaultdict(int)
    for s in word_sent:
      for word in s:
        if word not in self._stopwords:
          freq[word] += 1
    # frequencies normalization and fitering
    m = float(max(freq.values()))
    for w in freq.keys():
      freq[w] = freq[w]/m
      if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
        del freq[w]
    return freq

  def summarize(self, text, n):
    """
      Return a list of n sentences 
      which represent the summary of text.
    """
    sents = sent_tokenize(text)
    assert n <= len(sents)
    word_sent = [word_tokenize(s.lower()) for s in sents]
    self._freq = self._compute_frequencies(word_sent)
    ranking = defaultdict(int)
    for i,sent in enumerate(word_sent):
      for w in sent:
        if w in self._freq:
          ranking[i] += self._freq[w]
    sents_idx = self._rank(ranking, n)    
    return [sents[j] for j in sents_idx]

  def _rank(self, ranking, n):
    """ return the first n sentences with highest ranking """
    return nlargest(n, ranking, key=ranking.get)

if __name__ == '__main__':
    #app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
	app.run(debug=True)
