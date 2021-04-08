# 根据索引找出我们所需要的文件名称
import os

def chooseFileName(true_index, fileName, result_file):
    dir_name = os.listdir(fileName)
    all_true_file = []
    write_file_name = ['0-10', '10-50', '50']
    for index,name in enumerate(dir_name):
        one_true_index = true_index[index]
        all_file = os.listdir(fileName + '/' + name)
        one_true_index = list(map(lambda x: x-1, one_true_index))

        with open(result_file + '/' + write_file_name[index] + '.txt', 'a') as f:
            one_true_file = [f.write(all_file[file_index] + '\n') for file_index in one_true_index]
        # print(one_true_file)
        # print(len(one_true_file))
        all_true_file.append(one_true_file)
    return all_true_file


if __name__ == '__main__':
    true_index = [[22, 288, 713, 249, 186, 307, 647, 209, 745, 154, 700, 480],              
              
                  [761, 789, 895, 896, 1185, 1275, 1302, 1453, 2388, 2522, 2619, 2688, 2694, 2697, 2960, 2976, 2978, 3132, 3185, 303, 2555,
                   3297, 3371, 3377, 3671, 3719, 3863, 2990, 2230, 1883, 1958, 2890, 2983, 497, 1939, 2023, 2416, 331, 2599, 3481, 3531, 
                   2440, 3539, 2948, 3247, 1845, 2024, 2502, 3488, 2721, 3718, 3673, 1880, 2991, 2926,   
                   2095, 3449, 3680, 3874, 2082, 3401, 2126, 2867],

                  [649, 920, 1023, 1360, 1752, 2116, 2365, 2435, 2636, 3140, 3306, 3383, 2665, 1175, 2315]]
    fileName = '8000'
    result_file = '8000-result3.0'
    all_true_file = chooseFileName(true_index, fileName, result_file)
    # print(all_true_file)


