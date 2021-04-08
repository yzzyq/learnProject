import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 提取出我们需要的权重数据
def extractWeights(file_name):
    all_weights_data = []
    before_weight = 0
    with open(file_name, 'r') as f:
        for index,line_data in enumerate(f.readlines()):
            # one_weight_data = [index]
            tep = line_data.split('[')[1].split(']')[0]
            temp_weight = tep.split(',')
            temp_weight = [float(weight) for weight in temp_weight]
            if abs(temp_weight[0] - before_weight) > 0.1:
                one_weight_data = [index,'primary weight',temp_weight[0]]
                all_weights_data.append(one_weight_data)
                one_weight_data = [index,'secondary weight',temp_weight[1]]
                all_weights_data.append(one_weight_data)
                before_weight = temp_weight[0]
            if index > 64:
                break
            # one_weight_data.extend(temp_weight.split(','))
            # one_weight_data = [float(weight) for weight in one_weight_data]
            # print(one_weight_data)
            # all_weights_data.append(one_weight_data)
    return all_weights_data 


if __name__ == '__main__':
    file_name = 'C:/Users/spiderJ/Desktop/4.txt'
    # 提取出我们需要的权重数据
    weights = extractWeights(file_name)
    weights_pd = pd.DataFrame(weights, columns = ['index', 'weight class', 'weight value'])
    # 画出图像
    sns.set(style="whitegrid", color_codes=True)
    plt.figure(figsize=(9,7))
    sns.pointplot(x = 'index' , y = 'weight value', hue = 'weight class', data = weights_pd, 
                  palette = {'primary weight':'g', 'secondary weight':'m'},
                  markers = ['^','o'], linestyles = ['-', '--'])
    plt.show()
    




