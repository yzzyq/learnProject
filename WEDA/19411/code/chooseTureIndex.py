#选出正确的数据的序号
import os

def extractData(file):
    dataSet = []
    index = 0
    with open(file,'r') as f:
        for line in f.readlines():
##            if index == 0:
##                dataSet.append('spec-55859-F5902_sp03-028.fits.gz')
##                index += 1
##            else:
            dataSet.append(str(line.strip()))
    print(len(dataSet))
    return dataSet


if __name__ == '__main__':
    true_files = 'C:/Users/yzzyq/Desktop/8000/50.txt'
    all_files = '8000-result3.0/data-50.txt'
    true_data = extractData(true_files)
    all_data = extractData(all_files)
    print(len(true_data))
    print(len(all_data))
    results = []
    for data in true_data:
        results.append(all_data.index(data)+1)
    print(len(results))
    print(results)
##    list_dir = os.listdir(all_files)
##    true_index = 0
##    results = []
##    for index in range(len(list_dir)):
####        print(index)
####        print(list_dir[index])
####        print(list_dir[index],true_data[true_index])
##        if list_dir[index] == true_data[true_index]:
####            print('有相同的')
####            print(true_index)
##            print(index)
##            results.append(index+1)
##            if true_index < len(true_data) - 1:
##                true_index += 1
##            print(true_index)
##            print(true_data[true_index])
    
    # with open('all-trueIndex/19000/19000-alltrueIndex.txt','w') as f:
    #     f.write(str(results))




