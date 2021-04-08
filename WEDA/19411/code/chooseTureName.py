import os

def extractData(file):
    dataSet = []
    # index = 0
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
    all_file = extractData('all-fileName/4000allData.txt')
    no_choice_file = extractData('3000-4000.txt')
    true_file = [file for file in all_file if file not in no_choice_file]

    for file in true_file:
        with open('500-600-result1.0/50trueName.txt','a') as f:
            f.write(str(file) + '\n')
            

    
