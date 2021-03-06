# 得到所有对比算法的召回率和精确率
import os

def getTrueIndex():
    true_index = [[71, 303, 58, 63, 48, 57, 23, 3, 543, 137, 300, 14, 598, 39, 534, 86, 62, 5, 67, 88, 104, 82, 503, 108, 472, 476],
                  [7, 2343, 2297, 91, 2244, 823, 86, 113, 2039, 77, 881, 1901, 69, 1852, 2398, 401, 1769, 1149, 100, 2466, 1478, 943, 2221, 2416, 2193, 279, 6, 902, 2, 216, 2796, 108, 1400, 3, 2161, 2190, 2063, 2029, 95, 270, 885, 87, 8, 274, 1880, 2110, 2211, 1501, 2191, 927, 2681, 2084, 777, 162, 1707, 449, 2376, 2365, 2169, 2177, 2250, 135, 2199, 2800, 371, 913, 228, 2050, 905, 133, 84, 101, 32, 2329, 1797, 935, 1476, 1868, 2411, 2337, 2934, 1706, 2707, 1806, 264, 1607, 2553, 1164, 2864, 356, 136, 1183, 1716, 168, 2154, 1064, 306, 2502, 261, 2636, 1065, 102, 326, 2972, 1719, 1560, 484, 346, 1992, 2259, 2417, 1709, 815, 751, 288, 1067, 606, 2664, 2673, 1594, 49, 2172, 1860, 1576, 1641, 722, 625, 1708, 1693, 1589, 1290, 2805, 2167, 3014, 2066, 2781, 148, 1010, 2043, 1788, 48, 1779, 360, 2518, 1207, 1077, 2687, 698, 361, 844, 3034, 2074, 175, 292, 1703, 248, 850, 2020, 236, 643, 2197, 2870, 214, 438, 800, 1101, 2141, 1753, 2811, 1910, 1752, 138, 1700, 62, 1755, 2421, 2932, 2779, 1729, 1814, 229, 1618, 1732, 263, 404, 2933, 3261, 1096],
                  [805, 1072, 4690, 7629, 3854, 7643, 4931, 978, 1233, 34, 471, 3145, 93, 1324, 402, 282, 7742, 7965, 4903, 6260, 5314, 5912, 524, 6995, 7, 1075, 279, 5443, 250, 6581, 280, 416, 405, 2840, 4981, 327, 254, 44, 522, 109, 331, 5851, 400, 6, 7699, 6300, 477, 22, 290, 468, 420, 1084, 7454, 5021, 180, 961, 6208, 1976, 350, 21, 3518, 4856, 4912, 478, 414, 401, 406, 4969, 411, 222, 481, 5948, 518, 320, 7375, 268, 1097, 7320, 2122, 384, 272, 5087, 4348, 111, 546, 656, 6256, 120, 413, 417, 18, 511, 178, 356, 8013, 191, 2775, 17, 7309, 495, 302, 315, 558, 7956, 6558, 106, 545, 5786, 6168, 318, 319, 507, 432, 274, 16, 4546, 7413, 7350, 6656, 7087, 8122, 6862, 7063, 7953, 6315, 7466, 6131, 7152, 4925, 7480, 7138, 6316, 7951, 7180, 236, 6631, 6696, 7578, 6094, 7664, 7298, 6003, 7989, 7743, 7353, 6826, 6387, 7935, 6953, 6530, 6898, 4923, 6843, 7397, 6699, 5905, 5972, 8136, 7433, 7589, 5864, 7708, 6780, 7394, 6453, 7402, 6002, 7732, 4922, 8140, 803, 6745, 5158, 7381, 6476, 6949, 7164, 7963, 6632, 7553, 6062, 7179, 7722, 7950, 6671, 8172, 7186, 4695, 6009, 6078, 7735, 6962, 6702, 2686, 7869, 6143, 6555, 7114, 8004, 7122, 6825, 6525, 6690, 5105, 7750, 7481, 7797, 5994, 3275, 7285, 6155, 6991, 5955, 6077, 5883, 7581, 6092, 6427, 7369, 3341, 5878, 7588, 6669, 7370, 6246, 6017, 6820, 6704, 5110, 6893, 8032, 3722, 6553, 4426, 7380, 4477, 5902, 6301, 5867, 5887, 7024, 3366, 6014, 4852, 7464, 6892, 4350, 6563, 7942, 6224, 3498, 8008, 6831, 7555, 7794, 6498, 7534, 7132, 5116, 6979, 4378, 415, 7308, 6332, 8007, 4920, 8086, 7200, 6430, 6897, 6326, 6633, 3565, 6968, 7046, 6411, 6735, 6910, 6602, 6852, 7029, 5145, 6976, 6970, 1085, 7088, 7970, 7296, 7795, 7624, 37, 7861, 7493, 6908, 4593, 8167, 7479, 7352, 7282, 7185, 8159, 7241, 7120, 7618, 4239, 4198, 7627, 6247, 6858, 6216, 7346, 6420, 7448, 6192, 6676, 6488, 7540, 7363, 7658, 7047, 6848, 6966, 4585, 7079, 6997, 2947, 2525, 1642, 3997, 5929, 6818, 5520, 5732, 3347, 1959, 3719, 2076, 6816, 4029, 3574, 8130, 6821, 3807, 3629],
                  ]
    
    return true_index



if __name__ == '__main__':
    base_path = 'processResult'
    result_base_path = 'recallandPrecise'
    listDir = os.listdir(base_path)
    print(listDir)
    true_index = getTrueIndex()
    for current_dir in listDir:
        print('current_dir:',current_dir)
        path = base_path + '/' + current_dir
        result_path = result_base_path + '/' + current_dir
        list_file = os.listdir(path)
        print(list_file)

        one_true_index = 0
        for one_file in list_file:
            print('one_file:',one_file)
            data = []
            true_num = 0
            true_true_num = 0
            true_data = true_index[one_true_index]
            one_true_index += 1
            with open(path + '/' + one_file, 'r') as f:
                for index,one_line in enumerate(f.readlines()):
                    # print(index)
                    # print(one_line)
                    one_line = one_line.strip('\n')
                    one_line = int(float(one_line))
                    if one_line == 1:
                        true_num += 1
                        if (index + 1) in true_data:
                            true_true_num += 1
            one_recall = true_true_num / len(true_data)
            one_precise = true_true_num / true_num
            print('one_recall:',one_recall)
            print('one_precise:',one_precise)
            file_name = one_file.split('.')[0]
            result = 'recall:' + str(one_recall) + ',  precise:' + str(one_precise)
            with open(result_path + '/' + file_name + '.txt', 'w') as f:
                f.write(result)
            
                    
                    
                    
                
        
    
    
    
