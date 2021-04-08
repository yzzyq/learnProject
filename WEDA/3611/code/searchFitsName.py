#通过得出的结果的顺序找出对应的文件名
import os
#读取指定行的数据
def readLineData(file_path,line_num):
    for cur_line_num,line in enumerate(open(file_path,'rU')):
        if cur_line_num == line_num - 1:
            return line
    return ''



if __name__ == '__main__':
    #只拿出分为正类的就可以了
    all_index = []
    # with open('3000-4000.txt','r') as f:
    # with open('8000.txt','r') as f:
    # with open('12000.txt','r') as f:
    with open('19000.txt','r') as f:
        all_index = f.readline()
        all_index = all_index.split('[')[1]
        all_index = all_index.split(']')[0]
        all_index = all_index.split(',')
        all_index = [int(index) for index in all_index]
    print(len(all_index))

    all_fileName = []
    # with open('all-fileName/4000allData.txt','r') as f:
    # with open('all-fileName/8000allData.txt','r') as f:
    # with open('all-fileName/12000allData.txt','r') as f:
    with open('all-fileName/19000allData.txt','r') as f:
        for line in f.readlines():
            all_fileName.append(str(line.strip()))
    print(len(all_fileName))

    for index in all_index:
        file_name = all_fileName[index] + '\n'
        with open('all-unclassified.txt','a') as f:
            f.write(file_name)


    
    # list_dir = os.listdir('19000/50')
    # for index_num in all_index:
    #     with open('all-trueIndex/19000/trueName.txt','a') as f:
    #         f.write(str(list_dir[index_num]) + '\n')

