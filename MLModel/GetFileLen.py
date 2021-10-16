import os
path = "doc/"
d = os.listdir(path)
fileLen = {}
for ele in d:
    f = path+ele+"/"+"fileLen"
    f = open(f,"r")
    for line in f.readlines():
        fileLen[int((line.split())[0])] = int((line.split())[1])
import json
f = "fileLen"
f = open(f,"w")
json.dump(fileLen,f)
