import csv
import pandas
import pandas as pd

with open("data.csv", "w", newline="") as datacsv:
    # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
    csvwriter = csv.writer(datacsv, dialect=("excel"))
    # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
    #csvwriter.writerow(["B", "B", "C", "D"])
    #csvwriter.writerow(["A", "B", "C", "E"])

df=['A','B']
df=pd.DataFrame(df)
for i in range(2):
    df.to_csv('data.csv', mode='a',header=False,index=False)
df.to_excel('data.xlsx')