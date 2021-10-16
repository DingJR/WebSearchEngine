import nltk
import os
import gzip
import re
import threading
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from time import *
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import thread
from nltk.stem.porter import PorterStemmer
import psutil
import multiprocessing as mp

stop_words = set(stopwords.words('english'))
mylock = threading.Lock()
path = None
path=os.path.abspath('.')

def readfile(threadName,num):
    pid = os.getpid()
    print pid
    f=None
    globalOutputPath = "./doc/"
    inputPath = None
    global path
    inputPath = path
    alldic = ["docs.tesing/topics_raw_docs/","docs.training/topics_raw_docs/"]
    dicList = []
    ele = alldic[num]
    print ele
    mylock.acquire()
    temp = os.listdir("./"+ele)
    for e in temp:
        if not os.path.exists(globalOutputPath+e.strip('.')):
            os.mkdir(globalOutputPath+e.strip('.'))
        dicList.append(ele+e.strip('.'))
    mylock.release()
    print dicList
    print ""
    for foldername in dicList:
        print foldername
        inputPath = path +'/'+ foldername +'/'
        outputPath = None
        outputPath = globalOutputPath + (foldername.split('/'))[2] +'/'
        pathList = os.listdir(inputPath)
        for eachFile in pathList:
            print eachFile
            #f = gzip.GzipFile(mode = "rb", fileobj = open(eachFile,"rb"))
            if re.match('\S*gz$',eachFile):
                continue;
            with open(inputPath+eachFile,"r") as f:
                thesaurus = {}
                for line in f.readlines(): 
                    line = re.sub('/<.*/>',' ',line)
                    tokens = None
                    try:
                        tokens = nltk.word_tokenize(line)
                    except:
                        continue;
                    for word in tokens:
                        word = word.lower()
                        if word not in stop_words and re.match('^[a-z]+$',word):
                            wordAftLmmtz = WordNetLemmatizer().lemmatize(word,pos='v')
                            #ansWord = PorterStemmer().stem(wordAftLmmtz)
                            ansWord = wordAftLmmtz
                            if thesaurus.get(ansWord) :
                                thesaurus[ansWord] += 1
                            else :
                                thesaurus[ansWord] = 1
                print outputPath+eachFile
                out = open(outputPath+eachFile,"w")
                ansArray = []
                for (k,v) in thesaurus.items():
                    ansArray.append((k,v))
                SortedArray = sorted(ansArray, key = lambda x: (x[1]))
                for (k,v) in SortedArray:
                    print>>out ,k,v
                out.close()

if __name__ == "__main__":
    processes = [mp.Process(target=readfile, args=("thread", x)) for x in range(2)]
    for p in processes:
        p.start()

    for p in processes:
        p.join()






