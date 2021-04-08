from astropy.io import fits
import os
import copy
import numpy as np
import random

#对单个光谱数据的处理
def readfits(path,fileName):
    dfu = fits.open(path + '/'+fileName)
    #初始波长
    beginWave = dfu[0].header['COEFF0']
    #步长
    step = dfu[0].header['CD1_1']
    #读出数据中的位置
    #位置
    ra = dfu[0].header['ra']
    dec = dfu[0].header['DEC']
    snrr_stn = dfu[0].header['snrr']
    snri_stn = dfu[0].header['snri']
    poistion = [float(ra),float(dec)]
    #光谱中的流量 
    flux = dfu[0].data[0]
    #求出波长,求出与流量对应的波长
    wave = np.array([10**(beginWave + step*j) for j in range(len(flux))])
    data = [wave,flux]
    #-------------------------------------------
    return data,poistion,snrr_stn,snri_stn

#数据文件中的光谱数据
def exractData(fileName):
    listFile = os.listdir(fileName)
    # 分为三类数据
    three_ston_dataSet = [[],[],[]]
    three_ston_Poistion = [[],[],[]]
    three_ston_index = [[],[],[]]
    three_ston_fileName = [[],[],[]]
    for file_index, one_file in enumerate(listFile):
        data,poistion,snrr_stn,snri_stn = readfits(fileName,one_file)
        index = 0
        # print(snrr_stn,snri_stn)
        if 0 <= snrr_stn <= 10 and 0 <= snri_stn <= 10:
            three_ston_dataSet[0].append(data)
            three_ston_Poistion[0].append(poistion)
            three_ston_index[0].append(file_index)
            three_ston_fileName[0].append(one_file)
            index = 1
        if 10 < snrr_stn <= 50 and 10 < snri_stn <= 50:
            three_ston_dataSet[1].append(data)
            three_ston_Poistion[1].append(poistion)
            three_ston_index[1].append(file_index)
            three_ston_fileName[1].append(one_file)
            index = 2
        if snrr_stn > 50 and snri_stn > 50:
            three_ston_dataSet[2].append(data)
            three_ston_Poistion[2].append(poistion)
            three_ston_index[2].append(file_index)
            three_ston_fileName[2].append(one_file)
            index = 3
        if index == 0:
            # print('====================================================================================')
            # print(one_file)
            # print(snrr_stn,snri_stn)
            # print('====================================================================================')
            mean_snr = (snrr_stn + snri_stn) / 2
            # snrr_stn = int(snrr_stn)
            # snri_stn = int(snri_stn)
            if 0 <= mean_snr <= 10:
                three_ston_dataSet[0].append(data)
                three_ston_Poistion[0].append(poistion)
                three_ston_index[0].append(file_index)
                three_ston_fileName[0].append(one_file)
                # print('第一类')
                index = 1
            if 10 < mean_snr <= 50:
                three_ston_dataSet[1].append(data)
                three_ston_Poistion[1].append(poistion)
                three_ston_index[1].append(file_index)
                three_ston_fileName[1].append(one_file)
                # print('第二类')
                index = 2
            if mean_snr > 50:
                three_ston_dataSet[2].append(data)
                three_ston_Poistion[2].append(poistion)
                three_ston_index[2].append(file_index)
                three_ston_fileName[2].append(one_file)
                index = 3
            # if index == 0:
            #     print(mean_snr, snrr_stn, snri_stn)
            # if 0 <= snrr_stn <= 10 and 0 <= snri_stn <= 10:
            #     three_ston_dataSet[0].append(data)
            #     three_ston_Poistion[0].append(poistion)
            #     three_ston_index[0].append(file_index)
            #     index = 1
            #     # print('第一类')
            # if 10 < snrr_stn <= 50 and 10 < snri_stn <= 50:
            #     three_ston_dataSet[1].append(data)
            #     three_ston_Poistion[1].append(poistion)
            #     three_ston_index[1].append(file_index)
            #     index = 2
            #     # print('第二类')
            # if snrr_stn > 50 and snri_stn > 50:
            #     three_ston_dataSet[2].append(data)
            #     three_ston_Poistion[2].append(poistion)
            #     three_ston_index[2].append(file_index)
            #     index = 3
                # print('第三类')
            # if index == 0:
            #     print(snrr_stn, snri_stn)
    print('0-10:{0},10:50:{1},50:{2}'.format(len(three_ston_dataSet[0]), len(three_ston_dataSet[1]), len(three_ston_dataSet[2])))
    return three_ston_dataSet, three_ston_Poistion, three_ston_index, three_ston_fileName