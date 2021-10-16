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
paras = None

def CosinScore(sentence,N,fileLenList,para,num,stdRel,flnum2name,newpara):
        print num
        fileName = "BM/"+str(num)
        alpha = 1.0
        beta  = 0.75
        gamma = 0.25
        f = open(fileName, "r")
        fLine = f.readlines()

        notRela = 0
        NR = [0.0 for i in sentence]
        Rela    = 0
        R = [0.0 for i in sentence]
        filerank = {}
        for l in fLine:
            line = l.split()
            fnum = int(line[0])
            filerank[fnum] = 0.0
            ii = 0
            for p in line[1:]:
                filerank[fnum] += float(p)*para[ii]
                ii += 1
            ii = 0
            if flnum2name[fnum] in stdRel:
                Rela += 1
                for p in line[1:]:
                    R[ii] += float(p)
                    ii += 1
            else :
                for p in line[1:]:
                    NR[ii] += float(p)
                    ii += 1
                notRela += 1
        print Rela,notRela
        for i in range(len(sentence)):
            newpara[i] = alpha * para[i]
            if Rela != 0 :
                newpara[i] +=  beta*R[i]/float(Rela)
            if notRela != 0 :
                newpara[i] +=  gamma*NR[i]/float(notRela)
        return filerank

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

    filename = "vectorTable"
    paraf = open(filename,"r")
    paras = paraf.readlines()
    for i in range(len(paras)):
        paras[i] = (paras[i]).split()
        for j in range(len(paras[i])):
            paras[i][j] = float(paras[i][j])
    paraf.close()


    releFile = "RelavantFile"
    outputFile = "BMoutput"
    inputFile = "input"
    filename = "vectorTable"
    f = open(outputFile,"w")
    inf = open(inputFile,"r")
    rfile = open(releFile,"r")
    paraf = open(filename,"w")

    relFile = rfile.readlines()
    for i in range(len(relFile)):
        relFile[i] = (relFile[i]).split()

    fileLenList = GetFileLen()

    num = 0

    for sentence in inf.readlines():
        sentence = sentence.split()
        newpara = [1 for i in sentence[1:]]
        Num = sentence[0]
        result = CosinScore(sentence[1:],len(flNumList),fileLenList,paras[num],num+151,relFile[num],flNumList,newpara)
        print newpara
        for i in newpara:
            paraf.write(str(i)+" ")
        paraf.write("\n")
        ans = sorted(result.items(), key=lambda d:d[1],reverse = True)
        nn = 0
        for itm in ans[0:1000]:
            print >>f,Num,"0",(flNumList[itm[0]]),nn,itm[1],"IDIOT"
            nn += 1
        num += 1
    f.close()
    rfile.close()
    paraf.close()
    inf.close()
#print GetFileName(GetFileNum(sentence))
