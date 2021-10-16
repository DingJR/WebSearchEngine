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
globalDirPath="index//"

if __name__ == "__main__":
    indexGroup = []
    for word in string.lowercase:
        indexGroup.append({})
    path=os.path.abspath('.')
    addressFile = "addressname"
    fileList= open(addressFile,"r").readlines()
    #fileList = fileList[1:4]
    startTime = time()
    fileNum=0
    for eachFile in fileList:
        print fileNum
        eachFile = eachFile.strip('\n')
        if re.match('\S*gz$',eachFile):
            f = gzip.GzipFile(mode = "rb", fileobj = open(eachFile,"rb"))
        else :
            f = open(eachFile,"rb")
        for line in f:
            line = re.sub('/<.*/>',' ',line)
            tokens = nltk.word_tokenize(line)
            for word in tokens:
                word = word.lower()
                if word not in stop_words and re.match('^[a-z]+$',word):
                    wordAftLmmtz = WordNetLemmatizer().lemmatize(word,pos='v')
                    #ansWord = PorterStemmer().stem(wordAftLmmtz)
                    ansWord = wordAftLmmtz
                    num = ord(ansWord[0]) - ord('a')
                    subIndex = indexGroup[num]
                    if subIndex.get(ansWord) :
                        if not ((subIndex[ansWord])[-1] ==  fileNum):
                            (subIndex[ansWord]).append(fileNum)
                    else :
                        subIndex[ansWord] = [fileNum]
        f.close()
        fileNum += 1
    indexNum = 0
    for thesaurus in indexGroup:
        ansArray = []
        for (k,v) in thesaurus.items():
            ansArray.append((k,v))
        SortedArray = sorted(ansArray, key = lambda x: (x[0]))
        fileName = str(globalDirPath+str(chr(indexNum+ord('a'))))
        indexNum += 1
        f = open(fileName,"wb")
        for (k,v) in SortedArray:
            for ele in k:
                f.write(bytes(ele))
            pre = -1
            for ele in v:
                bl = []
                writeIn = ele-pre
                while writeIn>0:
                    bl.append(writeIn%128)
                    writeIn = writeIn/128
                pre = ele
                bl[0] += 128
                if len(bl) == 1:
                    bl.append(128)
                else :
                    bl[len(bl)-1] += 128
                for ele in reversed(bl):
                    f.write(bytes(chr(ele)))
        f.close()
        del ansArray
        del thesaurus
