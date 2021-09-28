import numpy as np
import pandas as pd
import os
import math

def bob_loading_csv(path):
    #print(path)
    with open(path) as temp_f:
        # get No of columns in each line
        col_count = [len(l.split(",")) for l in temp_f.readlines()]

    column_names = [i for i in range(max(col_count))]
    data = pd.read_csv(path, skip_blank_lines=True,
                       header=None, names=column_names)

    # data=pd.read_csv(path,header=None,error_bad_lines=False)   #header=None 就不会把第一列作为列名
    #print("type(data)=", type(data))
    #print("data.shape=", data.shape)

    # print(data['2'])
    data = np.array(data)
    '''print('data[0,1]=',data[0,1])
    print(data[1, 1])
    print(data[2, 1])
    print(data.shape)'''
    k = int(data.shape[0] / 48)
    # print("type(k)=",type(k))
    # xyz = [[0] * 120 for i in range(k)]

    for i in range(k):
        xyz = []
        for i2 in range(48):
            for j in range(120):
                if (data.shape[1] <= j):
                    # print("i=",i,"j=",j)
                    # print(data.iloc[i,j])
                    # print(data[i,j])
                    # xyz.append(data.iloc[i:i+1,j:j+1])
                    # xyz.append(data.iloc[i,j])
                    xyz.append(0)
                else:
                    t = i * 48 + i2
                    # print('t=',t,type(t))
                    # print('type(data[t,j])',type(data[t,j]))
                    # print(t,j,data[t,j])
                    # m=int(data[t,j])
                    # print(m)
                    if (math.isnan(data[t, j])):
                        xyz.append(0)
                    else:
                        xyz.append(data[i * 48 + i2, j])
        xyz = np.array(xyz)
        #print("xyz.shape=", xyz.shape)
        dataframe = pd.DataFrame(xyz, index=None)
        dataframe = pd.DataFrame(dataframe.values.T, index=dataframe.columns, columns=dataframe.index)
        dataframe.to_csv(path2, mode='a', header=False, index=False)
    print(path, "载入完成")
    return k

    # for i in range(data.shape[0]):
    #     for j in range(120):
    #         if(data.shape[1]<j):
    #             #print("i=",i,"j=",j)
    #             #print(data.iloc[i,j])
    #             #print(data[i,j])
    #             #xyz.append(data.iloc[i:i+1,j:j+1])
    #             #xyz.append(data.iloc[i,j])
    #             xyz.append(0)
    #         else:
    #             xyz.append(data[i,j])


if __name__ == '__main__':
    path = r"E:\PythonProjects\pythonproject1\gait_analysis\data\dzm\dzmCal 07.csv"
    path2 = r"data.csv"
    filename = pd.read_csv('path3.txt', header=None)
    filename = np.array(filename)
    # bob_loading_csv(path)
    # print(filename.shape)
    num=0
    for i in range(filename.shape[0]):
        # print(filename[i,0])
        num+=bob_loading_csv(filename[i, 0])
    print("数据总数=",num)
    # bob_loading_csv(path)
