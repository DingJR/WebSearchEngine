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
            i=1
            while i < len(wordArticle):
                ele = (int(wordArticle[i])+pre , int(wordArticle[i+1]))
                pre = pre + int(wordArticle[i])
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

def TF(tf,mva):
    return 0.2+0.8*tf/mva
    #return float(tf)/float(mva)


def BM(mva,q,avgdl,D):
    k = 1.2
    b = 0.75
    return TF(q,mva)*(k+1.0)/(TF(q,mva)+k*(1-b+b*D/avgdl))

def IDF(N,n):
    return math.log(1+N/n)

def TF_IDF(sentence,N,fileLenList):
        thesaurus = GetFileNum(sentence)
        fileRank = {}
        for (k,v) in thesaurus.items():
            maxValue = 0
            aveLen = 0.0
            for vv in v:
                maxValue = max(vv[1],maxValue)
                aveLen += fileLenList[vv[0]]
            aveLen /= float(len(v))
            for vv in v:
                if fileRank.get(vv[0]):
                    #fileRank[vv[0]] += TF(vv[1],maxValue)*IDF(len(fileLenList),len(v))
                    fileRank[vv[0]] +=BM(maxValue,vv[1],aveLen,fileLenList[vv[0]])*IDF(len(fileLenList),len(v))
                else :
                    #fileRank[vv[0]] = TF(vv[1],maxValue)*IDF(len(fileLenList),len(v))
                    fileRank[vv[0]] = BM(maxValue,vv[1],aveLen,fileLenList[vv[0]])*IDF(len(fileLenList),len(v))
        return fileRank

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
    outputFile = "trec_eval.9.0/output"
    inputFile = "input"
    f = open(outputFile,"w")
    inf = open(inputFile,"r")
    fileLenList = GetFileLen()
    for sentence in inf.readlines():
        sentence = sentence.split()
        Num = sentence[0]
        result =  TF_IDF(sentence[1:len(sentence)],len(flNumList),fileLenList)
        ans = sorted(result.items(), key=lambda d:d[1],reverse = True)
        nn = 0
        for itm in ans[0:1000]:
            print >>f,Num,"0",(flNumList[itm[0]]),nn,itm[1],"IDIOT"
            nn += 1
#print GetFileName(GetFileNum(sentence))
