import math
def prec(testData,relevantData):
    ts = set(testData)
    rs = set(relevantData)
    rele = ts.intersection(rs)
    return float(len(rele))/float(len(testData))

def recall(testData,relevantData,k):
    ts = set(testData)
    rs = set(relevantData)
    rele = ts.intersection(rs)
    return float(len(rele))/float(len(relevantData))

def pk(testData,relevantData,k):
    return prec(testData[0:float(k)*0.1*len(testData)],relevantData)

def rk(testData,relevantData,k):
    return rk(testData[0:k],relevantData)

def AP(testData,relevantData):
    ans = []
    for k in range(10):
        ans.append(pk(testData,relevantData,k+1))
    return ans

def recall(testData,relevantData):
    kList = [5,10,100,1000,10000] 
    ans = []
    for i in range(len(kList)):
        k = kList[i]
        if k < len(testData):
            ans.append(rk(testData,relevantData,k))
        else:
            ans.append(rk(testData,relevantData,len(testData)))
            return ans;
    return ans

def ndgg(testData,relevantData,p):
    ans = []
    normalFactor = 0.0
    k = 0.1
    while(k<=p):
        ans.append(pow(2,pk(testData,relevantData,k+1))/math.log(k+2,2))
        normalFactor = 1.0/math.log(k+2,2)
        k += 0.1
    return sum(ans)/normalFactor


'''
    @fun: evaluation the results with different methods
    @params:testData(an array containing the results IR retrieved from a query),
            relevantData(an array containing standard answer) 
            types: "P_at_K"   :Precision at position k for query q:
                               Another parameter kNum passed(1->10)
                   "AP"       :Average precision for query q(k = 1->10)
                   "RECALL"   :the fraction : the documents that are relevant and that are retrieved.
                   "R_at_K"   :the fraction : the documents that are relevant and that are retrieved at k.
                               Another parameter kNum passed(1->10)
                   "PRECISION": the fraction of the documents retrieved that are relevant to the all relevant
                   default = "all":apply all methods
    @return:
'''
def Evaluation(testData, relevantData,types = "all",kNum = 1):
    if types == "P_at_K":
        return pk(testData,relevantData,kNum)
    elif types == "AP":
        return AP(testData,relevantData)
    elif types == "PRECISION":
        return prec(testData,relevantData)
    elif types == "R_at_K":
        return rk(testData,relevantData,kNum)
    elif types == "RECALL":
        return recall(testData,relevantData)
    elif types == "NDGG":
        return ndgg(testData,relevantData,kNum)
    precises = AP(testData,relevantData)
    recalls = recall(testData,relevantData)
    gainrel = ndgg(testData,relevantData,kNum)
    return precise,recalls,gainrel
    



