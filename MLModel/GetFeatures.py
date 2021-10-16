import nltk
import os
import gzip
import re
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from time import *
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import thread
from nltk.stem.porter import PorterStemmer
import thread
import psutil
import math
import multiprocessing as mp
stop_words = set(stopwords.words('english'))
mystopwords = set(['for','to','in','of','a','the','with','andr','or','s'])
global_train_dir = "./2017TAR/training/extracted_data/"
global_train_result = "./2017TAR/training/qrels/train.abs.rels"
global_test_dir = "./2017TAR/testing/extracted_data/"
NumMapFile = []

def Read_Query(dataDir,path):
    queryFile = open(path,"r")
    queryDir= []
    allquery = []
    for ele in queryFile.readlines():
        ele = ele.strip()
        docfile = dataDir +ele+".title"
        doc = open(docfile,"r")
        queryWords = []
        sentence = ((doc.readlines())[0]).strip()
        tokens =  nltk.word_tokenize(sentence)
        aftertokens = []
        for i in range(len(tokens)):
            if i == 0 :
                queryDir.append(tokens[0])
                continue;
            word = (tokens[i]).lower()
            if word not in stop_words and re.match('^[a-z]+$',word) and word not in mystopwords:
                aftertokens.append(str(WordNetLemmatizer().lemmatize(word,pos='v')))
        allquery.append(aftertokens)
    return queryDir,allquery

def Read_File_Length( fileName):
    filepath = "doc/" +  fileName + "/" + "fileLen" 
    f = open(filepath,"r")
    fileLens = {}
    for ele in f.readlines():
        ele = ele.split()
        fileLens[int(ele[0])] = int(ele[1])
    return fileLens

def Read_Query_Dir(fileName):
    filepath = "doc/" +  fileName + "/"
    fileInfo = {}
    folder = os.listdir(filepath)
    ff = []
    for ele in folder:
        if ele != "fileLen":
            fileInfo[int(ele)] = []
    return fileInfo

def DecodeFile(fileName,wordList):
    thesaurus = {}
    wordNum = {}
    with open(fileName,"r") as f:
        for line in f.readlines():
            wordArticle = line.split()
            word = wordArticle[0]
            if not (word in wordList):
                continue;
            thesaurus[word] = []
            temp = thesaurus[word]
            num = 0
            i=1
            while i < len(wordArticle):
                ele = (NumMapFile[int(wordArticle[i])] , int(wordArticle[i+1]))
                num += int(wordArticle[i+1])
                temp.append(ele)
                i += 2
            wordNum[word] = num
    return thesaurus,wordNum

def GetFileNum(words):
    #for i in range(len(words)):
    #    words[i] = str(WordNetLemmatizer().lemmatize(words[i]))
    words = list(set(words))
    initList = []
    queryDic = {}
    wordNum = {}
    for word in words:
        initList.append(word[0])
        queryDic[word] = []
    initList = list(set(initList))
    for Initial in initList:
        thesaurus ,twordNum = DecodeFile("index/"+Initial,words)
        for word in words:
            if word[0] == Initial and thesaurus.get(word):
                queryDic[word] = thesaurus[word]
                wordNum[word] = twordNum[word]
    return queryDic,wordNum

'''
    Some functions used to calculate doc-query features
    tf
    idf
    BM25
    Vector Space Model
    Stastical Language Model
'''

'''
    @paras: tf   :term_number
            mva  :term_number_max_value
'''
def TF(tf,mva):
    return 0.2+0.8*tf/mva

'''
    @paras :N   :quantity of files
            n   :term number
'''
def IDF(N,n):
    return math.log(1+N/n)

'''
    @paras: mva  :term_number_max_value
            q    :term_number
            avgdl:term_number_average_value
            D    :file length * idf
'''
def BM(mva,q,avgdl,D):
    k = 1.2
    b = 0.75
    return TF(q,mva)*(k+1.0)/(TF(q,mva)+k*(1-b+b*D/avgdl))

'''
    @paras: tf : term number
            N  : file length
            pwc: wordNum/allfilelength
'''
def Dirichlet_Priors(tf,N,pwc):
    u = 0.5
    return (tf + u*pwc)/(float(N) + u)



'''
    Get features
    @paras: fileInfo:dics(keys:filenumber) 
            query: a list containing query words
            fileLen: dics(keys:filenumber value:file length)
'''

def getDocFeature(fileInfo,query,fileLens):
    queryDic,wordNum = GetFileNum(query)
    qlen = len(query)
    for key in fileInfo.keys():
        (fileInfo[key])= [0 for i in range(4)]
    allLength = 79497169
    quantityFiles = 235502
    length = 0
    for i in range(len(query)):
        word = query[i]
        q_file_length = 0
        if not queryDic.get(word):
            continue
        maxvalue=0                #max term number
        for val in queryDic[word]:
            maxvalue =  max(maxvalue,val[1])
            q_file_length += fileLens[val[0]] 
        idf = IDF(quantityFiles,len(queryDic[word]))
        avgvalue=float(q_file_length)/float(len(queryDic[word]))
        pwc = float(wordNum[word])/float(allLength)
        visit = {}
        for val in queryDic[word]:
            visit[val[0]] = val[1]
            if fileInfo.get(val[0]):
                fileInfo[val[0]][1] += TF(val[1],maxvalue)*idf
                fileInfo[val[0]][2] += BM(maxvalue,val[1],avgvalue,fileLens[val[0]])*idf
                fileInfo[val[0]][3] += float(val[1])/float(fileLens[val[0]])
        for k in fileInfo.keys():
            if visit.get(k):
                fileInfo[k][0] += math.log(Dirichlet_Priors(visit[k],fileLens[k],pwc))*idf
            else:
                fileInfo[k][0] += math.log(Dirichlet_Priors(0,fileLens[k],pwc))*idf


def get_Train_Feature():
    queryDir,allquery = Read_Query(global_train_dir,"allquery_fortrain")
    f = "fileLen"
    f = open(f,"r")
    fileLen = json.load(f)
    fileLens = {}
    for (k,v) in fileLen.items():
        fileLens[int(k)] = v 
    for i in range(len(queryDir)):
        print queryDir[i]
        fileInfo = Read_Query_Dir(queryDir[i])
        getDocFeature(fileInfo,allquery[i],fileLens)
        output = "Features/" + queryDir[i]
        output = open(output,"w")
        json.dump(fileInfo,output)

import json
def get_Test_Feature():
    queryDir,allquery = Read_Query(global_test_dir,"allquery_fortest")
    f = "fileLen"
    f = open(f,"r")
    fileLen = json.load(f)
    fileLens = {}
    for (k,v) in fileLen.items():
        fileLens[int(k)] = v 
    for i in range(len(queryDir)):
        print queryDir[i]
        fileInfo = Read_Query_Dir(queryDir[i])
        getDocFeature(fileInfo,allquery[i],fileLens)
        output = "Features/" + queryDir[i]
        output = open(output,"w")
        json.dump(fileInfo,output)

'''
    read file "address" to generate num->filenumber's map
'''
def readFileMap():
    address = "address"
    address = open(address,"r")
    global NumMapFile
    for ele in address.readlines():
        NumMapFile.append(int((ele.split())[2]))

if __name__=="__main__":
    readFileMap()
    get_Train_Feature()
    get_Test_Feature()
