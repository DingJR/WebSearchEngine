import nltk
import os
import gzip
import re
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from time import *
import thread
import psutil
import multiprocessing as mp

globalPath = "./doc/"
dirList = list(os.listdir(globalPath))

def GetFileLen(threadName,x):
    global dirList
    threadList = dirList[int(len(dirList)*(float(x)/float(4))):int(len(dirList)*(float(x+1)/float(4)))]
    for d in threadList:
        pdir = globalPath + d + "/"
        print pdir
        fls = os.listdir(pdir)
        output = pdir + "fileLen"
        ouf = open(output,"w")
        for name in fls:
            if name == "fileLen":
                continue
            f = open(pdir+name,"r")
            lines = f.readlines()
            l = 0
            for line in lines:
                eles = (line.split())
                if len(eles) > 1:
                    l += int((line.split())[1])
            if l == 0:
                print name
                print>>ouf ,name,'0'
            else :
                print>>ouf,name,l

if __name__=="__main__":
    dirList = list(os.listdir(globalPath))
    processes = [mp.Process(target=GetFileLen, args=("thread", x)) for x in range(4)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
