import random
import numpy as np
import copy

# 得出主信息的置信度
def getFluxData(dataSet, two_centers, dataProcess, aroundData, other_centers):
    len_dataSet = len(dataSet)
    no_class_index = []
    all_centers = two_centers + other_centers
    # 对所有的数据进行叠加,叠加之前先进行归一化和放大，如果所有数据都经过这样的处理的话，那么时间复杂度会很高，考虑是不是要放大
    for data_index in range(len_dataSet):
        self_wave = []
        # print('数据的索引:', data_index)
        for index, center in enumerate(two_centers):
            # print(index, center)
            side_left = center - 11
            side_right = center + 12
            # 这里的置信度就是通过峰值与中心点的距离计算出来的
            one_trust = getOneValue(dataSet[data_index],side_left,side_right,center,self_wave)
            # print(index, center, one_trust)
            # one_trust = getOneValue(dataSet[data_index],side_left,side_right,center, self_data) if index == 0 else \
            #                                                     getOneValue(dataSet[data_index],side_left,side_right,center)

            # if len(one_range_data) == 0:
            #     print('{0}:{1}'.format(data_index,index))
            # print('{0}:{1}'.format(center, one_trust))
            dataProcess[data_index, 0] += one_trust
            # self_data.append(one_range_data)
            # 如果Ha不存在的话，那么就算没有这个发射线
            if 0 == index and 0 == one_trust:
                dataProcess[data_index, -1] = -1
                break
        
        # print('主信息计算完毕，计算次要信息')
        
        # 只有可能有发射线的数据需要检测
        if dataProcess[data_index, -1] != -1:
            no_class_index.append(data_index)
            sourroundData = [dataSet[sourround_index] for sourround_index in aroundData[data_index]]

            # 线表
            for one_center in other_centers:
                # print(one_center)
                one_side_left = one_center - 10
                one_side_right = one_center + 10
                one_trust = getOneValue(dataSet[data_index],one_side_left,one_side_right,one_center,self_wave)
                dataProcess[data_index, 1] += one_trust
            # print('计算完线表信息')
            
            sourround_trust = 0
            # 周围数据的置信度
            if len(sourroundData) != 0:
                for one_index, one_center in enumerate(all_centers):
                    side_left = one_center - 11
                    side_right = one_center + 12
                    sourround_trust += overLayData(sourroundData,side_left,side_right,one_center,self_wave[one_index])
            
            dataProcess[data_index, 1] = dataProcess[data_index, 1] / len(other_centers)
            dataProcess[data_index, 2] = sourround_trust / len(all_centers)
    return no_class_index

# 周围数据与之全部叠加起来,得出整体的置信度
def overLayData(sourroundData,side_left,side_right,one_center,self_wave):
    # 注意还有周围什么数据都没有的离群数据点
    over_data = np.zeros(len(self_wave))
    # print('len(over_data):', len(over_data))
    # print('len(one_self_data[0]):', len(one_self_data[0]))
    # print('原本的数据:', over_data)
    for data in sourroundData:
        # for index,one_wave in enumerate(data[0]):
        #     if side_left < one_wave < side_right:
        #         choice_data.append(data[1][index])
        choice_data = [data[1][index] for index,one_wave in enumerate(data[0]) if side_left < one_wave < side_right]
        choice_data = mostValueScaling(choice_data)
        for choice_data_index in range(min(len(over_data), len(choice_data))):
            over_data[choice_data_index] += choice_data[choice_data_index]
    # 全部数据叠加完之后再进行判断置信度
    over_data = list(map(lambda x:x/len(sourroundData), over_data))
    # over_data = over_data / len(sourroundData)
    # print('叠加完的数据:', over_data)
    trust = getOverDataTrust(over_data,self_wave,one_center)
    return trust



# # 周围数据与之全部叠加起来,得出整体的置信度
# def overLayData(one_self_data,sourroundData,side_left,side_right,one_center):
#     # 注意还有周围什么数据都没有的离群数据点
#     over_data = one_self_data[1]
#     # print('len(over_data):', len(over_data))
#     # print('len(one_self_data[0]):', len(one_self_data[0]))
#     # print('原本的数据:', over_data)
#     for data in sourroundData:
#         choice_data = [data[1][index] for index,one_wave in enumerate(data[0]) if side_left < one_wave < side_right]
#         choice_data = mostValueScaling(choice_data)
#         for choice_data_index in range(min(len(over_data), len(choice_data))):
#             over_data[choice_data_index] += choice_data[choice_data_index]
#     # 全部数据叠加完之后再进行判断置信度
#     over_data = list(map(lambda x:x/len(sourroundData), over_data))
#     # over_data = over_data / len(sourroundData)
#     # print('叠加完的数据:', over_data)
#     trust = getOverDataTrust(over_data,one_self_data[0],one_center)
#     return trust


    # for index,one_center in enumerate(two_centers):
        
    #     one_self_data = self_data[index]
    #     # 注意还有周围什么数据都没有的离群数据点
    #     over_data = copy.deepcopy(one_self_data[1])
    #     # print('len(over_data):', len(over_data))
    #     # print('len(one_self_data[0]):', len(one_self_data[0]))
    #     # print('原本的数据:', over_data)
    #     for data in sourroundData:
    #         choice_data = [data[1][index] for index,one_wave in enumerate(data[0]) if side_left < one_wave < side_right]
    #         # print('周围数据的长度:', len(choice_data))
    #         # choice_data = getChoiceData(data,side_left,side_right,one_center)
    #         choice_data = mostValueScaling(choice_data)
    #         # print(choice_data)
    #         for choice_data_index in range(min(len(over_data), len(choice_data))):
    #             over_data[choice_data_index] += choice_data[choice_data_index]
    #     # 全部数据叠加完之后再进行判断置信度
    #     over_data = list(map(lambda x:x/len(sourroundData), over_data))
    #     # over_data = over_data / len(sourroundData)
    #     # print('叠加完的数据:', over_data)
    #     one_trust = getOverDataTrust(over_data,one_self_data[0],one_center)
    #     trust += one_trust
    # return trust

# 对数据进行归一化
def mostValueScaling(data):
    max_data = max(data)
    min_data = min(data)
    len_data = max_data - min_data
    # print('data:', data)
    # print('len_data:', len_data)
    if max_data == min_data:
        return [0 for index in range(len(data))]
    return [(value - min_data) / len_data for value in data]

# 判断置信度,从置信度和高度来看
def getOverDataTrust(over_data,wave,one_center):
    # center_index = len(over_data - 1) // 2
    dis_center = {}
    before_slope = None
    trust = 0
    for index,one_wave in enumerate(wave[:-1]):
        slope = (over_data[index + 1] - over_data[index]) / (wave[index + 1] - one_wave)
        if before_slope != None:
            if before_slope < 0 and slope > 0 and one_center - 1 < one_wave < one_center + 1:
                return trust
            if before_slope > 0 and slope < 0:
                dis_center[index] = abs(one_wave - one_center)
        before_slope = slope
    if len(dis_center) != 0:
        min_wave = min(dis_center, key = dis_center.get)
        trust += 1 / dis_center[min_wave]    
        trust = getTwoSideHightByDifferent([wave,over_data], min_wave)
    return trust



# 得出发射线俩边的区别
def getTwoSideHightByDifferent(data, wave_one_index):
    change_len = 1
    before_slope = (data[1][wave_one_index - (change_len - 1)] - data[1][wave_one_index - change_len]) / \
                   (data[0][wave_one_index - (change_len - 1)] - data[0][wave_one_index - change_len])
    after_slope = (data[1][wave_one_index + change_len] - data[1][wave_one_index + (change_len - 1)]) / \
                  (data[0][wave_one_index + change_len] - data[0][wave_one_index + (change_len - 1)])
    # 前后差距，高度和俩边的宽度
    before_index = 0
    before_height_diff = 0
    after_index = 0
    after_height_diff = 0
    difference = 0
    len_min = min(len(data[0]), len(data[1]))
    while before_slope > 0 or after_slope < 0:
        change_len += 1

        if wave_one_index - change_len - 1 < 0 or wave_one_index + change_len + 1 > len_min:
            break
        
        if before_slope > 0:
            before_slope = (data[1][wave_one_index - (change_len - 1)] - data[1][wave_one_index - change_len]) / \
                           (data[0][wave_one_index - (change_len - 1)] - data[0][wave_one_index - change_len])
            if before_slope < 0:
                before_index = wave_one_index - change_len + 1
                before_height_diff = abs(data[1][wave_one_index] - data[1][before_index])
     
        if after_slope < 0:
            after_slope = (data[1][wave_one_index + change_len] - data[1][wave_one_index + (change_len - 1)]) / \
                          (data[0][wave_one_index + change_len] - data[0][wave_one_index + (change_len - 1)])
            if after_slope > 0:
                after_index = wave_one_index + (change_len - 1)
                after_height_diff = abs(data[1][wave_one_index] - data[1][after_index])
    # print('wave_one_index:{0},after_index:{1},before_index:{2},\
    #        after_height_diff:{3},before_height_diff:{4}'.format(wave_one_index,
    #                                                             after_index,
    #                                                             before_index,
    #                                                             after_height_diff,
    #                                                             before_height_diff))

    # 没有处理的差异值，因数据的不同会不同，需要归一化
    # 波长的差异
    if max(after_index - wave_one_index, wave_one_index - before_index) != 0:
        difference += min(after_index - wave_one_index, wave_one_index - before_index) / \
                    max(after_index - wave_one_index, wave_one_index - before_index)

    # 流量的差异
    if max(after_height_diff, before_height_diff) != 0:
        difference += min(after_height_diff, before_height_diff) / max(after_height_diff, before_height_diff) 
    
    return difference

# 得出相关中心点的置信度
# def getOneValue(data,side_left,side_right,center,*params):
#     len_data = len(data[0])
#     dis_center = {}
#     before_slope = None
#     trust = 0
#     one_wave = []
#     # is_have_center = False
#     if data[0][-1] > side_right and data[0][0] < side_left:
#         for wave_one_index in range(len_data):
#             # print(wave_one_index)
#             if side_left <= data[0][wave_one_index] <= side_right:
#                 one_wave.append(data[0][wave_one_index])
#                 slope = (data[1][wave_one_index+1] - data[1][wave_one_index]) / (data[0][wave_one_index+1] - data[0][wave_one_index])
#                 if before_slope != None:
#                     if before_slope < 0 and slope > 0 and center < data[0][wave_one_index] < center + 1:
#                         return trust
#                     if before_slope > 0 and slope < 0:
#                         # 差距的计算
#                         dis_center[wave_one_index] = abs(data[0][wave_one_index] - center)
#                         # if center - 2  < data[0][wave_one_index] < center + 2:
#                         #     is_have_center = True
#                 before_slope = slope
#     if len(params) > 0 and len(one_wave) > 0:
#         params[0].append(one_wave)
#     # 峰值不能离中心点太远
#     if len(dis_center) != 0 and min(dis_center.values()) < 2:
#         min_wave = min(dis_center, key = dis_center.get)
#         trust += 1 / dis_center[min_wave]  
#         trust += getTwoSideHightByDifferent(data, min_wave)
#     return trust







# 得出相关中心点的置信度
# def getOneValue(data,side_left,side_right,center,*params):
#     len_data = len(data[0])
#     dis_center = {}
#     before_slope = None
#     trust = 0
#     one_flux = []
#     one_wave = []
#     # is_have_center = False
#     if data[0][-1] > side_right and data[0][0] < side_left:
#         for wave_one_index in range(len_data):
#             # print(wave_one_index)
#             if side_left <= data[0][wave_one_index] <= side_right:
#                 one_flux.append(data[1][wave_one_index])
#                 one_wave.append(data[0][wave_one_index])
#                 slope = (data[1][wave_one_index+1] - data[1][wave_one_index]) / (data[0][wave_one_index+1] - data[0][wave_one_index])
#                 if before_slope != None:
#                     if before_slope < 0 and slope > 0 and center < data[0][wave_one_index] < center + 1:
#                         return trust
#                     if before_slope > 0 and slope < 0:
#                         # 差距的计算
#                         dis_center[wave_one_index] = abs(data[0][wave_one_index] - center)
#                         # if center - 2  < data[0][wave_one_index] < center + 2:
#                         #     is_have_center = True
#                 before_slope = slope

#     if len(params) > 0 and len(one_wave) > 0 and len(one_flux) > 0:
#         params[0].append(one_wave)
#         params[0].append(one_flux)
#     # print('range_data:', len(range_data))
#     # 峰值不能离中心点太远
#     if len(dis_center) != 0 and min(dis_center.values()) < 2:
#         min_wave = min(dis_center, key = dis_center.get)
#         trust += 1 / dis_center[min_wave]  
#         trust += getTwoSideHightByDifferent(data, min_wave)
#     return trust
   

#得出第一个值
def getOneValue(data,side_left,side_right,center,*params):
    # peak_value = []
    before_slope = None
    isMout = False
    isBorder = False
    ismiddle = False
    ispadd = False
    ispadd_two = False
    ispadd_three = False
    ispadd_four = False
    ispadd_five = False
    isMout_middle = False
    one_wave = []
    dis_center = {}
    len_data = len(data[0])
    # value = 0
    isRemote = False
    # min_value = float('inf')
    trust = 0
    if data[0][-1] > side_right:
        for i in range(len_data):
            if side_left <= data[0][i] <= side_right:
                # value = data[1][i+1]
                
                one_wave.append(data[0][i])

                #需要记录峰值
                slope = (data[1][i+1] - data[1][i])/(data[0][i+1] - data[0][i])
                #距离边缘值
                if before_slope != None:
                #     peak_value.append(data[1][i])
                # else:
                    if before_slope > 0 and slope < 0:
                        dis_center[i] = abs(data[0][i] - center)
                        if center-2 < data[0][i] < center+2:
                            #分为好几种情况
                            # print('纪律峰值')
                            # print(data[0][i])
                            if abs(before_slope) > 0.02 and abs(slope) > 0.02:
                                if center - 1 < data[0][i] < center:
                                    # print('1:', (data[1][i+1] - data[1][i+2]) / (data[1][i] - data[1][i+1]))
                                    # print('2:', (data[1][i] - data[1][i+2]) / (data[1][i+3] - data[1][i+2]))
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
                                        (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) < 0 and \
                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) < 0 and \
                                        (data[1][i+1] - data[1][i+2]) / (data[1][i] - data[1][i+1]) < 0.2 and \
                                        (data[1][i] - data[1][i+2]) / (data[1][i+3] - data[1][i+2]) > 0.7:
                                        isMout = False
                                        break 

                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
                                        (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) > 0 and \
                                        (data[1][i+5] - data[1][i+4])/(data[0][i+5] - data[0][i+4]) < 0 and \
                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) < 0 and \
                                        (data[1][i+1] - data[1][i+2]) / (data[1][i] - data[1][i+1]) < 0.2 and \
                                        (data[1][i] - data[1][i+2]) / (data[1][i+3] - data[1][i+2]) > 0.7:
                                        isMout = False
                                        break
                                    
                                    # print((data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+2]))
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) < 0 and \
                                        (data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+2]) < 0.2:
                                        isMout = False
                                        break 
                                    


                                if center + 1 < data[0][i] < center + 2:
                                    # print('进入6565')
                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                       ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                       (data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-2]) < 0.4:
                                        isMout = False
                                        break

                                # if center + 1 < data[0][i] < center + 2 and \
                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                       ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                       ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                       (data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-2]) < 0.3:
                                        isMout = False
                                        break

                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
                                       ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                       ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                       (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i-1]) < 0.3:
                                        isMout = False
                                        break

                                    # 19000中的10-50的4778
                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
                                       ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                        ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
                                        ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) < 0 and \
                                        ((data[1][i+5] - data[1][i+4])/(data[0][i+5] - data[0][i+4])) > 0 and \
                                        0.4 < (data[1][i+1] - data[1][i+4]) / (data[1][i] - data[1][i+1]) < 0.5 and \
                                        0.3 < (data[1][i] - data[1][i+4]) / (data[1][i] - data[1][i-2]) < 0.4 and \
                                        0.4 < (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i-1]) < 0.5:
                                        isMout = False
                                        break

                                    # 12000中的10-50的407的特殊情况
                                    # print((data[1][i-1] - data[1][i-3]) / (data[1][i] - data[1][i-1]))
                                    # print((data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-1]))
                                    # if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                    #     ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                    #     ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0 and \
                                    #    ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                    #    (data[1][i-1] - data[1][i-3]) / (data[1][i] - data[1][i-1]) < 0.6 and \
                                    #     0.9 < (data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-1]) < 1.1:
                                    #     isMout = False
                                    #     break

 
                                    # 3000-4000中的10-50的958
                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
                                        ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                        ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
                                        ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) > 0 and \
                                        (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i-1]) < 0.35 and \
                                        0.8 < (data[1][i] - data[1][i+3]) / (data[1][i] - data[1][i-2]) < 1:
                                        isMout = False
                                        break
                                    
                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
                                        ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) > 0 and \
                                       ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
                                       ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                       (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i-1]) < 0.3:
                                        isMout = False
                                        break

                                    #偏移
                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
                                       ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                       (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i-1]) < 0.7:
                                       # (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i-1]) < 0.4:
                                        # (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i-1]) <= 0.8:
                                        isMout = False
                                        break
                                    
                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                        ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) > 0 and \
                                        ((data[1][i-4] - data[1][i-5])/(data[0][i-4] - data[0][i-5])) > 0 and \
                                        ((data[1][i-5] - data[1][i-6])/(data[0][i-5] - data[0][i-6])) < 0 and \
                                       ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                       (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i-1]) < 0.3:
                                        isMout = False
                                        break
                                    

                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                        ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0 and \
                                       ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                       ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                       (data[1][i-1] - data[1][i-3]) / (data[1][i] - data[1][i-1]) < 0.3 and \
                                        0.7 < (data[1][i] - data[1][i-3]) / (data[1][i] - data[1][i+2]) < 1.3:
                                        isMout = False
                                        break
                                    
                                    # print((data[1][i-1] - data[1][i-3]) / (data[1][i] - data[1][i-1]))
                                    # print((data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-3]))
                                    # 全新
                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                        ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0 and \
                                       ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                       ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                       0.5 < (data[1][i-1] - data[1][i-3]) / (data[1][i] - data[1][i-1]) < 1.6 and \
                                        (data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-3]) < 0.5:
                                        isMout = False
                                        break
                                    

                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                       ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                        ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0 and \
                                       ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                       (data[1][i-1] - data[1][i-3]) / (data[1][i] - data[1][i-1]) < 0.3:
                                    #    (data[1][i-1] - data[1][i-3]) / (data[1][i] - data[1][i-1]) < 0.7:
                                        isMout = False
                                        break
                                    
                                if center-2 < data[0][i] < center - 1:
                                    # print((data[1][i] - data[1][i+1]) / (data[1][i+3] - data[1][i+1]))
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) > 0 and \
                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
                                        (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) < 0 and \
                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) < 0 and \
                                        0.6 < (data[1][i] - data[1][i+1])/(data[1][i+3] - data[1][i+1]) < 1.8:
                                        isMout = False
                                        break
                                    
                                    # print((data[1][i] - data[1][i-1])/(data[1][i] - data[1][i+2]))
                                    # print((data[1][i+3] - data[1][i+2])/(data[1][i] - data[1][i+2]))
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
                                        (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) < 0 and \
                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0 and \
                                        (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) < 0 and \
                                        0.7 < (data[1][i+3] - data[1][i+2])/(data[1][i] - data[1][i+2]) < 1.2 and \
                                        (data[1][i] - data[1][i-1])/(data[1][i] - data[1][i+2]) < 0.1:
                                        isMout = False
                                        break

                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                       ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
                                       (data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+2]) < 0.4:
                                        isMout = False
                                        break
                                    
                                    # print('(data[1][i+4] - data[1][i+1]) / (data[1][i] - data[1][i+1]):',(data[1][i+4] - data[1][i+1]) / (data[1][i] - data[1][i+1]))
                                    # 617的0-10的1的新偏移
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) > 0 and \
                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
                                        (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) > 0 and \
                                        (data[1][i+5] - data[1][i+4])/(data[0][i+5] - data[0][i+4]) < 0 and \
                                       ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
                                       0.3 < (data[1][i+4] - data[1][i+1]) / (data[1][i] - data[1][i+1]) < 1:
                                        isMout = False
                                        break
                                    
                                    # 3611的0-10的新偏移
                                    # print((data[1][i+1]) - data[1][i+2] / (data[1][i] - data[1][i+1]))
                                    # print((data[1][i]) - data[1][i+2] / (data[1][i+3] - data[1][i+2]))
                                    # # print()
                                    # if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                    #     (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
                                    #     (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) < 0 and \
                                    #     (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0 and \
                                    #     (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) > 0 and \
                                    #     (data[1][i+1]) - data[1][i+2] / (data[1][i] - data[1][i+1]) < 0.2 and \
                                    #     (data[1][i]) - data[1][i+2] / (data[1][i+3] - data[1][i+2]) > 0.7:

                                    #     isMout = False
                                    #     break
                                    
                                    
                                    # 300-4000的0-10中95的Hb新的偏移
                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
                                        ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) > 0 and \
                                        ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
                                        ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                        0.1 < (data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-1]) < 0.4 and \
                                        0 < (data[1][i+2] - data[1][i+3]) / (data[1][i] - data[1][i+2]) < 0.1:
                                        isMout = False
                                        break
                                    

                                    # 300-4000的0-10中377的Hb新的偏移
                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
                                        ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) > 0 and \
                                        ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
                                        ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                        0.9 < (data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-1]) < 1.02 and \
                                        0.9 < (data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-2]) < 1.02 and \
                                        0 < (data[1][i+2] - data[1][i+3]) / (data[1][i] - data[1][i+2]) < 0.05:
                                        isMout = False
                                        break


                                     
                                    # 8000的10-50中3781新的偏移
                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
                                        ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) > 0 and \
                                       ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
                                       ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                       (data[1][i+1] - data[1][i+2]) / (data[1][i] - data[1][i+1]) < 0.05:
                                        isMout = False
                                        break
                                    
                                    # print((data[1][i] - data[1][i+3]) / (data[1][i+5] - data[1][i+3]))
                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
                                        ((data[1][i+5] - data[1][i+4])/(data[0][i+5] - data[0][i+4])) > 0 and \
                                        ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) > 0 and \
                                       ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
                                       ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                        center == 4862 and \
                                       0.5 < (data[1][i] - data[1][i+3]) / (data[1][i+5] - data[1][i+3]) < 1.5:
                                        isMout = False
                                        break
                                    
                                    # print((data[1][i+4] - data[1][i+1]) / (data[1][i] - data[1][i+1]))
                                    if ((data[1][i+5] - data[1][i+4])/(data[0][i+5] - data[0][i+4])) < 0 and \
                                       ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) > 0 and \
                                       ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                       ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                        center == 4862 and \
                                       0.5 < (data[1][i+4] - data[1][i+1]) / (data[1][i] - data[1][i+1]) < 1.5:
                                        isMout = False
                                        break

                                    # 8000的50中1941新偏移
                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                        ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) > 0 and \
                                        ((data[1][i-4] - data[1][i-5])/(data[0][i-4] - data[0][i-5])) < 0 and \
                                        ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                        ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
                                        ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) > 0 and \
                                        (data[1][i] - data[1][i-1]) / (data[1][i-1] - data[1][i-4]) < 0.03 and \
                                        (data[1][i+1] - data[1][i+3]) / (data[1][i] - data[1][i+1]) < 0.6 and \
                                        (data[1][i] - data[1][i+3]) / (data[1][i] - data[1][i-4]) < 0.65:
                                        isMout = False
                                        break 
                                    
                                    # 8000中的10-50的3253新的偏移
                                    # print((data[1][i] - data[1][i+1]) / (data[1][i+1] - data[1][i+2]))
                                    # print((data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+2]))
                                    # print((data[1][i] - data[1][i+2]) / (data[1][i+3] - data[1][i+2]))
                                    # print((data[1][i] - data[1][i-3]) / (data[1][i+3] - data[1][i+4]))
                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                        ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0 and \
                                        ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                        ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                        ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) < 0 and \
                                        ((data[1][i+5] - data[1][i+4])/(data[0][i+5] - data[0][i+4])) > 0 and \
                                        (data[1][i] - data[1][i+1]) / (data[1][i+1] - data[1][i+2]) > 0.2 and \
                                        0.8 < (data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+2]) < 1.2 and \
                                        0.5 < (data[1][i] - data[1][i+2]) / (data[1][i+3] - data[1][i+2]) < 1.2 and \
                                        0.4 < (data[1][i] - data[1][i-3]) / (data[1][i+3] - data[1][i+4]) < 1.2:
                                        isMout = False
                                        break 


                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) < 0 and \
                                        (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) > 0 and \
                                       ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
                                       (data[1][i+1] - data[1][i+2]) / (data[1][i] - data[1][i+1]) < 0.7 and \
                                        (data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+3]) > 0.7:
                                        ispadd_two = True

                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                       ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                       (data[1][i+1] - data[1][i+2]) / (data[1][i] - data[1][i+1]) < 0.3:
                                        # isMout = False
                                        # break
                                        isRemote = True

                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                       ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                       ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
                                       (data[1][i] - data[1][i-2]) / (data[1][i] - data[1][i+2]) < 0.4:
                                       if (data[1][i] - data[1][i+1]) / (data[1][i+1] - data[1][i+2]) > 0.1:
                                            isMout = False
                                            break
                                    # 偏移    
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
                                        ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
                                        (data[1][i+1] - data[1][i+2]) / (data[1][i] - data[1][i+1]) < 0.6:
                                        if 0.7 < (data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-2]) < 1.5:
                                            isRemote = True
                                    
                                    # 19000的10-50的4236特殊情况
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
                                        ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
                                        0.25 < (data[1][i] - data[1][i+1]) / (data[1][i+1] - data[1][i+2]) < 0.3 and \
                                        0.4 < (data[1][i] - data[1][i-2]) / (data[1][i] - data[1][i+2]) < 0.55:
                                        isMout = False
                                        break

                                    # 19000的10-50的4522特殊情况
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) < 0 and \
                                        (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) < 0 and \
                                        (data[1][i+5] - data[1][i+4])/(data[0][i+5] - data[0][i+4]) > 0 and \
                                        ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
                                        0.4 < (data[1][i] - data[1][i+1]) / (data[1][i+1] - data[1][i+4]) < 0.5 and \
                                        0.4 < (data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+4]) < 0.5:
                                        isMout = False
                                        break

                                    # 19000的10-50的4369特殊情况
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) < 0 and \
                                        (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) > 0 and \
                                        ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                        ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0 and \
                                        0.3 < (data[1][i] - data[1][i-2]) / (data[1][i-2] - data[1][i-3]) < 0.4 and \
                                        0.8 < (data[1][i+1] - data[1][i+3]) / (data[1][i] - data[1][i+1]) < 0.9 and \
                                        0.7 < (data[1][i] - data[1][i-3]) / (data[1][i] - data[1][i+3]) < 0.8:
                                        isMout = False
                                        break

                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
                                        ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
                                        (data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-1]) > 0.2 and \
                                        (data[1][i] - data[1][i-1]) / (data[1][i+1] - data[1][i+2]) < 0.7:
                                        isBorder = True
                                    
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
                                        ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
                                        (data[1][i] - data[1][i+1]) / (data[1][i+1] - data[1][i+2]) > 0.1 and \
                                        (data[1][i+1] - data[1][i+2]) / (data[1][i] - data[1][i-1]) < 0.8:
                                        isMout = False
                                        break

                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
                                        ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
                                        (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i-1]) < 0.7:
                                        isMout = False
                                        break

                                    # print((data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-1]) > 0.4)
                                    # print((data[1][i] - data[1][i-1]) / (data[1][i-1] - data[1][i-2]) < 0.3)
                                    # print((data[1][i] - data[1][i+1]) / (data[1][i+1] - data[1][i+2]) < 0.2)
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
                                        ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) > 0 and \
                                        ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
                                        (data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-1]) > 0.4 and \
                                        (data[1][i] - data[1][i-1]) / (data[1][i-1] - data[1][i-2]) < 0.3 and \
                                        (data[1][i] - data[1][i+1]) / (data[1][i+1] - data[1][i+2]) < 0.2 and \
                                        0.7 < (data[1][i] - data[1][i-2]) / (data[1][i+1] - data[1][i+3]) < 1:
                                        isMout = False
                                        break
                                    
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                        ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
                                        (data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-1]) > 0.4 and \
                                        (data[1][i] - data[1][i-1]) / (data[1][i-1] - data[1][i-2]) < 0.5 and \
                                        (data[1][i] - data[1][i+1]) / (data[1][i+1] - data[1][i+2]) < 0.3 and \
                                        0.7 < (data[1][i] - data[1][i-2]) / (data[1][i] - data[1][i+2]) < 1.2:
                                        isMout = False
                                        break
                                    

                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                        ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0 and \
                                        0.9 < (data[1][i] - data[1][i-3]) / (data[1][i] - data[1][i+1]) < 1.1:
                                        isMout = False
                                        break

                                    if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0.05 and \
                                        0.7 < (data[1][i] - data[1][i-2]) / (data[1][i] - data[1][i+1]) < 1.1:
                                        # ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0.02 and \
                                            # isRemote = True
                                        isMout = False
                                        break
                                    
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                        ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
                                        0.8 < (data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+2]) < 1.2 and \
                                        0 < (data[1][i+1] - data[1][i+2]) / (data[1][i] - data[1][i+1]) < 0.7:
                                            # isRemote = True
                                        isMout = False
                                        break

                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                        ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                        ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0 and \
                                        (data[1][i] - data[1][i-3]) / (data[1][i] - data[1][i+2]) < 1.2:
                                            # isRemote = True
                                        isMout = False
                                        break
    
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                        ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                        ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) > 0 and \
                                        ((data[1][i-4] - data[1][i-5])/(data[0][i-4] - data[0][i-5])) < 0 and \
                                        ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                        (data[1][i] - data[1][i-4]) / (data[1][i] - data[1][i+2]) < 1.2:
                                        isMout = False
                                        break
                                    
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                       ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
                                       ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                       (data[1][i+1] - data[1][i]) / (data[1][i+2] - data[1][i+1]) < 0.1:
                                        isMout = False
                                        break 
                                    
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                       ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                       ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                       ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0 and \
                                       ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
                                       (data[1][i] - data[1][i-3]) / (data[1][i] - data[1][i+3]) < 0.4:
                                        isMout = False
                                        break
                                    
                                    if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                       ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                       ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                       ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) > 0 and \
                                       ((data[1][i-4] - data[1][i-5])/(data[0][i-4] - data[0][i-5])) < 0 and \
                                       ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                       (data[1][i] - data[1][i-4]) / (data[1][i] - data[1][i+2]) < 0.4:
                                        isMout = False
                                        break

                                    isMout = True
                                    # mout_value.append(data[1][i])

                                    # if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
                                    #    ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                    #    (data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+2]) < 0.4:
                                    #     isMout = False
                                    #     break
                                    # isMout = True
                                    # mout_value.append(data[1][i])


                                if center - 1 < data[0][i] < center + 2:
                                    # if center < data[0][i] < center + 1 and abs(slope / before_slope) < 0.02 and \
                                    #     ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0:
                                    #     isMout = False
                                    #     break
                                    if center < data[0][i] < center + 1:
                                        ismiddle = True
                                    # print('center:', center)
                                    # print((data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+1]))
                                    # print((data[1][i-2] - data[1][i-1]) / (data[1][i] - data[1][i-1]))
                                    # print((data[1][i] - data[1][i+3]) / (data[1][i-2] - data[1][i-4]))
                                    # 3000-4000的10-50的475的Hb的特殊情况
                                    if center-1 < data[0][i] < center and \
                                       ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                       ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
                                       ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) > 0 and \
                                       ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                        ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) > 0 and \
                                        ((data[1][i-4] - data[1][i-5])/(data[0][i-4] - data[0][i-5])) < 0 and \
                                        0 < ((data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+1])) < 0.05 and \
                                        0 < ((data[1][i-2] - data[1][i-1]) / (data[1][i] - data[1][i-1])) < 0.11 and \
                                        0.8 < ((data[1][i] - data[1][i+3]) / (data[1][i-2] - data[1][i-4])) < 0.9:
                                        # print('1')
                                        # ((data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i+1])) < 0.01:
                                        isMout = False
                                        break

                                    # if center < data[0][i] < center + 1 and \
                                    #     ((data[1][i] - data[1][i+1])/(data[1][i+1] - data[1][i+2])) < 0.08 and \
                                    #     ((data[1][i+2] - data[1][i+3])/(data[1][i+1] - data[1][i+2])) < 0.01 and \
                                    #     ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                    #     ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
                                    #     ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) > 0 and \
                                    #     ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0:
                                    #     ispadd_four = True
                                    
                                    # if center < data[0][i] < center + 1 and \
                                    #    ((data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+1])) < 0.1 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0:
                                    #     # print('2')
                                    #     isMout = False
                                    #     # print('1')
                                    #     break

                                    # 19000中的10-50的4428
                                    # if center < data[0][i] < center + 1 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                    #     ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                    #     ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0 and \
                                    #     0.4 < ((data[1][i] - data[1][i-3]) / (data[1][i] - data[1][i+1])) < 0.5 and \
                                    #     ((data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i+1])) < 0.01:
                                    #     # print('3')
                                    #     isMout = False
                                    #     break
                                    
                                    # if center < data[0][i] < center + 1 and \
                                    #    ((data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-1])) < 0.2 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0:
                                    #     ispadd_three = True

                                    # if center < data[0][i] < center + 1 and \
                                    #    ((data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-1])) < 0.1 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0:
                                    #     isMout = False
                                    #     # print('3')
                                    #     # print('2')
                                    #     break
                                    # if center < data[0][i] < center + 1 and \
                                    #    ((data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+1])) < 0.1 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0:
                                    #     isMout = False
                                        # print('2')
                                        # break
                                

                                    # if center < data[0][i] < center + 1 and \
                                    #    ((data[1][i] - data[1][i-2]) / (data[1][i] - data[1][i+1])) < 0.1 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                    #    ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0:
                                    #     isMout = False
                                    #     # print('3')
                                    #     break

                                    # 19000的10-50的5440特殊情况
                                    # if center < data[0][i] < center + 1 and \
                                    #    0.5 < ((data[1][i-2] - data[1][i-1]) / (data[1][i] - data[1][i-1])) < 0.6 and \
                                    #     0.5 < ((data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+2])) < 0.6 and \
                                    #     0.8 < ((data[1][i] - data[1][i+2]) / (data[1][i-2] - data[1][i-4])) < 0.9 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                    #     ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
                                    #    ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                    #     ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) > 0 and \
                                    #     ((data[1][i-4] - data[1][i-5])/(data[0][i-4] - data[0][i-5])) < 0:
                                    #     ispadd_five = True
                                    
                                    # 8000中10-50的3715特殊情况
                                    # print(((data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-2])))
                                    # print(((data[1][i+2] - data[1][i+1]) / (data[1][i] - data[1][i-2])))
                                    # if center < data[0][i] < center + 1 and \
                                    #    ((data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-2])) < 0.5 and \
                                    #    0.5 < ((data[1][i+2] - data[1][i+1]) / (data[1][i] - data[1][i+1])) < 1.2 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                    #     ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
                                    #     ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) > 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                    #    ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0:
                                    #     isMout = False
                                    #     # print('3')
                                    #     break

                                    # # 3000-4000中的0-10的338的特殊情况
                                    # if center < data[0][i] < center + 1 and \
                                    #    ((data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-1])) < 0.03 and \
                                    #    ((data[1][i] - data[1][i-1]) / (data[1][i+1] - data[1][i+4])) < 0.4 and \
                                    #     ((data[1][i-3] - data[1][i-1]) / (data[1][i] - data[1][i-1])) < 0.2 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                    #     ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
                                    #     ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) < 0 and \
                                    #     ((data[1][i+5] - data[1][i+4])/(data[0][i+5] - data[0][i+4])) > 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
                                    #    ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
                                    #     ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) > 0:
                                    #     isMout = False
                                    #     # print('3')
                                    #     break
                                    
                                    # # 8000中10-50的2094特殊情况
                                    # if center < data[0][i] < center + 1 and \
                                    #    ((data[1][i] - data[1][i-2]) / (data[1][i] - data[1][i+4])) < 0.2 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                    #     ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
                                    #     ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) < 0 and \
                                    #     ((data[1][i+5] - data[1][i+4])/(data[0][i+5] - data[0][i+4])) > 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                    #    ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0:
                                    #     isMout = False
                                    #     # print('3')
                                    #     break

                                    # if center < data[0][i] < center + 1 and \
                                    #    ((data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-2])) < 0.29 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                    #    ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0:
                                    #     ispadd = True

                                    # if center < data[0][i] < center + 1 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                    #     ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
                                    #     ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) > 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
                                    #    ((data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-1])) < 0.5 and \
                                    #    ((data[1][i+2] - data[1][i+1]) / (data[1][i+2] - data[1][i+3])) < 0.5 and \
                                    #    0.8 < ((data[1][i] - data[1][i-1]) / (data[1][i+2] - data[1][i+3])) < 1.2:
                                    #    isMout = False
                                    # #    print('3')
                                    #    break
                                        
                                    # if center < data[0][i] < center + 1 and \
                                    #    ((data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-2])) < 0.1 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                    #    ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0:
                                    #     isMout = False
                                    #     # print('3')
                                    #     break

                                    # if center < data[0][i] < center + 1 and \
                                    #    ((data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-2])) < 0.1 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                    #    ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                    #     ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0:
                                    #     isMout = False
                                    #     # print('3')
                                    #     break

                                    # # 19000的10-50中的5440特殊情况
                                    # if center < data[0][i] < center + 1 and \
                                    #    ((data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-2])) < 0.1 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                    #    ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                    #     ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0:
                                    #     isMout = False
                                    #     # print('3')
                                    #     break

                                    # 12000中的10-50的1816的特殊情况
                                    # if center < data[0][i] < center + 1 and \
                                    #    ((data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-3])) < 0.2 and \
                                    #    0.9 < ((data[1][i] - data[1][i+2]) / (data[1][i+3] - data[1][i+2])) < 1.1 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                    #     ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
                                    #     ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) < 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
                                    #    ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
                                    #     ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0:
                                    #     isMout = False
                                    #     # print('3')
                                    #     break

                                    # if center < data[0][i] < center + 1 and \
                                    #    ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
                                    #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
                                    #    ((data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+2])) < 0.1:
                                    # #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0:
                                    #     isMout = False
                                    #     print('4')
                                    #     break
                                    # print('增加峰值')
                                    isMout = True
                                    # mout_value.append(data[1][i])
                            
                        # else:
                            # peak_value.append(data[1][i])
                    elif before_slope < 0 and slope > 0:
                        # if center - 2 < data[0][i] < center - 1:
                        #     isSpecial = True
                        
                        if center < data[0][i] < center + 1:
                            isMout = False
                            break

                    # if center + 1 < data[0][i] < center + 2:
                    #     if (data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-2]) < 0.05:
                    #         isMout = False
                    #         break 
                        # if center + 1 < data[0][i] < center + 2:
                        #     if not isMout_middle:
                        #         isMout = False
                        #         break
                    elif before_slope < 0 and slope < 0:
                        if center < data[0][i] < center + 1 and (data[1][i-1] - data[1][i+1]) / (data[1][i] - data[1][i+1]) < 0.1 and \
                           (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) > 0:
                            if not isMout_middle:
                                # print('5')
                                isMout = False
                    # elif before_slope > 0 and slope > 0 and 0.8 < abs(before_slope / slope) < 1.2:
                    #     if center < data[0][i] < center + 1:
                    #         if not isMout_middle:
                    #             isMout = False
                        # if center + 1 < data[0][i] < center + 2 and abs(abs(before_slope) - abs(slope)) < 1:
                        #     isMout = False
                        #     break
                if slope != 0:
                    before_slope = slope
                #检查是否有峰值，如果没有可以直接退出来
                # if data[0][i] >= center+2 and not isMout:
                #     break
        # if min_value > value:
        #     min_value = value 
        # peak_value.append(value)
        # peak_value = np.array(peak_value)
    
        if len(params) > 0 and len(one_wave) > 0:
            params[0].append(one_wave)

        if isMout and len(dis_center) != 0 and min(dis_center.values()) < 2:
            min_wave = min(dis_center, key = dis_center.get)
            # print('center:{0}, dis_center[min_wave]:{1},'.format(center,dis_center[min_wave]))
            trust += 1 / dis_center[min_wave]
            # 开始增强
            # if int(data[0][min_wave]) == center:
            #     trust += trust
            # if dis_center[min_wave] < 1:
            #     trust += trust
            # print('center:{0}, dis_center[min_wave]:{1},trust:{2}'.format(center,dis_center[min_wave],trust))  
            trust += getTwoSideHightByDifferent(data, min_wave)
            # print('two_trust:', trust)

        if trust < 1.5 and isRemote:
            trust = 0
        if trust < 1 and isBorder:
            trust = 0
        if 0.04 < trust < 0.06 and not ismiddle:
            trust = 0
        if trust < 0.04:
            trust = 0
        if trust < 1 and ispadd:
            trust = 0
        if trust < 1 and ispadd_two:
            trust = 0
        if trust < 0.4 and ispadd_three:
            trust = 0
        if trust < 1 and ispadd_four:
            trust = 0
        if trust < 1.17 and ispadd_five:
            trust = 0    
    return trust    