import os
pathList = []
def GetPathAddress(pathName):
    if os.path.isdir(pathName):
        os.chdir(os.path.abspath('.')+'/'+pathName)
        pathnames = os.listdir()
        for name in pathnames:
            GetPathAddress(pathName)
    else :
        pathList.append(os.path.abspath('.'))

output = open("addressname","w")
i=0
GetPathAddress("disk1","disk2")
for name in pathList:
    print>>output ,name,i
    i += 1
