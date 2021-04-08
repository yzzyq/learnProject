import fitsData
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# 画出全部数据的点图
def drawPoint(data_pos):
    pos_pd = pd.DataFrame(data_pos, columns = ["latitude", "longitude"])
    sns.jointplot(x = "latitude", y = "longitude", data = pos_pd, height = (10))
    plt.show()


if __name__ == '__main__':
    file_path = "E:/second/second-1"
    # file_path = "500-600/0-10"
    dataSet, allPoistion, all_file_name = fitsData.exractData(file_path)
    print(allPoistion)
    drawPoint(allPoistion)
