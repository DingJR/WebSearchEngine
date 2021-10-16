import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
import json
import mord as md
from sklearn.neural_network import MLPClassifier
from sklearn import svm
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
clf = md.LogisticIT()
clf = LinearRegression()
clf = LogisticRegression(random_state=0, solver='lbfgs',multi_class='multinomial')
clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,max_depth=1, random_state=0)
clf = LinearRegression()
clf = linear_model.BayesianRidge()
clf = linear_model.Ridge(alpha=.5)
clf = svm.SVC(kernel='linear')
clf = MLPClassifier(solver='sgd',hidden_layer_sizes=10)
clf = tree.DecisionTreeClassifier()
clf = OneVsRestClassifier(LinearSVC(random_state=0))
clf = GradientBoostingClassifier()
clf = DecisionTreeClassifier()
#clf = SVC(gamma='auto',probability=True)
def read_data(allquery,feature,qf):
    qf = open(qf,"r")
    allquery = open(allquery,"r")
    q2f = {}
    for line in qf.readlines():
        words = line.split()
        if not q2f.get(words[0]):
            q2f[words[0]] = [words[2]]
        else :
            q2f[words[0]].append(str(words[2]))

    query = json.load(allquery)
    i = 0
    for q in query:
        queryFeature = open(feature+q,"r")
        print queryFeature
        trainData = json.load(queryFeature)
        asd = 0
        for k in trainData.keys():
            if str(k) in q2f[q]:
                (trainData[k]).append(float(1))
            else:
                (trainData[k]).append(float(-1))
        if i == 0:
            M = np.array((trainData.values()))
        else :
            M = np.vstack(M,np.array((trainData.values())))
    #print np.array(M[:,0:-1])
    print M[:,-1]
    clf.fit(M[:,0:-1],M[:,-1])
    return M

def Predict(paras,array):
    ans = 0.0
    for i in range(len(array)):
        ans += paras[0][i]*array[i]
    return ans

def test(allquery,feature,qf,M):
    qf = open(qf,"r")
    allquery = open(allquery,"r")
    q2f = {}
    for line in qf.readlines():
        words = line.split()
        if not q2f.get(words[0]):
            q2f[words[0]] = [words[2]]
        else :
            q2f[words[0]].append(words[2])
    query = json.load(allquery)
    i = 0
    outputFile = "SLMoutput"
    f = open(outputFile,"w")
    print f
    for q in query:
        queryFeature = open(feature+q,"r")
        trainData = json.load(queryFeature)
        print queryFeature
        for i in trainData.keys():
            #print clf.coef_
            #trainData[i] = np.dot(np.array(trainData[i]),clf.coef_.T)
            #print (clf.predict_proba(np.array([trainData[i]])))
            trainData[i] = (clf.predict_proba(np.array([trainData[i]])))[0][1]/(clf.predict_proba(np.array([trainData[i]])))[0][0]
            #print (clf.predict(np.array([trainData[i]])))

        ans = sorted(trainData.items(), key=lambda d:d[1],reverse=True)
        nn = 0
        for itm in ans[0:1000]:
            print>>f,q,"0",itm[0],nn,itm[1],"IDIOT"
            nn +=1

if __name__=="__main__":
    M = read_data("./trainData","./Features/","./train.abs.rels")
    test("./trainData","./Features/","./train.abs.rels",M)
