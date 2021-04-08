#提取出光谱名保存在一个文件中
import os

fileLocation = 'H:/数据/comparedExperiment/all'
listDirs = os.listdir(fileLocation)
for dirName in listDirs:
    with open('H:/数据/comparedExperiment/44713allData.txt','a') as f:
        f.write(dirName + '\n')
        
