import pandas as pd
import numpy as np
import math
import os
import ezc3d

def bob_loading_csv(path):
    with open(path) as temp_f:
        # get No of columns in each line
        col_count = [len(l.split(",")) for l in temp_f.readlines()]

    column_names = [i for i in range(max(col_count))]
    data = pd.read_csv(path, skip_blank_lines=True,header=None, names=column_names)
    data = np.array(data)

    print(path, "载入完成")
    return data

def bob_time(end,frequency):
    return end/frequency

def bob_toe_off_time(dataarray,dataend):
    maxinum=-99999
    maxinum_order=-1
    # print(dataend)
    # print("start:",dataarray[47,0],"end:",dataarray[47,dataend])
    for i in range(dataend):
        if(dataarray[41,i]>maxinum):
            maxinum_order=i
            maxinum=dataarray[41,i]
    for i in range(maxinum_order-1,0,-1):
        #print(i)
        if(dataarray[47,i]<dataarray[47,i+1]) & (dataarray[47,i]<dataarray[47,i-1]): #47是RTOE的z坐标轨迹
            # print(dataarray[47,i-1],dataarray[47,i],dataarray[47,i+1])
            return i


# def bob_Single_step_time(dataarray,end,frequency):
#     #print(dataarray[47:])
#     #第13条轨迹为LHEE，选择其z坐标最小值作为右脚开始迈步的时刻
#     bob_minimum=99999
#     bob_minimum_order=-1
#     for i in range(end):
#         if(bob_minimum>dataarray[38,i]):   #38是LHEE的z坐标轨迹索引
#             bob_minimum=dataarray[38,i]
#             bob_minimum_order=i
#     #print("bob_minimum_order=",bob_minimum_order)
#     return (end-bob_minimum_order)/frequency

def bob_single_step_time(toe_off_time,end,frequency):
    return (end-toe_off_time)/frequency

def bob_step_time(dataarray,end,frequency):
    return (end)/frequency

def bob_velocity(dataarray,end,time):
    #print(dataarray[40,end-1])     #40是RHEE的y坐标轨迹索引
    return abs(dataarray[40,end-1]-dataarray[40,0])/1000/time

def bob_cadence(time):
    return 60/time

# def bob_ipsilateral_standing_phase(dataarray,end):
#     bob_minimum = 99999
#     bob_minimum_order = -1
#     for i in range(end):
#         if (bob_minimum > dataarray[38, i]):
#             bob_minimum = dataarray[38, i]
#             bob_minimum_order = i
#     return bob_minimum_order/end

def bob_ipsilateral_standing_phase(toe_off_time,end):
    return toe_off_time/end

# def bob_step_length(dataarray,end):
#     # print(dataarray[47:])
#     # 第13条轨迹为LHEE，选择其z坐标最小值作为右脚开始迈步的时刻
#     bob_minimum = 99999
#     bob_minimum_order = -1
#     for i in range(end):
#         if (bob_minimum > dataarray[38, i]):    #38是LHEE的z坐标轨迹索引
#             bob_minimum = dataarray[38, i]
#             bob_minimum_order = i
#     nums=[[0] for i in range(bob_minimum_order)]
#     for i in range(bob_minimum_order):
#         nums[i]=dataarray[41,i]                 #41是RHEE的z坐标轨迹索引
#     nums=np.percentile(nums,(25,50,75),interpolation='midpoint')
#     #print(nums)
#     for i in range(bob_minimum_order):
#         if(dataarray[41,i]-nums[1]>5):
#             median=i
#             #print("median=",median)
#             break
#     # print(bob_minimum_order,dataarray[40,bob_minimum_order])
#     # print(dataarray[40,0])
#     # print(dataarray[40,end-1])
#     return abs(dataarray[40,end-1]-dataarray[40,bob_minimum_order])/1000   #40是RHEE的y坐标轨迹索引

def bob_step_length(dataarray,toe_off_time,end):
    return abs(dataarray[40,end]-dataarray[40,toe_off_time])/1000

def bob_stride_length(dataarray,end):
    return abs(dataarray[37,0]-dataarray[40,end])/1000   #37是LHEE的y坐标轨迹索引

def bob_right_ankle_angle(dataarray,bob1_time):
    a = [[0] for i in range(3)]
    b = [[0] for i in range(3)]
    for i in range(3):
        a[i] = dataarray[33 + i, bob1_time] - dataarray[27 + i, bob1_time]  # 35是RANK的z坐标轨迹索引;  29是RTIB的z坐标轨迹索引
        b[i] = dataarray[33 + i, bob1_time] - dataarray[45 + i, bob1_time]
    a_norm = np.linalg.norm(a, ord=2)  # linalg是线性代数包，norm是求范数函数，默认求第二范数，ord=i参数决定求i范数
    b_norm = np.linalg.norm(b, ord=2)
    inner_product = np.dot(a, b)
    return math.degrees(math.acos(inner_product / (a_norm * b_norm)))

def bob_right_knee_angle(dataarray,bob1_time):
    a = [[0] for i in range(3)]
    b = [[0] for i in range(3)]
    for i in range(3):
        # print(i)
        # print(dataarray[21 + i, bob1_time], dataarray[27 + i, bob1_time])
        # print(dataarray[21 + i, bob1_time], dataarray[15 + i, bob1_time])
        a[i] = dataarray[21 + i, bob1_time] - dataarray[27 + i, bob1_time]  # 23是RKNE的z坐标轨迹索引;  29是RTIB的z坐标轨迹索引
        b[i] = dataarray[21 + i, bob1_time] - dataarray[15 + i, bob1_time]  # 17是RTHI的z坐标轨迹索引
    a_norm = np.linalg.norm(a, ord=2)  # linalg是线性代数包，norm是求范数函数，默认求第二范数，ord=i参数决定求i范数
    b_norm = np.linalg.norm(b, ord=2)
    #print(a,b,a_norm,b_norm)
    inner_product = np.dot(a, b)
    return math.degrees(math.acos(inner_product / (a_norm * b_norm)))

def bob_right_toe_out_angle(dataarray,end):
    a=[[0] for i in range(3)]
    b=[[0] for i in range(3)]
    for i in range(3):
        a[i]=dataarray[39+i,0]
        b[i]=dataarray[45+i,0]
    #print("a=",a,"b=",b)
    a_norm=np.linalg.norm(a,ord=2)   #linalg是线性代数包，norm是求范数函数，默认求第二范数，ord=i参数决定求i范数
    b_norm=np.linalg.norm(b,ord=2)
    inner_product=np.dot(a,b)
    #print(a_norm,b_norm,inner_product)
    return math.degrees(math.acos(inner_product/(a_norm*b_norm)))

def bob_right_hip_angle(dataarray,bob1_start,bob1_end):
    a=[[0] for i in range(3)]
    b=[[0] for i in range(3)]
    for i in range(3):
        a[i]=dataarray[21+i,bob1_start]-dataarray[15+i,bob1_start]
        b[i]=dataarray[21+i,bob1_end]-dataarray[15+i,bob1_end]
    a_norm=np.linalg.norm(a,ord=2)
    b_norm=np.linalg.norm(b,ord=2)
    print(a, b)
    inner_product=np.dot(a,b)
    return math.degrees(math.acos(inner_product/(a_norm*b_norm)))

def bob_plantar_flexion(dataarray,toe_off_time):
    a = [[0] for i in range(3)]
    b = [[0] for i in range(3)]
    for i in range(3):
        a[i] = dataarray[33 + i, toe_off_time]-dataarray[27+i,toe_off_time] #35是RANK的z坐标轨迹索引;  29是RTIB的z坐标轨迹索引
        b[i] = dataarray[33 + i, toe_off_time]-dataarray[45+i,toe_off_time]
    a_norm = np.linalg.norm(a, ord=2)  # linalg是线性代数包，norm是求范数函数，默认求第二范数，ord=i参数决定求i范数
    b_norm = np.linalg.norm(b, ord=2)
    inner_product = np.dot(a, b)
    return math.degrees(math.acos(inner_product / (a_norm * b_norm)))-90

if __name__=='__main__':
    path="E:\PythonProjects\pythonproject1\gait_analysis\data\dzm\dzmCal 03.csv"
    data=bob_loading_csv(path)
    print(data.shape)
    k = int(data.shape[0] / 48)
    frequency = 200
    for i in range(k):
        start=0+48*i
        end=48+48*i
        print("第%d个步态周期："%(i+1))
        data_single=data[start:end]
        data_single_end=data_single.shape[1]-1 #这里shape[1]是数据矩阵的列长，对应矩阵纵坐标的最大值+1
        for i in range(data_single.shape[1]):   #这里因为之前c3dproduct2.py里已经对所有缺失值进行了补偿，即使不同轨迹
                                                #尾部因缺失值导致长度不同，也会被补偿到和RHEE一样长，因此此时每条轨迹等长，
                                                #不必每条都检查长度是否和data.shape[1]一致。
            if (math.isnan(data_single[0,i])):
                #print("data_single_end=",i)
                data_single_end=i-1
                break
        print(data_single_end, data_single[47, data_single_end])
        print("数据规模：",data_single.shape,"    ","帧率：",frequency)
        print("单步态周期帧数：",data_single_end+1)
        time=bob_time(data_single_end,frequency)
        right_toe_off_time=bob_toe_off_time(data_single,data_single_end)
        print("右脚脚趾离地时刻：",right_toe_off_time)
        print("单步时间：",bob_single_step_time(right_toe_off_time,data_single_end,frequency),"s") #单步时间
        print("跨步时间：",bob_step_time(data_single,data_single_end,frequency),"s") #跨步时间
        print("步速：",bob_velocity(data_single,data_single_end,time),"m/s")
        print("步频：",bob_cadence(time),"steps/min")
        print("同侧站立相时间百分比:",bob_ipsilateral_standing_phase(right_toe_off_time,data_single_end)*100,"%")
        print("步长：",bob_step_length(data_single,right_toe_off_time,data_single_end),"m")
        print("跨步长：",bob_stride_length(data_single,data_single_end),"m")
        print("足夹角：",bob_right_toe_out_angle(data_single,data_single_end),"°")
        print("跖屈：",bob_plantar_flexion(data_single,right_toe_off_time),"°")
        print("站立相足跟着地时的踝关节角度：",bob_right_ankle_angle(data_single,data_single_end),"°")
        print("站立相脚趾离地时的踝关节角度：", bob_right_ankle_angle(data_single, right_toe_off_time), "°")
        print("站立相支撑中期的踝关节角度：",bob_right_ankle_angle(data_single,int(right_toe_off_time/2)), "°")
        print("站立相足跟着地时的膝关节角度：",bob_right_knee_angle(data_single,1), "°")
        print("站立相脚趾离地时的膝关节角度：",bob_right_knee_angle(data_single,right_toe_off_time), "°")
        print("站立相支撑中期的膝关节角度",bob_right_knee_angle(data_single,int(right_toe_off_time/2)), "°")
        print("摆动相髋关节角度变化：",bob_right_hip_angle(data_single,right_toe_off_time,data_single_end),"°")


        

