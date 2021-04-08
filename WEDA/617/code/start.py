import numpy as np
import fitsData
import selfDataCompare as sdc
import lineDataCompare as ldc
import aroundDataCompare as adc
import os
import time
import process

# 根据相似度进行对比
counter_start_time = time.perf_counter()

# 发射线的位置
center = [6564, 4862]
# 线表各发射线的位置
all_Centers = [6549,6585,6718,6732]

threshold = 1

# fileName = 'E:/second/second-1'
# fileName = 'difficult'
fileName = '617'
result_file = '617-result-2'

# fileName = '3611'
# result_file = '3611-result'


max_threshold = [0.5, 0.5, 1]
preset_weight = [0.8, 0.2]

list_dir = os.listdir(fileName)
if not os.path.exists(result_file):
    os.mkdir(result_file)

# 3611
true_index = [[211, 161, 35, 5, 6, 242, 176, 395, 182, 169], 

              [175, 67, 1143, 1148, 13, 744, 1156, 1602, 1630, 202],

              [217, 640, 876]]

three_dir_name = ['0-10', '10-50', '50']
cut_off_threshold = [(index+1) / 20  for index in range(20)]

# 提取出所有数据的信息，并且按照信噪比对数据进行分组
three_ston_dataSet, three_ston_Poistion, three_ston_index, three_ston_fileName = fitsData.exractData(fileName)

for ston_index in range(len(three_ston_dataSet)):
    file_path = fileName + '/' + three_dir_name[ston_index]
    # result_path = result_file + '/' + three_dir_name[ston_index]
    # 创建文件夹
    # if not os.path.exists(result_path):
    #     os.mkdir(result_path)

    # 拿出数据
    dataSet = three_ston_dataSet[ston_index]
    allPoistion = three_ston_Poistion[ston_index]
    allIndex = three_ston_index[ston_index]
    all_fileName = three_ston_fileName[ston_index]
    # for data_print_index in range(len(allIndex)):
        # print('{0}:{1},{2}'.format(data_print_index, allIndex[data_print_index], all_fileName[data_print_index]))
    dataProcess = np.zeros((len(dataSet),4))
    print('找到周围数据。。')
    # 得出所有数据周围的数据
    aroundData = adc.getAroundData(allPoistion, threshold)
    print('开始计算信息。。')
    # 得出全部的信息
    no_class_index = sdc.getFluxData(dataSet, center, dataProcess, aroundData, all_Centers)
    print('得到全部的信息')
    for data_index,data in enumerate(dataProcess):
        print(data_index, data)

    print('得到全部的信息，算法进行排序')
    all_sort_index = process.threeColProcess(dataProcess,no_class_index,preset_weight)

    print('排序的结果:', all_sort_index)
    with open(result_file + '/617-' + three_dir_name[ston_index] + '-true-file-name.txt', 'a') as f:
        for one_index in all_sort_index:
            f.write(all_fileName[one_index] + '\n')
    
    for one_threshold in cut_off_threshold:
        num = int(len(all_sort_index) * one_threshold)
        result = set(all_sort_index[:num])
        have_num = len(result & set(true_index[ston_index]))
        recall = 0
        precise = 0
        if len(true_index[ston_index]) != 0 and num != 0:
            recall = have_num / len(true_index[ston_index])
            precise = have_num / num
        no_index = set(true_index[ston_index]) - result
        # for index in no_index:
        #     print(all_fileName[index])
        print('threshold:{0}, recall:{1}, precise:{2}, number:{3}, true_num:{4}'.format(one_threshold,
                                                                                        recall,
                                                                                        precise,
                                                                                        num,
                                                                                        have_num))

running_time = time.perf_counter() - counter_start_time
print('运行时间:', running_time)
with open(result_file + '/time.txt', 'w') as f:
    f.write('time:' + str(running_time))

