import numpy as np

# simpDat = [['a','b'],['b','c','d'],['a','c','d','e'],
#              ['a','d','e'],['a','b','c'],['a','b','c','d'],['b','c'],['a','b','c'],
#              ['a','b','d'],['b','c','e']]

# d = []
# dlist = []
# # 找出全部的项
# for i in range(len(simpDat)):
#     d.extend(simpDat[i])
# dlist=list(set(d))
# print(dlist)

# #计算1项集的支持度计数
# s={}
# support=0
# for i in range(len(dlist)):
#     for one_data in simpDat:
#         if len({dlist[i]} & set(one_data)) > 0:
#             support += 1
#     if support >2:
#         s[str(dlist[i])]=support
#         # print(s)
#         support=0
# print(s)


if __name__ == '__main__':

    # 对数据排序
    all_data = [['a','b'],
                ['b','c','d'],
                ['a','c','d','e'],
                ['a','d','e'],
                ['a','b','c'],
                ['a','b','c','d'],
                ['b','c'],
                ['a','b','c'],
                ['a','b','d'],
                ['b','c','e']]
    a = {'a':3, 'b':1, 'c':4, 'd':5}
    for one_data in all_data:
        one_data = one_data & a.keys()
        print(sorted(one_data, key = lambda x:a[x], reverse = True))

    # 重复的代码
    a = '2+3'
    print(eval(a))





# sort_all_data = []
# for one_data in all_data:
    




# t=0
# for i in range(len(a)-1):
#     if a[i]>a[i+1]:
#         t=a[i]
#         s=b[i]
#         a[i]=a[i+1]
#         b[i]=b[i+1]
#         a[i+1]=t
#         b[i+1]=s
# print(a)
# print(b)
# paixv={}
# for i in range(len(a)):
#     paixv[b[i]]=a[i]
# print(paixv)