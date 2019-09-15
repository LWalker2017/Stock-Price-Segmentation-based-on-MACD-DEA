import matplotlib.pyplot as plt
import datetime
import xlrd
from xlrd import open_workbook
from xlrd import xldate_as_tuple
import copy # 深度拷贝

# 从Excel导入数据并读入相应的数组中
wb = open_workbook('20160701-20190701-30min.xlsx')
date_data=[]   # 日期
close_data=[]  # 收盘价
dea_data=[]    # DEA指标
for s in wb.sheets():
    for row in range(s.nrows):
        values = []
        for col in range(s.ncols):
            values.append(s.cell(row,col).value)
            if s.cell(row,col).ctype == 3:
                #通过 xldate_as_tuple 方法，将读取的Excel值转换为tuple, 再通过datetime转换为转为时间类型
                date = xldate_as_tuple(s.cell(row,col).value,0)
                values[0] = datetime.datetime(*date)
        date_data.append(values[0])
        close_data.append(values[1])
        dea_data.append(values[2])

segment_date_data=[]
segment_close_data=[]
date_extreme_point=[]
close_extreme_point=[]
# pre_segment_date_data = []
# pre_segment_close_data = []
start_point = 0   # 起点无法判断高低点，设置为空
allow_pop = 0     # 不允许弹出点
for i in range(0, len(date_data)-1): # [0,601)
    # DEA指标小于0，则继续添加该分段
    if dea_data[i]<0 and (start_point=='d' or start_point==0):
        segment_date_data.append(date_data[i])
        segment_close_data.append(close_data[i])
    # DEA指标大于0，则继续添加该分段
    elif dea_data[i]>0 and (start_point=='g' or start_point==0):
        segment_date_data.append(date_data[i])
        segment_close_data.append(close_data[i])

    # DEA指标由负变正，则在该分段寻找价格最低点d
    if dea_data[i]<0 and dea_data[i+1]>0 and len(segment_close_data)>0 and (start_point=='d' or start_point==0):
        segment_min = min(segment_close_data)
        i_temp = close_data.index(segment_min)
        flag = 0
        # 不是起点
        if start_point != 0:
            pre_date = date_extreme_point.pop()
            pre_close = close_extreme_point.pop()
            # 检测该结点是否为该分段上的最小值
            while close_data[i_temp] != pre_close:
                i_temp -= 1
                if close_data[i_temp] < segment_min:
                # 该结点不是该分段上的最小值，标记为异常波段
                    flag = 1
                    break
        # 正常波段处理
        if flag == 0:
            # 不是起点
            if start_point != 0:
                date_extreme_point.append(pre_date)
                close_extreme_point.append(pre_close)
            index = segment_close_data.index(segment_min)
            date_extreme_point.append(segment_date_data[index])
            close_extreme_point.append(segment_close_data[index])
        # 存储当前的分段值，用于之后异常波段处理
            pre_segment_date_data = copy.deepcopy(segment_date_data)
            pre_segment_close_data = copy.deepcopy(segment_close_data)
            segment_date_data.clear()
            segment_close_data.clear()
            allow_pop = 1 # 之后允许弹出点
        else:
        # 异常波段处理
            # 不是起点且不允许弹出点
            if start_point != 0 and allow_pop != 1:
                date_extreme_point.append(pre_date)
                close_extreme_point.append(pre_close)
                index = pre_segment_close_data.index(min(pre_segment_close_data))
                date_extreme_point.append(pre_segment_date_data[index])
                close_extreme_point.append(pre_segment_close_data[index])
                segment_date_data.clear()
                segment_close_data.clear()
                allow_pop = 1 # 之后允许弹出点
            else:
                segment_date_data.clear()
                segment_close_data.clear()
                segment_date_data = copy.deepcopy(pre_segment_date_data)
                segment_close_data = copy.deepcopy(pre_segment_close_data)
                allow_pop = 0 # 之后不允许弹出点
        if len(date_extreme_point) == 0:
            start_point = 0
            allow_pop = 0 # 之后不允许弹出点
        else:
            start_point = 'g'
        continue
        # 调试专用
        # print(len(date_extreme_point))

    # DEA指标由正变负，则在该分段寻找价格最高点g
    if dea_data[i]>0 and dea_data[i+1]<0 and len(segment_close_data)>0 and (start_point=='g' or start_point==0):
        segment_max = max(segment_close_data)
        i_temp = close_data.index(segment_max)
        flag = 0
        # 不是起点
        if start_point != 0:
            pre_date = date_extreme_point.pop()
            pre_close = close_extreme_point.pop()
            # 检测该结点是否为该分段上的最大值
            while close_data[i_temp] != pre_close:
                i_temp -= 1
                if close_data[i_temp] > segment_max:
                # 该结点不是该分段上的最大值，标记为异常波段
                    flag = 1
                    break
        # 正常波段处理
        if flag == 0:
            # 不是起点
            if start_point != 0:
                date_extreme_point.append(pre_date)
                close_extreme_point.append(pre_close)
            index = segment_close_data.index(segment_max)
            date_extreme_point.append(segment_date_data[index])
            close_extreme_point.append(segment_close_data[index])
        # 存储当前的分段值，用于之后异常波段处理
            pre_segment_date_data = copy.deepcopy(segment_date_data)
            pre_segment_close_data = copy.deepcopy(segment_close_data)
            segment_date_data.clear()
            segment_close_data.clear()
            allow_pop = 1 # 之后允许弹出点
        else:
        # 异常波段处理
            # 不是起点且不允许弹出点
            if start_point != 0 and allow_pop != 1:
                date_extreme_point.append(pre_date)
                close_extreme_point.append(pre_close)
                index = pre_segment_close_data.index(max(pre_segment_close_data))
                date_extreme_point.append(pre_segment_date_data[index])
                close_extreme_point.append(pre_segment_close_data[index])
                segment_date_data.clear()
                segment_close_data.clear()
                allow_pop = 1 # 之后允许弹出点
            else:
                segment_date_data.clear()
                segment_close_data.clear()
                segment_date_data = copy.deepcopy(pre_segment_date_data)
                segment_close_data = copy.deepcopy(pre_segment_close_data)
                allow_pop = 0 # 之后不允许弹出点
        if len(date_extreme_point) == 0:
            start_point = 0
            allow_pop = 0 # 之后不允许弹出点
        else:
            start_point = 'd'
        # 调试专用
        # print(len(date_extreme_point))

# 尾段处理
segment_date_data.append(date_data[i+1])
segment_close_data.append(close_data[i+1])
if start_point == 'd':
    index = segment_close_data.index(min(segment_close_data))
    date_extreme_point.append(segment_date_data[index])
    close_extreme_point.append(segment_close_data[index])
    segment_date_data.clear()
    segment_close_data.clear()
    # 当前价大于前一个高点，则判断下跌行情结束
    if close_data[i+1] > close_extreme_point[-2]:
        date_extreme_point.append(date_data[i+1])
        close_extreme_point.append(close_data[i+1])
        print("当前为高点，波浪数量：%d" % (len(date_extreme_point)-1))
    else:
        print("当前为低点，波浪数量：%d" % (len(date_extreme_point)-1))
elif start_point == 'g':
    index = segment_close_data.index(max(segment_close_data))
    date_extreme_point.append(segment_date_data[index])
    close_extreme_point.append(segment_close_data[index])
    segment_date_data.clear()
    segment_close_data.clear()
    # 当前价小于前一个低点，则判断上涨行情结束
    if close_data[i+1] < close_extreme_point[-2]:
        date_extreme_point.append(date_data[i+1])
        close_extreme_point.append(close_data[i+1])
        print("当前为低点，波浪数量：%d" % (len(date_extreme_point)-1))
    else:
        print("当前为高点，波浪数量：%d" % (len(date_extreme_point)-1))

# 画图
plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False   # 用来正常显示负号

plt.subplot(3,1,1)
plt.title("上证指数", color='k', size=20)
plt.plot(date_data, dea_data, 'y-', label="DEA")
plt.legend()
plt.ylabel("DEA值", size=12)
plt.grid(True)
plt.xticks([]) # 设置x轴的刻度线为空

plt.subplot(3,1,2)
plt.plot(date_data, close_data, 'c-', linewidth=1.5, label="股价")
plt.scatter(date_extreme_point, close_extreme_point, color='r', s=15, label="分段点")
plt.legend()
plt.ylabel("30分钟收盘价", size=12)
plt.grid(True)
plt.xticks([]) # 设置x轴的刻度线为空

plt.subplot(3,1,3)
plt.plot(date_extreme_point, close_extreme_point, 'k-', linewidth=1.0, label="波浪")
plt.legend()
plt.xlabel("日   期", size=12)
plt.ylabel("30分钟收盘价", size=12)
plt.grid(True)
plt.show()

# 输出数据
profit_rate=[] # 涨跌幅度
for k in range(0, len(date_extreme_point)):
    if k == 0:
        profit_temp = (close_extreme_point[k] - close_data[0])/close_data[0]
        profit_rate.append(profit_temp)
    else:
        profit_temp = (close_extreme_point[k] - close_extreme_point[k-1])/close_extreme_point[k-1]
        profit_rate.append(profit_temp)
    print(date_extreme_point[k], close_extreme_point[k], profit_rate[k])
