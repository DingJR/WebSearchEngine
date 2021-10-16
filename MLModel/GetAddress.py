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
Num = 0
outputFile = "address"
wf = open(outputFile,"w")
prePath = None
def GetPathAddress(pathName):
    global  Num
    global  prePath
    if os.path.isdir(pathName):
        os.chdir(os.path.abspath('.')+'/'+pathName)
        prePath = os.path.abspath('.')+'/'
        pathnames = os.listdir('.')
        for name in pathnames:
            GetPathAddress(name)
        os.chdir('..')
    else :
        if pathName != "fileLen":
            print>>wf,Num,os.path.abspath('.')+"/"+pathName,pathName
            Num += 1

GetPathAddress('doc')
