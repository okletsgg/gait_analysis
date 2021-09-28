import numpy as np
import matplotlib.pyplot as plt

def datafit(t3,left,right):
    t32=[0 for i in range(right-left+1)]
    x=[]
    #y=[0 for i in range(right-left)]
    y=[]
    z=[]
    mm=1
    #print('     right-left+1=',right-left+1)
    t32[0]=right-left
    for i in range(right-left):
        t32[mm] = t3[i + left]
        mm += 1
        #print(i, i + left, mm - 1, t32[mm - 1])
        if (t3[i+left]!=0):
            #print(i,i+left,mm-1, t32[mm-1])
            y.append(t3[i+left])
            x.append(i)
        else:
            z.append(i)
    z=np.array(z)
    #print(x)
    x=np.array(x)
    #print("         非缺省值序号字典规模=",x.shape)
    y=np.array(y)
    if(x.shape[0]==0):
        return t3
    #print("非缺省值序号字典=",x)
    f1=np.polyfit(x,y,25)
    p1=np.poly1d(f1)
    yvals=p1(x)
    for i in range(right-left):
        if (t32[i]==0):
            #print("i=",i,"t32[i]=",t32[i])
            t32[i]=p1[i]
            #print(t32[i])
    queshi=p1(z)
    #print("             queshi=",queshi)
    plot1 = plt.plot(x,y,'s',label='original values')
    plot2 = plt.plot(x,yvals,'r',label='polyfit values')
    #plt.show()
    return t32