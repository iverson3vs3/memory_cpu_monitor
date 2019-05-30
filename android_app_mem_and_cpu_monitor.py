# -*- coding: utf-8 -*-
'''
Created on March 31 2016
Monitor Android app memory and cpu
@author iverson3vs3
'''

import os
import re
import matplotlib.pyplot as plt
import pylab as pl
import matplotlib.patches as mpatches
from time import sleep

#获取package进程当前占用的内存值,拿的是pss
def get_Memoryinfo(package):
    os.system('adb shell dumpsys meminfo ' + package + ' >./meminfo.txt')
    f1 = open('./meminfo.txt','r')
    meminfo = f1.read()
    mem = re.findall('TOTAL\s+(.*?)\s+\d+',meminfo,re.S)
    f1.close()
    mem1 = mem[0]
    float_mem = float(mem1)/1024
    return float_mem

#获取packge进程当前的cpu占有至
def get_CPUinfo(package):
    os.system('adb shell dumpsys cpuinfo |findstr ' + package + ' >./cpuinfo.txt')
    f2 = open('./cpuinfo.txt','r')
    cpuinfo = f2.read()
    cpu = re.findall('' + package + ': (.*?)% user',cpuinfo,re.S)
    f2.close()
    cpu1 = cpu[0]
    float_cpu = float(cpu1)
    return float_cpu

#绘制内存曲线
#package为被测应用的包名，如com.tencent.qq；endtime为打多少个点,如50；space为每个点之间的间隔，单位为秒，如5；
#color为曲线的颜色，b蓝色、g绿色、r红色、y黄色、k黑色、w白色
def draw_Memory_and_CPU_Line(package,endtime,space,color):
    time_axis_mem=[]
    memory_axis_mem=[]
    time_axis_cpu=[]
    cpu_axis_cpu=[]
    for times in range(0,endtime):
        memory = get_Memoryinfo(package)
        cpu = get_CPUinfo(package)
        sleep(space)
        time_axis_mem.append(times * space)
        memory_axis_mem.append(memory)
        time_axis_cpu.append(times * space)
        cpu_axis_cpu.append(cpu)

    x1 = time_axis_mem
    y1 = memory_axis_mem
    y_start_mem = min(y1) - 5
    y_end_mem = max(y1) + 5
    average_mem = round(sum(y1)/len(y1),2)
    max_mem = round(max(y1),2)

    x2 = time_axis_cpu
    y2 = cpu_axis_cpu
    y_start_cpu = min(y2) - 5
    y_end_cpu = max(y2) + 5
    average_cpu = round(sum(y2)/len(y2),2)
    max_cpu = round(max(y2),2)

    plt.figure(1)
    plt.figure(2)

    #绘制内存曲线
    plt.figure(1)
    pl.plot(x1,y1,color)
    pl.xlim(0,max(x1))
    pl.ylim(y_start_mem,y_end_mem)
    plt.title('Memory ' + '(' + package + ')')
    plt.xlabel('time (s)')
    plt.ylabel('memory (m)')
    red_patch1 = mpatches.Patch(color=color,label='average=' + str(average_mem) + 'm')
    red_patch2 = mpatches.Patch(color=color,label='max=' + str(max_mem) + 'm')
    pl.legend(handles=[red_patch1,red_patch2])

    #绘制cpu曲线
    plt.figure(2)
    pl.plot(x2,y2,color)
    pl.xlim(0,max(x2))
    pl.ylim(y_start_cpu,y_end_cpu)
    plt.title('CPU ' + '(' + package + ')')
    plt.xlabel('time (S)')
    plt.ylabel('cpu (%)')
    red_patch1 = mpatches.Patch(color=color,label='average=' + str(average_cpu) + '%')
    red_patch2 = mpatches.Patch(color=color,label='max=' + str(max_cpu) + '%')
    pl.legend(handles=[red_patch1,red_patch2])
    pl.show()

if __name__=='__main__':
    package,endtime,space,color = input('please enter the package、test time、time interval and line color(example:"com.tencent.qq",50,3,"r"):')
    draw_Memory_and_CPU_Line(package,endtime,space,color)
