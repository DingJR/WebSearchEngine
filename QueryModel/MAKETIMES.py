import nltk
import os
import gzip
import re
from time import *
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import string
import struct
stop_words = set(stopwords.words('english'))
globalDirPath="times/"

def GetTimes(initial,fileList):
    path=os.path.abspath('.')
    startTime = time()
    fileNum=0
    thesaurus = {}
    print initial
    for eachFile in fileList:
        f = (eachFile.split())[0]
        f = open(f,"r")
        fLines = f.readlines()
        for line in fLines:
            words = line.split()
            for ansWord in words:
                if ansWord[0] == initial:
                    if thesaurus.get(ansWord) :
                        if not ((thesaurus[ansWord])[-1][0] ==  fileNum):
                            (thesaurus[ansWord]).append([fileNum,1])
                        else:
                            (thesaurus[ansWord])[-1][1] += 1
                    else :
                        thesaurus[ansWord] = [[fileNum,1]]
        f.close()
        fileNum += 1
    indexNum = 0

    ansArray = []
    for (k,v) in thesaurus.items():
        ansArray.append((k,v))
    SortedArray = sorted(ansArray, key = lambda x: (x[0]))
    fileName = str(globalDirPath+initial)
    indexNum += 1
    f = open(fileName,"w")
    for (k,v) in SortedArray:
        f.write(k+' ')
        pre = 0
        for vv in v:
            f.write(str(vv[0]-pre)+' '+str(vv[1])+' ')
            pre = vv[0]
        f.write('\n')
    f.close()
    del ansArray
    del thesaurus

if __name__ == "__main__":
    indexGroup = []
    for word in string.lowercase:
        indexGroup.append({})
    addressFile = "addressname"
    fileList= open(addressFile,"r").readlines()
    for i in range(len(indexGroup)):
        GetTimes(chr(i+ord('a')),fileList)
