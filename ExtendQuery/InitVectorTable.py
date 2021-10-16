import math
import re
import os
import string
    
if __name__ == "__main__":
    filename = "vectorTable"
    paraf = open(filename,"w")

    inputFile = "input"
    inf = open(inputFile,"r")
    for l in inf.readlines():
        for i in (l.split())[1:]:
            paraf.write("1 ")
        paraf.write("\n")
    paraf.close()
    inf.close()
#print GetFileName(GetFileNum(sentence))
