import nltk
import os
import gzip
import re
from time import *
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

thesaurus = {}
f=None
stop_words = set(stopwords.words('english'))
if __name__ == "__main__":
    path=os.path.abspath('.')
    fNm = "addressname"
    with open(fNm,"r") as f:
        fLns = f.readlines()
    print "Input the File Num you Get in Query"
    numF = int(raw_input())
    fNm = fLns[numF]
    fNm = fNm.strip('\n')
    print fNm
    f.close()
    f = gzip.GzipFile(mode = "rb", fileobj = open(fNm,"rb"))
    print "Input the Query Word"
    tQry = raw_input()
    tQry = set(tQry.split(' '))
    lN = 0
    for line in f:
        tokens = nltk.word_tokenize(line)
        lineWord = set()
        for word in tokens:
            word = word.lower()
            if word not in stop_words and re.match('^[a-z]+$',word):
                wordAftLmmtz = WordNetLemmatizer().lemmatize(word,pos='v')
                #ansWord = PorterStemmer().stem(wordAftLmmtz)
                ansWord = wordAftLmmtz
                lineWord.add(ansWord)
        lQ = lineWord & set(tQry)
        if lQ :
            print "Line: %7d" %(lN) ," Contains: ",list(lQ)
        lN += 1

