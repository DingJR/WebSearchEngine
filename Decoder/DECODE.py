import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import re
import string
stop_words = set(stopwords.words('english'))
def DecodeFile(fileName):
    thesaurus = {}
    with open(fileName,"rb") as f:
        chunk = f.read()
        state = 0 # 0:char 1:num begin mid 2:num end
        temp = 0
        word=str("")
        for ele in chunk:
            eleNum = ord(ele)
            if state == 0:
                temp = 0
                if eleNum >= 128:
                    temp += eleNum - 128
                    thesaurus[word] = []
                    state = 1
                elif eleNum < 128 :
                    word  = word + ele
            elif state == 1:
                if eleNum < 128:
                    temp *=128
                    temp += eleNum
                elif eleNum == 128:
                    state = 2
                else :
                    temp *=128
                    temp += eleNum - 128
                    state = 2
                if state == 2:
                    (thesaurus[word]).append(temp)
                    temp = 0
            elif state == 2:
                if eleNum < 128:
                    word = str("")
                    word = word + ele
                    state = 0
                else:
                    state = 1
                    temp += eleNum-128
    return thesaurus

def GetCommonFileNum(list1,list2):
    set1 = set(list1)
    set2 = set(list2)
    ansSet = set1 & set2
    return sorted(list(ansSet))

def GetPages(codeList):
    leng = len(codeList)
    temp = []
    temp.append(codeList[0])
    for i in range(leng-1):
        temp.append(temp[i] + codeList[i+1])
    return temp

def GetFileNum(line):
    tokens = nltk.word_tokenize(line)
    mergeList = []
    with open("addressname",'r') as f:
        fileNumNameList = f.readlines()
    for i in range(len(fileNumNameList)):
        mergeList.append(i+1)
    f.close()
    words = []
    for word in tokens:
        word = word.lower()
        if word not in stop_words and re.match('^[a-z]+$',word):
            wordAftLmmtz = WordNetLemmatizer().lemmatize(word,pos='v')
            #ansWord = PorterStemmer().stem(wordAftLmmtz)
            ansWord = wordAftLmmtz
            words.append(ansWord)
    initList = []
    for word in words:
        initList.append(str(word[0]))
    initSet = set(initList)
    initList = list(initSet)
    for Initial in initList:
        thesaurus = DecodeFile("index//"+Initial)
        for word in words:
            if thesaurus.get(word):
                mergeList = GetCommonFileNum(mergeList,GetPages(thesaurus[word]))
            elif word[0] == Initial:
                mergeList = []
        if len(mergeList) == 0:
            break
    mergeList = sorted(mergeList)
    print mergeList
    return mergeList
def GetFileName(numList):
    with open("addressname",'r') as f:
        fileNumNameList = f.readlines()
    results = []
    for ele in numList:
        results.append((fileNumNameList[ele-1]).strip('\n'))
    return results
print "Input the sentence you want to question !"
sentence = raw_input()
sentence = sentence.lower()
print GetFileName(GetFileNum(sentence))
