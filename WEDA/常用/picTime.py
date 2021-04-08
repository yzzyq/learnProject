import copy
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import xlwt
import os
from matplotlib.font_manager import FontProperties


if __name__ == '__main__':
    color_set = ['salmon', 'amber', 'baby poop green','aqua', 'windows blue', 'baby purple','bubblegum pink']
    legend_set = ['ASUWO', 'BSVM', 'MSSVM', 'multitrain', 'ssoSMOTEsso','VBensembles','wcrank']
    time = [[304.67855030000004, 891.5890271, 3178.1495494], [10108.4394453, 10819.2379265, 13170.1219843], 
            [47841.4482133, 48500.3794513, 50727.5763556], [3093.5495290999997, 4050.7318622, 8042.715062099998], 
            [385.5890895, 968.1393223, 3298.7447880000004], [34965.32367069999, 35616.2371611, 37915.40542829999],
            [11.7934775, 424.29736790000004, 2004.5705459]]
    data_num = [617,8202,19411]
    sns.set_style('darkgrid',{"axes.facecolor": ".9"})
    sns.set_context('paper',font_scale=1,rc={"lines.linewidth": 1.5})
    sns.set(font_scale=1,font='Times New Roman')
    y_pos = list(range(len(time)))
    width = 0.7/2
    plt.figure(figsize=(9,7))
    plt.title('all algorithms time')
    plt.xlim((0,60000))
    plt.barh(y_pos,time,height = 0.7/2,color='steelblue',alpha = 0.8)
    plt.yticks(range(len(legend_set)),legend_set)
    plt.xlabel('time')
    for x,y in enumerate(time):
        plt.text(y+0.4,x-0.2,'%s'%y )
        
    for i in range(len(y_pos)):
        y_pos[i] = y_pos[i] + width
    
    plt.barh(y_pos,time,height = 0.7/2, color='red',alpha = 0.8)
    plt.yticks(range(len(legend_set)),legend_set)
    plt.xlabel('time')
    for x,y in enumerate(time):
        plt.text(y+0.2,x-0.1,'%s'%y )
    
    ax = plt.gca()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*0.85 , box.height])
    plt.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0,fontsize = 9,
               handleheight = 3)
    plt.grid(True)
    

    plt.show()
