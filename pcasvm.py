import numpy as np
import pandas as pd
import os
import math
from sklearn.decomposition import PCA
from sklearn import decomposition
from sklearn import svm

path=r"E:\PythonProjects\pythonproject1\gait_analysis\data"
filename='data001.csv'
with open(path+'\\'+filename) as temp_f:
    # get No of columns in each line
    col_count = [len(l.split(",")) for l in temp_f.readlines()]

column_names = [i for i in range(max(col_count))]
data = pd.read_csv(path+'\\'+filename, skip_blank_lines=True,header=None, names=column_names)
data=np.array(data)
print("病态步态数据规模：",data.shape)

filename='data002.csv'
with open(path+'\\'+filename) as temp_f:
    # get No of columns in each line
    col_count = [len(l.split(",")) for l in temp_f.readlines()]

column_names = [i for i in range(max(col_count))]
data2 = pd.read_csv(path+'\\'+filename, skip_blank_lines=True,header=None, names=column_names)
data2=np.array(data2)
print("正常步态数据规模：",data2.shape)

x=[[0]*(data.shape[1]) for i in range(data.shape[0]+data2.shape[0])]
x=np.array(x)
print("训练集数据规模：",x.shape)
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        x[i,j]=data[i,j]
#print("此时i为",i)
for i in range(data2.shape[0]):
    for j in range(data.shape[1]):
        x[data.shape[0]+i,j]=data2[i,j]
#print("此时i为",data.shape[0]+i)
# y=[[0] for i in range(data.shape[0]+data2.shape[0])]
# y=np.array(y)
y=[]
for i in range(data.shape[0]):
    y.append(0)
for i in range(data2.shape[0]):
    y.append(1)
y=np.array(y)
print("标签数组规模：",y.shape)
pca=decomposition.PCA(n_components=50)
pca.fit(x)
z=pca.transform(x)
print("PCA后训练集规模：",z.shape)
#z=x
model = svm.SVC(C=10, kernel='linear')
model.fit(z, y)
k=np.empty([1,5760])
k=pca.transform(k)
#print(k.shape)

filename='data003.csv'
with open(path+'\\'+filename) as temp_f:
    # get No of columns in each line
    col_count = [len(l.split(",")) for l in temp_f.readlines()]

column_names = [i for i in range(max(col_count))]
data = pd.read_csv(path+'\\'+filename, skip_blank_lines=True,header=None, names=column_names)
data=np.array(data)
print("测试集数据规模：",data.shape)
k=[[0]*(data.shape[1]) for i in range(data.shape[0])]
k=np.array(k)
#print("测试集标签数据规模",k.shape)
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        k[i,j]=data[i,j]
k2=pca.transform(k)
print("PCA后测试集数据规模",k2.shape)
print("测试集分类结果：",model.predict(k2))

#print(x.shape)
#print(k.shape)
model2 = svm.SVC(C=20, kernel='linear')
model2.fit(x, y)
print("测试集分类结果：",model2.predict(k))
print("准确率=",37/39)