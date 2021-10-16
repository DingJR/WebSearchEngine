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
pathList = []
globalpath = None
Num = 0
def GetTopic(pathName):
        eachFile = pathName
        f = open(eachFile,"r")
        print eachFile
        ii = 0
        ff = f.readlines()
        Num = 151
        name = None
        line = None
        wf = None
        writein = ''
        outputName = globalpath+"output"
        wf = open(outputName,"w")
        for line in ff:
            if line[0:7] == '<title>':
                line = re.sub('<.*?>','',line)
                line = re.sub('Topic:','',line)
                print line
                tokens = nltk.word_tokenize(line)
                for word in tokens:
                    word = word.lower()
                    if word not in stop_words and re.match('^[a-z]+$',word):
                        wordAftLmmtz = WordNetLemmatizer().lemmatize(word,pos='v')
                        #ansWord = PorterStemmer().stem(wordAftLmmtz)
                        ansWord = wordAftLmmtz
                        writein += ansWord+' '
                print >>wf,Num,writein
                Num += 1
                writein = ''
        wf.close()

globalpath = os.path.abspath('.')+'/doc/'
print globalpath
GetTopic(os.path.abspath('.')+'/'+'topics(1).151-200')
