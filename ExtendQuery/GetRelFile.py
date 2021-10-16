import math
import re
import os
import string
if __name__ == "__main__":
    outputFile = "RelavantFile"
    inputFile = "StdAns"
    f = open(outputFile,"w")
    inf = open(inputFile,"r")
    curid = 151
    for l in inf.readlines():
        temp = int((l.split())[0])
        name = (l.split())[2]
        rel  = int((l.split())[3])
        if temp != curid:
            f.write("\n")
            curid = temp
        if rel:
            f.write(name+" ")
    f.write('\n')
    f.close()
    inf.close()
#print GetFileName(GetFileNum(sentence))
