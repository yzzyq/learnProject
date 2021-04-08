# 将txt里面的文件名写入到excel中
import openpyxl

# 从txt中读取全部的文件名
all_file_name = []
result_path = 'D:/论文/论文修改/数据整理/617-0-10.txt' 
with open(result_path, 'r', encoding = 'utf-8') as f:
    for line in f.readlines():
        file_name = line.strip('\n')
        print(file_name)
        all_file_name.append(file_name)
print(len(all_file_name))

excel_name = 'D:/论文/论文修改/数据整理/617-0-10-all-rsult-1.xlsx'
work_book = openpyxl.load_workbook(excel_name)
sheets_name = work_book.get_sheet_names()
first_table = work_book.get_sheet_by_name(sheets_name[0])
for file_index,file_name in enumerate(all_file_name):
    first_table.cell(row = file_index + 2, column = 2).value = file_name 
# os.remove(excel_name)
work_book.save('D:/论文/论文修改/数据整理/617-0-10-all-rsult-2.xlsx')   

# sheet1.write(0,0,'数量比阈值')
# sheet1.write(0,1,'总和阈值')
# sheet1.write(0,2,'召回率')
# sheet1.write(0,3,'精确率')
# for threshold_amount in range(len(all_criteria)):
#     for col in range(4):
#         sheet1.write(threshold_amount+1,col,str(all_criteria[threshold_amount][col]))
# book.save(result_fileName+'/all-result.xls')


