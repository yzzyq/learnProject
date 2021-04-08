import numpy as np
import fitsData
import selfDataCompare as sdc
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

# fileName = '3611'
# result_file = '3611-result-4'

fileName = '8202'
result_file = '8202-result-3'

# fileName = '12872'
# result_file = '12872-result'

# fileName = '19411'
# result_file = '19411-result'




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

# 8202
true_index = [[371, 402, 548, 736, 499, 739, 569, 384, 448, 19, 283, 486, 52, 450, 243, 156, 744, 757, 567, 664, 606, 646, 314, 
               705, 4, 405, 153, 616, 142, 684, 154, 250, 244, 481, 574, 190, 145, 21, 312, 62, 192, 645, 241, 3, 743, 667, 287, 
               11, 161, 282, 253, 414, 729, 577, 102, 381, 662, 462, 205, 10, 492, 563, 568, 288, 249, 242, 245, 572, 247, 128, 
               290, 649, 310, 186, 725, 148, 426, 721, 466, 228, 149, 591, 521, 64, 334, 362, 663, 68, 248, 251, 206, 8, 308, 
               101, 208, 762, 110, 479, 7, 719, 298, 171, 181, 339, 756, 682, 61, 333, 639, 660, 184, 185, 306, 260, 150, 6, 63, 
               69, 346, 60, 57, 9, 471, 207],
               [1184, 3184, 3131, 2521, 2899, 3819, 2696, 2876, 3672, 2229, 3233, 2069, 2959, 1515, 3247, 2945, 2230, 3670, 2984, 
                86, 2501, 2554, 3337, 2038, 3406, 3088, 1958, 3702, 3480, 3134, 2665, 2288, 3655, 2777, 2415, 2728, 1513, 2679, 
                3171, 2557, 1879, 1931, 3831, 3204, 3345, 1841, 3448, 2629, 3169, 2348, 3176, 1957, 3471, 1512, 3834, 330, 2598, 
                1694, 3158, 2369, 2773, 2970, 3679, 2502, 3315, 2008, 2983, 3461, 3669, 2532, 3862, 2990, 1314, 1963, 2023, 3473, 
                2786, 2560, 692, 1966, 3597, 2081, 2439, 2925, 3714, 2933, 2664, 2411, 2550, 1646, 3487, 3248, 3530, 1950, 726, 3075, 
                2093, 2811, 1917, 2022, 1857, 3340, 2036, 2322, 3148, 2099, 739, 1852, 3344, 2530, 3149, 2171, 1970, 2661, 2562, 
                1651, 2723, 3739, 788, 2437, 1076, 3157, 1121, 1876, 2218, 1844, 1861, 2840, 745, 1968, 1452, 3231, 2722, 1013, 2445, 
                3661, 2150, 760, 3718, 2669, 3317, 3527, 2387, 3296, 2942, 1656, 2801, 1036, 141, 3097, 2243, 3717, 1510, 3786, 3002, 
                2325, 2727, 2238, 2503, 765, 2791, 2861, 2308, 2590, 2738, 2478, 2687, 2845, 1682, 2798, 2793, 496, 2900, 3683, 3086, 
                3528, 3375, 16, 3590, 3258, 2137, 2736, 1223, 3857, 3246, 3133, 3072, 2989, 3850, 3037, 2931, 2544, 2352, 1398, 1474, 
                804, 2889, 2946, 3370, 926, 895, 3376, 2172, 2693, 2142, 3128, 2317, 3219, 2125, 2536, 2379, 3302, 3142, 3400, 2862, 
                2683, 2789, 1216, 2891, 3722, 2816, 3879, 3538],
                [1751, 1359, 648, 2635, 3382, 3461, 3139, 3305, 2115, 919, 2434, 1022, 3460, 2664, 2314, 3533, 3463, 2499, 2364]]


# 3611
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

# file_index = ['C:/Users/guoji/Desktop/paper/数据整理/8202/8202-0-10-true-file_name.txt', 
#               'C:/Users/guoji/Desktop/paper/数据整理/8202/8202-10-50-true-file_name.txt',
#               'C:/Users/guoji/Desktop/paper/数据整理/8202/8202-50-true-file_name.txt']

for ston_index in range(len(three_ston_dataSet)):
    file_path = fileName + '/' + three_dir_name[ston_index]

    # 拿出数据
    dataSet = three_ston_dataSet[ston_index]
    allPoistion = three_ston_Poistion[ston_index]
    allIndex = three_ston_index[ston_index]
    all_fileName = three_ston_fileName[ston_index]

    # one_true_index = true_index[ston_index]
    # with open('3611-true-file.txt', 'a') as f:
    #     for one_index in one_true_index:
    #         f.write(all_fileName[one_index] + '\n')
    # continue


    # 根据文件名找出标签
    # if ston_index == 2:
    # true_index = []
    # with open(file_index[ston_index], 'r') as f:
    #     for one_file in f.readlines():
    #         # print(one_file)
    #         index = all_fileName.index(one_file.strip('\n').strip(' '))
    #         true_index.append(index)
    #         # print(index)
    # print(true_index)
    # print(len(true_index))
    # continue
    # aa = aa
    # else:
    #     continue
    # aa = aa

    # for data_print_index in range(len(allIndex)):
        # print('{0}:{1},{2}'.format(data_print_index, allIndex[data_print_index], all_fileName[data_print_index]))
    dataProcess = np.zeros((len(dataSet),4))
    print('找到周围数据。。')
    # 得出所有数据周围的数据，这样得话计算量较大，修改一下
    # aroundData = adc.getAroundData(allPoistion, threshold)
    print('开始计算信息。。')
    # 得出全部的信息
    no_class_index = sdc.getFluxData(dataSet, center, dataProcess, allPoistion, all_Centers, threshold)
    print('得到全部的信息')
    for data_index,data in enumerate(dataProcess):
        print(data_index, data)

    print('得到全部的信息，算法进行排序')
    all_sort_index = process.threeColProcess(dataProcess,no_class_index,preset_weight)

    print('排序的结果:', all_sort_index)
    with open(result_file + '/' + fileName + '-' + three_dir_name[ston_index] + '-true-file-name.txt', 'a') as f:
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
        for index in no_index:
            print(all_fileName[index])
        print('threshold:{0}, recall:{1}, precise:{2}, number:{3}, true_num:{4}'.format(one_threshold,
                                                                                        recall,
                                                                                        precise,
                                                                                        num,
                                                                                        have_num))

running_time = time.perf_counter() - counter_start_time
print('运行时间:', running_time)
with open(result_file + '/time.txt', 'w') as f:
    f.write('time:' + str(running_time))

