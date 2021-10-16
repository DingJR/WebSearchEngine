import nltk
import math
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import re
import os
import string
stop_words = set(stopwords.words('english'))
globalPathName = None
allFileLen = 0
def DecodeFile(fileName,wordList):
    thesaurus = {}
    wordNum = {}
    print wordList
    with open(fileName,"r") as f:
        for line in f.readlines():
            wordArticle = line.split()
            word = wordArticle[0]
            if not (word in wordList):
                continue;
            thesaurus[word] = []
            temp = thesaurus[word]
            num = 0
            pre = 0
            i=1
            while i < len(wordArticle):
                ele = (int(wordArticle[i])+pre , int(wordArticle[i+1]))
                num += int(wordArticle[i+1])
                pre = pre + int(wordArticle[i])
                temp.append(ele)
                i += 2
            wordNum[word] = num
    return thesaurus,wordNum

def GetFileNum(words):
    for i in range(len(words)):
        words[i] = str(WordNetLemmatizer().lemmatize(words[i]))
    words = list(set(words))
    initList = []
    queryDic = {}
    wordNum = {}
    for word in words:
        initList.append(word[0])
        queryDic[word] = []
    initList = list(set(initList))
    for Initial in initList:
        thesaurus ,twordNum = DecodeFile(globalPathName+Initial,words)
        for word in words:
            if word[0] == Initial and thesaurus.get(word):
                queryDic[word] = thesaurus[word]
                wordNum[word] = twordNum[word]
    return queryDic,wordNum

def Linear_Interpolation(tf,N,pwc):
    alpha = 0.3
    return alpha * float(tf) / float(N)  + (1 - alpha) * pwc

def Dirichlet_Priors(tf,N,pwc):
    u = 0.8
    return (tf + u*pwc)/(float(N) + u)

def Add_One(tf,N):
    u = 562916
    return (tf + 1)/(float(N) + u)

def Absolute_Discounting(tf,N,cf,M,uNum):
    sigma = 0.7
    return (max(tf/float(N)-sigma,0) + sigma*uNum*tf/float(N))/float(N)

def p_w_D(Type,tf,N,pwc):
    if Type == "L":
        return Linear_Interpolation(tf,N,pwc)
    elif Type == "D":
        return Dirichlet_Priors(tf,N,pwc)
    elif Type == "A":
        return Add_One(tf,N)

iii = 0
def SLM(sentence,N,fileLenList):
        print allFileLen
        thesaurus, wordNum = GetFileNum(sentence)
        global iii
        print iii
        iii += 1
        Relevant_File = {}
        for (k,v) in thesaurus.items():
            for vv in v:
                Relevant_File[vv[0]] = 0.0
        for (k,v) in thesaurus.items():
            if len(v) == 0:
                continue
            '''
            maxValue = 0
            wordLen = 0
            for vv in v:
                maxValue = max(vv[1],maxValue)
                wordLen += vv[1]
                '''
            wn = wordNum[k]
            pwc = float(wn)/float(allFileLen)
            fileRank = {}
            Type = "A"
            for vv in v:
                if fileRank.get(vv[0]):
                    fileRank[vv[0]] +=  math.log(p_w_D(Type,vv[1],fileLenList[vv[0]],pwc))
                else:
                    fileRank[vv[0]]  =  math.log(p_w_D(Type,vv[1],fileLenList[vv[0]],pwc))

            for kk in Relevant_File.keys():
                if fileRank.get(kk):
                    Relevant_File[kk] += fileRank[kk]
                else :
                    Relevant_File[kk] += math.log(p_w_D(Type,0,fileLenList[kk],pwc))
        return Relevant_File

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
    fileLenList = GetFileLen()
    allFileLen = sum(fileLenList)
    outputFile = "SLMoutput"
    inputFile = "input"
    f = open(outputFile,"w")
    inf = open(inputFile,"r")
    for sentence in inf.readlines():
        sentence = sentence.split()
        Num = sentence[0]
        result = SLM(sentence[1:len(sentence)],len(flNumList),fileLenList)
        ans = sorted(result.items(), key=lambda d:d[1],reverse = True)
        nn = 0
        for itm in ans[0:1000]:
            print >>f,Num,"0",(flNumList[itm[0]]),nn,itm[1],"IDIOT"
            nn += 1
#print GetFileName(GetFileNum(sentence))
