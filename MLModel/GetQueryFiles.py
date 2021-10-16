import os
import re
import gzip
from time import *
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import string
stop_words = set(stopwords.words('english'))
outputFile = "query_files"
wf = open(outputFile,"w")
prePath = None
qf = {}
def GetPathAddress(pathName):
    global  prePath
    if os.path.isdir(pathName):
        os.chdir(os.path.abspath('.')+'/'+pathName)
        prePath = pathName
        if prePath != 'doc':
            qf[prePath] = []
        pathnames = os.listdir('.')
        for name in pathnames:
            GetPathAddress(name)
        os.chdir('..')
    else :
        if pathName != "fileLen":
            (qf[prePath]).append(pathName)

GetPathAddress('doc')
import json
json.dump(qf,wf)
