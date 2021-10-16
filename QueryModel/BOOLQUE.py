import nltk
import math
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import re
import os
import string
stop_words = set(stopwords.words('english'))
globalPathName = None
def DecodeFile(fileName,wordList):
    thesaurus = {}
    with open(fileName,"r") as f:
        for line in f.readlines():
            wordArticle = line.split()
            word = wordArticle[0]
            if not (word in wordList):
                continue;
            thesaurus[word] = []
            temp = thesaurus[word]
            pre = 0
            i = 1
            while i < len(wordArticle):
                ele = int(wordArticle[i])+pre
                pre = ele
                temp.append(ele)
                i += 2
    return thesaurus

def GetFileNum(words):
    words = list(set(words))
    initList = []
    queryDic = {}
    for word in words:
        initList.append(word[0])
        queryDic[word] = []
    initList = list(set(initList))
    print initList
    print words
    for Initial in initList:
        thesaurus = DecodeFile(globalPathName+Initial,words)
        for word in words:
            if word[0] == Initial and thesaurus.get(word):
                queryDic[word] = thesaurus[word]
    return queryDic


def BQ(sentence,N,fileList):
        sentence = sentence.split("OR")
        AllWords = []
        newSentence = []
        for words in sentence:
            words = words.split("AND")
            i = 0
            for i in range(len(words)):
                words[i] = ((words[i].split())[0])
                AllWords.append(words[i])
            newSentence.append(words)
        print newSentence
        thesaurus = GetFileNum(AllWords)
        '''
        fileRank = {}
        for (k,v) in thesaurus.items():
            for vv in v:
                if fileRank.get(vv):
                    fileRank[vv].append(vv)
                else :
                    fileRank[vv] = [vv]
        '''
        ans = set()
        for words in newSentence:
            pans = set(thesaurus[words[0]])
            for word in words:
                print word
                pans = pans.intersection(set(thesaurus[word]))
            ans = pans.union(ans)
        return list(ans)

def GetFileLen():
    fileLen = "fileLen"
    fileLenList = []
    with open(fileLen,"r") as f:
        for i in f.readlines():
            fileLenList.append(int(i.strip('\n')))
    return fileLenList

def GetFileName():
    with open("addressname",'r') as f:
        fileNumNameList = f.readlines()
    results = []
    for ele in fileNumNameList:
        temp = ele.strip('\n')
        results.append((temp.split('/'))[-1])
        #results.append((temp.split('/'))[-1])
    return results

if __name__ == "__main__":
    globalPathName = os.path.abspath('.')+'/'+'times/'
    flNumList = GetFileName()
    outputFile = "output"
    f = open(outputFile,"a")
    fileList = GetFileLen()
    sentence = raw_input()
    sentence = sentence.strip('\n')
    ans = BQ(sentence,len(flNumList),fileList)
    nn = 0
    Num = len(flNumList)
    sortedAnd = sorted(list(ans))
    for itm in sortedAnd:
        #print >>f,Num,"0",(flNumList[itm[0]]),nn,itm[1],"IDIOT"
        print >>f,Num,"0",(flNumList[itm]),nn,itm,"IDIOT"
        nn += 1
#print GetFileName(GetFileNum(sentence))
