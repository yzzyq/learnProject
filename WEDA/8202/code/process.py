import copy
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import xlwt
import os
import pandas as pd
import math
from matplotlib.font_manager import FontProperties
from itertools import product

#主要用的思想：1.将数据分为俩组,  一组就是只看第一列，原因就是2作为切分阈值，可能切出来的可能不准确
#                              一组就是需要通过后面的数据来看是否是正类
#             2.将这俩组数据通过动态权重的来进行混合起来
def threeColProcess(dataProcess,no_class_index,preset_weight,k = 1,this_gap = 0.1):
    #正类数据和无类别数据进行划分成俩组
    data_copy = []
    no_class_index_copy = copy.deepcopy(no_class_index)

    #区分自身数据的每个阶段的个数，用于后面权重的调整
    num_stage = np.zeros(10)
    for index in no_class_index:
        #对数据进行归一化处理
        data_copy.append(dataProcess[index,:-1])
        if dataProcess[index,0] > 1:
            num_stage[int((dataProcess[index,0] % 1)*10)] += 1
    # print('num_stage:',num_stage)
    if sum(num_stage) == 0:
        return []
    two_max_gap = 0.5
    # 最多取一半数据的步长
    if sum(num_stage[1:3]) > 0:
        two_max_gap = (0.8 - 0.5) / (sum(num_stage[1:3])*0.5)
    data_copy = np.array(data_copy)
    one_min_gap = 0.1
    #通过不稳定数据计算出初始权重,看最大的那个就行了
    entropy_weights = [0,0]
    if sum(num_stage[3:]) > 0:
        entropy_weights = getWeight(data_copy,preset_weight,num_stage,no_class_index)
        one_min_gap = (entropy_weights[0] - 0.8) / (sum(num_stage[3:])*0.9)
    else:
        entropy_weights[0] = 0.8
        entropy_weights[1] = 0.2
    start_weights = entropy_weights[0]
        
    past_weight = 0
    #对数据进行归一化处理，之后再使用
    data_copy = normalizaedData(data_copy)

    #使用渐变权重排序出的结果
    choice_index = []

    #查看前一个是多少
    before_one = 0
    sum_num = len(no_class_index_copy)
    inver_weight = 0
    inver_weight_max_gap = 0
    inver_weight_min_gap = 0
    #使用权重对第一组和第二组数据进行计算
    while len(no_class_index_copy) > 0:
        past_weight += entropy_weights[0]
        # print('entropy_weights:',entropy_weights)
        current_sum = []

        for index in range(len(no_class_index_copy)):
            tmp_sum = entropy_weights[0]*data_copy[index,0] + \
                      entropy_weights[1]*(preset_weight[0]*data_copy[index,1] + preset_weight[1]*data_copy[index,2])
            current_sum.append(tmp_sum)
        #将之从大到小进行排序
        sort_sum = np.argsort(-np.array(current_sum))

        current_one = 0 
        if len(sort_sum) > k:
            current_one = data_copy[sort_sum[k],0]

        sort_current = sort_sum[:k]
        sum_one = 0
        for sort_index in sort_current:
            sum_one += data_copy[sort_index,0]
            choice_index.append(no_class_index_copy[sort_index])
            #从未分类数据中删除该数据
            
            data_copy = np.delete(data_copy,sort_index,axis = 0)
            del no_class_index_copy[sort_index]
        #将之前的权重存储起来，用于下一次进行对比
        before_one = sum_one / k

        #通过前后k的数值来进行更新权重
        if entropy_weights[0] <= 1 and sum(num_stage) != 0 and inver_weight == 0:
            entropy_weights = updateWeight(before_one,current_one,entropy_weights,
                                           num_stage,this_gap,past_weight,two_max_gap,one_min_gap)
        else:
            entropy_weights = updateWeightByTwo(before_one,current_one,entropy_weights,past_weight,inver_weight_max_gap,inver_weight_min_gap)
        
        if len(no_class_index_copy) / sum_num < 0.7 and entropy_weights[1] == 1 and len(no_class_index_copy) > 4:
            entropy_weights[0] = max(start_weights - 0.2,0.6)
            # entropy_weights[0] = start_weights
            entropy_weights[1] = 1 - entropy_weights[0]
            past_weight = past_weight*0.1
            inver_weight += 1
            sum_num = len(no_class_index_copy)
            inver_weight_max_gap = entropy_weights[0] / (sum_num*0.2)
            inver_weight_min_gap = entropy_weights[0] / (sum_num*0.25)
            
    return choice_index

#z-score归一化数据,这里会变成0均值，那么相加得到的值几乎是0，后序就无法求和
def normalizaedData(data_copy):
    # for col in range(len(data_copy[0]) - 1):
        # max_value = max(data_copy[:,col + 1])
        # min_value = min(data_copy[:,col + 1])
        # data_copy[:,col+1] = (data_copy[:,col+1] - min_value) / (max_value - min_value)
    max_value = max(data_copy[:,1])
    min_value = min(data_copy[:,1])
    if max_value != min_value:
        data_copy[:,1] = (data_copy[:,1] - min_value) / (max_value - min_value)
    return data_copy


def getWeight(data_copy,preset_weight,num_stage,no_class_index):
    entropy_weights = [0.5,0.5]
    #得出的数据还应该进行排序过，这时候使用的就是排序完的数据
    data_two_col = getTarget(data_copy,preset_weight)
    all_num = 0

    #得出我们需要判断前多少个数据的信息
    for num_index in range(len(num_stage) - 1):
        true_index = len(num_stage) - num_index - 1
        if num_stage[true_index] > 0:
            all_num += num_stage[true_index]
            if num_stage[true_index - 1] / num_stage[true_index] >= 2 and num_stage[true_index] >= 4:
                all_num += num_stage[true_index - 1] / 2
                break
    
    one_col = 0
    two_col = 0
    index_need_process = []
    for col in range(2):
        tmp_result = np.argsort(-data_two_col[:,col])
        len_tmp_result = len(tmp_result)
        for index in range(len_tmp_result):
            if col == 0 and len(index_need_process) < all_num:
                index_need_process.append(tmp_result[index])
            data_two_col[tmp_result[index],col] = (len_tmp_result - index) / len_tmp_result

    two_col_gap = 0

    for index in index_need_process:
        tmp_gap = abs(data_two_col[index,0] - data_two_col[index,1])
        if tmp_gap > two_col_gap:
            two_col_gap = tmp_gap
    
    # print('two_col_gap:',two_col_gap)
    entropy_weights[0] += two_col_gap

    entropy_weights[1] -= two_col_gap
    # entropy_weights[1] = 1 - two_col_gap

    entropy_weights[0] = min(1, entropy_weights[0])
    entropy_weights[1] = max(entropy_weights[1], 0)
    
    return entropy_weights

def updateWeightByTwo(before_one,current_one,entropy_weights,past_weight,inver_weight_max_gap,inver_weight_min_gap):
    #首次之后的权重迭代方法
    dissipate = 0.1
    learn_ratio = 0.1
    gap = dissipate*past_weight + abs(current_one - before_one)
    gap = min(learn_ratio*gap,inver_weight_max_gap)
    gap = max(gap,inver_weight_min_gap)
    entropy_weights[0] -= gap
    entropy_weights[1] += gap
    if entropy_weights[0] <= 0:
        entropy_weights[0] = 0.01
    elif entropy_weights[0] > 1:
        entropy_weights[0] = 1
    if entropy_weights[1] > 1:
        entropy_weights[1] = 1
    elif entropy_weights[1] < 0:
        entropy_weights[1] = 0
    return entropy_weights


# #更新权重
# def updateWeight(before_one,current_one,entropy_weights,num_stage,this_gap,past_weight):
#     #只是对第一列进行缩小，不对之进行反弹放大
#     # gap = before_one - current_one
#     # gap = abs(before_one - current_one)
#     # before_num = int((before_one % 1)*10)
#     # current_num = int((current_one % 1)*10)
#     # #如果数据从一个阶段跌落下来，比如从1.2到了1.1，那么就会根据这个阶段的数量减去一个置信度 
#     # if current_num > 1 and before_num != current_num:
#     #     gap += num_stage[current_num] / sum(num_stage)
#     # print('current_one:',current_one)    
#     # gap = gap / this_gap
#     # if current_one != 0:
#     #     gap = gap / ((current_one + before_one) / 2)



#     # 对于下降的速度，一共是三个方面，一个是过去，主要功能就是慢慢加速
#     #                              一个是现在和将来，指会下降多少
#     # 过去的消散指数
#     # dissipate = 0.1
#     before_num = int((before_one % 1)*10)
#     current_num = int((current_one % 1)*10)
#     dissipate = this_gap
#     # print('current_one:',current_one)
#     # print('before_one:',before_one)
#     # 如今的学习率
#     # current_num = int((current_one % 1)*10)
#     # learn_ratio = 1
#     gap = 0
#     if current_num > 0:
#         learn_ratio = sum(num_stage[current_num:]) / sum(num_stage)


#     gap = dissipate*past_weight + abs(current_one - before_one)

#     learn_ratio = 0.1
#     # if current_num > 2:
#     #     # print('不一样的')
#     #     gap = dissipate*past_weight + abs(current_one - before_one)
#     # elif 0 < current_num <= 2:
#     #     # print('一样的')
#     #     first = len(num_stage) - 1
#     #     while first > 0:
#     #         if num_stage[first] > 0:
#     #             break
#     #         else:
#     #             first -= 1
#     #     gap = dissipate*past_weight + abs(current_one - before_one) + (first - current_num) / 10
#     # elif current_num == 0:
#     #     gap = past_weight
#     # print('gap:',gap)
#     # print('学习率：',learn_ratio)    
#     gap = learn_ratio*gap

#     entropy_weights[0] -= gap
#     entropy_weights[1] += gap
#     if entropy_weights[0] < 0:
#         entropy_weights[0] = 0
#     elif entropy_weights[0] > 1:
#         entropy_weights[0] = 1
#     if entropy_weights[1] > 1:
#         entropy_weights[1] = 1
#     elif entropy_weights[1] < 0:
#         entropy_weights[1] = 0
#     return entropy_weights


#更新权重
def updateWeight(before_one,current_one,entropy_weights,num_stage,this_gap,past_weight,two_max_gap,one_min_gap):
    
    before_num = int((before_one % 1)*10)
    current_num = int((current_one % 1)*10)
    # dissipate = this_gap
    # learn_ratio = 0
    learn_ratio = 0.1
    gap = 0
    # if current_num > 0:
    #     learn_ratio = sum(num_stage[current_num:]) / sum(num_stage)
    dissipate = 0.1
    if current_num > 2:
        # dissipate = 0.1
        # learn_ratio = 0.1
        gap = dissipate*past_weight + abs(current_one - before_one)
        gap = learn_ratio*gap
        if gap > one_min_gap:
            gap = one_min_gap
    elif 0 < current_num <=2:
        # dissipate = 0.3
        # learn_ratio = 0.2
        gap = dissipate*past_weight + abs(current_one - before_one)
        gap = learn_ratio*gap
        if sum(num_stage[1:3]) > 3:
            # (0.7 - 0.5) / (sum(num_stage[1:3])/2)
            # print('gap:',gap)
            # print('(0.8 - 0.5) / (sum(num_stage[1:3])*0.3):',(0.8 - 0.5) / (sum(num_stage[1:3])*0.3))
            gap = min((0.8 - 0.5) / (sum(num_stage[1:3])*0.3),gap)
        # if gap > 0.1:
        #     gap = 0.1
        # print('gap:',gap)
        # print('two_max_gap:',two_max_gap) 
        gap = max(two_max_gap,gap)
        # print('gap:',gap)
        # mm = mm
        # if gap < two_max_gap:
        #     gap = two_max_gap 
    elif current_num == 0:
        # dissipate = 0.5
        # learn_ratio = 0.3
        gap = dissipate*past_weight + abs(current_one - before_one) 
        gap = learn_ratio*gap
    # print('entropy_weights:',entropy_weights)
    # print('gap:',gap)
    entropy_weights[0] -= gap
    entropy_weights[1] += gap
    # print('entropy_weights:',entropy_weights)

    # if entropy_weights[0] < 0.7 and current_num > 2:
    #     entropy_weights[0] = 0.7
    # if current_num <= 2 and entropy_weights[0] > 0.7:
    #     entropy_weights[0] = 0.7 

    # print('entropy_weights:',entropy_weights)
    if entropy_weights[0] <= 0:
        entropy_weights[0] = 0.01
    elif entropy_weights[0] > 1:
        entropy_weights[0] = 1
    if entropy_weights[1] > 1:
        entropy_weights[1] = 1
    elif entropy_weights[1] < 0:
        entropy_weights[1] = 0
    return entropy_weights

#将三列合并成俩列
def getTarget(data_copy,preset_weight):
    data_no = np.zeros((len(data_copy),2))
    data_no[:,0] = data_copy[:,0]
    # data_value = set(data_copy[:,2])
    data_no[:,1] = preset_weight[0]*data_copy[:,1] + preset_weight[0]*data_copy[:,2]
    return data_no 

def trueClassWriteExcel(dataProcess,threshold,result_path,file_path,true_data):
    true_result = []
    list_dir = os.listdir(file_path)
    
    for index in range(len(dataProcess)):
        if dataProcess[index,-1] == 1:
            one_reult = []
            one_reult.append(list_dir[index])
            one_reult.append(index+1)
            one_reult.append(dataProcess[index,0])
            one_reult.append(dataProcess[index,1])
            one_reult.append(dataProcess[index,2])
            one_reult.append(dataProcess[index,3])
            true_result.append(one_reult)
    
    recall,precise = getRecallAndPrecise(dataProcess,true_data)

    #将相关的数据写入到文件中去
    book = xlwt.Workbook(encoding='utf-8')
    sheet1 = book.add_sheet('data',cell_overwrite_ok=True)
    sheet1.write(0,0,'文件名')
    sheet1.write(0,1,'序号')
    sheet1.write(0,2,'自身发射线')
    sheet1.write(0,3,'线表')
    sheet1.write(0,4,'周围数据')
    sheet1.write(0,5,'类别')
    len_true = len(true_result) 
    for line in range(len_true):
        len_col = len(true_result[0])
        for col in range(len_col):
            sheet1.write(line+1,col,str(true_result[line][col]))

    sheet1.write(len_true+3,0,'召回')
    sheet1.write(len_true+3,1,recall)

    sheet1.write(len_true+4,0,'精确')
    sheet1.write(len_true+4,1,precise)
    
    book.save(result_path + '/'+ str(threshold) +'-threshold.xls')
    
    return recall,precise


def getRecallAndPrecise(dataProcess,true_data):
    true_index = 0
    init_data = []
    true_num = 0
    for index in range(len(dataProcess)):
        if dataProcess[index,-1] == 1:
            true_num += 1
            if (index+1) in true_data:
                init_data.append(index+1)
                true_index += 1
            elif dataProcess[index,-1] == 1 and (index+1) not in true_data:
                print(index+1)
##    for index in range(len(dataProcess)):
##        if dataProcess[index,-1] == 1 and (index+1) in true_data:
##            # print(index+1)
##            # print(dataProcess[index,:-1])
##            true_num += 1
##            init_data.append(index+1)
##            true_index += 1
        
    #     elif dataProcess[index,-1] == 1 and (index+1) not in true_data:
    #         print(index+1)
    # print('---------------------------------')
    # print()
##    print('开始查找')
    # print('init_data:',init_data)
    print('--------------------------------------')
    for data in true_data:
        if data not in init_data:
            print(data)
    print('召回的个数:{0},全部为正的个数{1},判断为正的个数{2}'.format(true_index, len(true_data), true_num))
    print('-----------------')
    precise = 1
    if true_num != 0:
        precise = true_index / true_num

    recall = true_index / len(true_data)
    return recall,precise



#将所有的召回率和精确率写入到文件中
def allThresholdWriteExcel(all_criteria,result_fileName):
    book = xlwt.Workbook(encoding='utf-8')
    sheet1 = book.add_sheet('data',cell_overwrite_ok=True)
    sheet1.write(0,0,'数量比阈值')
    sheet1.write(0,1,'总和阈值')
    sheet1.write(0,2,'召回率')
    sheet1.write(0,3,'精确率')
    for threshold_amount in range(len(all_criteria)):
        for col in range(4):
            sheet1.write(threshold_amount+1,col,str(all_criteria[threshold_amount][col]))
    book.save(result_fileName+'/all-result.xls')


#对我们的各数据评价标准画出折线图
def drawEvaluationStandard(all_recall_precise):
    # ch.set_ch()
    all_recall_precise = np.array(all_recall_precise)
    myfont=FontProperties(fname='C:\Windows\Fonts\simhei.ttf',size=14)
    sns.set(font=myfont.get_name())
    sns.set_style('darkgrid',{"axes.facecolor": ".9"})
    sns.set_palette('Set2')
    sns.set_context('paper',font_scale=1,rc={"lines.linewidth": 1.5})
    sns.set(font=myfont.get_name())
    # plt.style.use('ggplot')
    plt.figure(figsize=(7,5))
    plt.title('数据的信噪比50以上,权重1-0.5-0.5下阈值的大小与召回、精确的关系')

    # plt.title('阈值的大小与召回、精确的关系')
    plt.xlabel('数量比阈值')
    plt.xlim((0.001,0.07))
    #分为俩个线段
    #数量阈值和召回
    # for index in range(len(all_recall_precise)):
    # plt.subplot(3,4,index+1)
    # plt.xlim((0.02,0.12))
    plt.plot(all_recall_precise[:,0],all_recall_precise[:,1],label='召回率')
    #数量阈值和精确率
    plt.plot(all_recall_precise[:,0],all_recall_precise[:,2],label='精确率')
    # plt.legend(loc='best')
    # plt.legend(loc='upper right')
    plt.legend(loc='best')
    plt.grid(True)
    # plt.legend(handles = [threshold_recall,threshold_precise],labels=['recall','precise'],loc='upper right')
    # sns.despine()
    # plt.plot_date(x_date,data['close'],'-',label="收盘价")
    # plt.plot_date(x_date,data['high'],'-',label="最高价")
    # plt.legend()
    # plt.grid(True)
    plt.show() 
    

def drawData(dataProcess):
    dataSet_pd = pd.DataFrame(dataProcess,columns=['Ha','frame','neighbor data','class'])
    myfont=FontProperties(fname='C:\Windows\Fonts\simhei.ttf',size=14)
    sns.set(font=myfont.get_name())
    sns.set_style('darkgrid',{"axes.facecolor": ".9"})
    sns.set_palette('Set2')
    sns.set_context('paper',font_scale=1,rc={"lines.linewidth": 1.5})
    sns.set(font=myfont.get_name())
    plt.rcParams['axes.unicode_minus'] = False
    f,(ax1,ax2,ax3) = plt.subplots(1,3,figsize=(11,14),sharex=True)
    #最基本的
    sns.boxplot(x = 'class',y = 'Ha',data = dataSet_pd,ax=ax1,palette="Set2")
##    sns.swarmplot(x = '类别',y = '自身位置',data = dataSet_pd,ax=ax1,color='000')

    sns.boxplot(x = 'class',y = 'frame',data = dataSet_pd,ax=ax2,palette="Set2")
##    sns.swarmplot(x = '类别',y = '线表',data = dataSet_pd,ax=ax2,alpha=.5,color='w')

    sns.boxplot(x = 'class',y = 'neighbor data',data = dataSet_pd,ax=ax3,palette="Set2")
##    sns.swarmplot(x = '类别',y = '线表',data = dataSet_pd,ax=ax3,color='.25')

    plt.show()




