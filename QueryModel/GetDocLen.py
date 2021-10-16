def GetFileName():
        with open("addressname",'r') as f:
            fileNumNameList = f.readlines()
            results = []
            for ele in fileNumNameList:
                temp = ele.strip('\n')
                results.append(temp)
            return results
fls = GetFileName()
output = 'output'
ouf = open(output,"w")
for name in fls:
    f = open(name,"r")
    line = f.readlines()
    if len(line) == 0:
        print name
        print>>ouf ,'0'
    else :
        line = (line[0]).split()
        print>>ouf,len(line)

