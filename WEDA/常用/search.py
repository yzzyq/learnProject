import xlrd


if __name__ == '__main__':
    file_name = 'C:/Users/spiderJ/Desktop/Halphas-threshold - v3/result5.0-v4.0/data-0-10/0.06-threshold.xls'
    data = xlrd.open_workbook(file_name)
    table = data.sheets()[0]
    col_name = table.row_values(0)
    list_value = []
    nrows = table.nrows
    for row_num in range(1,nrows):
        row = table.row_values(row_num)
        if row[1] != '':
            list_value.append(float(row[1]))
    #print(list_value)
    true_index = [[8,79,104,122,126,262,358,362,373,451,531,612,649,682,686,692,697,698,701,702,706,712,721,728,757,762,767,769,771,798,803,805,806,809,811,812,816,817,819,821,825,826,838,844,845,846,847,848,849,850,851,852,853,854,858,859,860,861,866,867,869,870,871,874,888,911,913,914,923,931,972,1016,1020,1062,1063,1065,1071,1078,1109,1292,1323,1449,1453,1554,1556,1821,1852,1892,1916,1918,1920,1924,1962,2021,2048,2088,2160,2166,2167,2170,2173,2194,2199,2236,2264,2270,2271,2273,2297,2298,2299,2305,2306,2308,2309,2316,2378,2380,2381,2424,2445,2447,2459,2470,2474,2476,2480,2481,2489,2500,2571,2583,2587,2620,2628,2629,2630,2682,2686,2734,2781,2803,2868,3120,3302,3311,3435,3521,4144,4251,4922],
              [622,648,845,860,1205,1260,1453,1500,1579,1638,1663,1727,1831,1870,1893,1943,1971,2068,2072,2077,2126,2167,2169,2221,2226,2288,2312,2669,2880,3317,3465,3502,3538,3546,3547,3566,3611,3613,3853,4223,4364,4471,4781,4787,4788,4802,4853,4863],
              [74,81,180,225,309,432,439,589,771,889,951,1438,1715,1957,2253,2932,3114,3193,3373,3478,3897,4154,4344,4389,4552,4860,4864,4876]]
    data = true_index[0]
    for index in data:
        if index not in list_value:
            print(index)
