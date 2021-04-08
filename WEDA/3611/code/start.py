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
# result_file = 'difficult-result-2'

# fileName = '617'
# result_file = '617-result-2'

fileName = '3611'
result_file = '3611-result-3'




max_threshold = [0.5, 0.5, 1]
preset_weight = [0.8, 0.2]

list_dir = os.listdir(fileName)
if not os.path.exists(result_file):
    os.mkdir(result_file)

cut_off_threshold = [(index+1) / 20  for index in range(20)]

# 3611
# true_index = [[211, 161, 35, 5, 6, 242, 176, 395, 182, 169], 

#               [175, 67, 1143, 1148, 13, 744, 1156, 1602, 1630, 202],

#               [217, 640, 876]]

three_dir_name = ['0-10', '10-50', '50']

# 提取出所有数据的信息，并且按照信噪比对数据进行分组
three_ston_dataSet, three_ston_Poistion, three_ston_index, three_ston_fileName = fitsData.exractData(fileName)

# 将数据保存起来
# for ston_index, ston_fileName in enumerate(three_ston_fileName):
#     file_name = fileName + '-' + three_dir_name[ston_index] + '.txt'
#     with open(file_name, 'a') as f:
#         for one_file_name in ston_fileName:
#             f.write(one_file_name + '\n')
# aa = aa

# true_index = [[4, 422, 408, 43, 394, 154, 40, 60, 334, 37, 160, 317, 34, 311, 434, 118, 275, 181, 49, 446, 
#                 231, 175, 386, 442, 375, 104, 3, 165, 0, 90, 456, 56, 210, 1, 364, 373,
#                 339, 331, 45, 102, 161, 41, 5, 103, 315, 352, 381, 241, 374, 172, 451, 348, 151, 75, 266, 123, 431, 
#                 429, 366, 370, 397, 70, 376, 457, 112, 170, 91, 336, 168, 69, 38, 50, 18, 414, 292, 173, 230, 312, 
#                 438, 418, 461, 265, 452, 300, 100],
#                [1051, 1629, 743, 1798, 198, 38, 757, 1144, 61, 1406, 679, 156, 1601, 122, 1670, 680, 28, 174, 1857, 
#                1147, 1008, 286, 190, 1309, 1464, 1547, 1139, 505, 463, 142, 682, 378, 1685, 1691, 1040, 13, 1420, 1230, 
#                1023, 1083, 445, 391, 1138, 1129, 1035, 831, 1768, 1417, 1879, 1347, 1756, 46, 644, 1334, 1193, 12, 
#                1189, 201, 1612, 778, 687, 1700, 436, 202, 525, 1890, 1351, 66, 143, 1136, 113, 530, 1322, 107, 407, 1432, 
#                1801, 90, 253, 493, 704, 1397, 1175, 1771, 1258, 1174, 39, 1133, 18, 1177, 1550, 1832, 1755, 1155, 1200, 102, 
#                1061, 1157, 124, 231],
#                [639, 875, 216]]


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



    # 根据文件名找出标签
    # if ston_index == 2:
    #     true_index = []
    #     with open('C:/Users/guoji/Desktop/paper/数据整理/3611/3611-50-true-file.txt', 'r') as f:
    #         for one_file in f.readlines():
    #             # print(one_file)
    #             index = all_fileName.index(one_file.strip('\n'))
    #             true_index.append(index)
    #             # print(index)
    #     print(true_index)
    #     aa = aa
    # else:
    #     continue
    # aa = aa

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
    with open(result_file + '/' + fileName + '-' + three_dir_name[ston_index] + '-true-file-name.txt', 'a') as f:
        for one_index in all_sort_index:
            f.write(all_fileName[one_index] + '\n')
    
    # for one_threshold in cut_off_threshold:
    #     num = int(len(all_sort_index) * one_threshold)
    #     result = set(all_sort_index[:num])
    #     have_num = len(result & set(true_index[ston_index]))
    #     recall = 0
    #     precise = 0
    #     if len(true_index[ston_index]) != 0 and num != 0:
    #         recall = have_num / len(true_index[ston_index])
    #         precise = have_num / num
    #     no_index = set(true_index[ston_index]) - result
    #     # for index in no_index:
    #     #     print(all_fileName[index])
    #     print('threshold:{0}, recall:{1}, precise:{2}, number:{3}, true_num:{4}'.format(one_threshold,
    #                                                                                     recall,
    #                                                                                     precise,
    #                                                                                     num,
    #                                                                                     have_num))

running_time = time.perf_counter() - counter_start_time
print('运行时间:', running_time)
with open(result_file + '/time.txt', 'w') as f:
    f.write('time:' + str(running_time))

