import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import copy # 深度拷贝
from WindPy import *

def divide_to_segment_data(date_data, close_data, dea_data):
    """基于MACD之DEA指标的价格分段函数，输入三个列表依次为：日期，收盘价，DEA值，输出分段后的二个列表：日期，收盘价。"""
    segment_date_data=[]
    segment_close_data=[]
    date_extreme_point=[]
    close_extreme_point=[]
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

    # 尾段处理和波浪确认规则
    segment_date_data.append(date_data[i+1])
    segment_close_data.append(close_data[i+1])
    if start_point == 'd':
        segment_min = min(segment_close_data)
        i_temp = close_data.index(segment_min)
        # 默认设置为已确认
        confirm_flag = 0
        pre_close = close_extreme_point[-1]
        # 检测该结点是否为该分段上的最小值
        while close_data[i_temp] != pre_close:
            i_temp -= 1
            if close_data[i_temp] < segment_min:
            # 该结点不是该分段上的最小值，设置为未确认
                confirm_flag = 1
                break
        index = segment_close_data.index(segment_min)
        date_extreme_point.append(segment_date_data[index])
        close_extreme_point.append(segment_close_data[index])
        segment_date_data.clear()
        segment_close_data.clear()
        # 当前价大于前一个高点，则判断下跌行情结束，加入快速突破的高点
        if close_data[i+1] > close_extreme_point[-2]:
            date_extreme_point.append(date_data[i+1])
            close_extreme_point.append(close_data[i+1])
            print("当前为快速突破的高点，已确认，波浪数量：%d" % (len(date_extreme_point)-1))
        elif confirm_flag == 0:
            print("当前为低点，已确认，波浪数量：%d" % (len(date_extreme_point)-1))
        else:
            print("当前为低点，未确认，波浪数量：%d" % (len(date_extreme_point)-1))
    elif start_point == 'g':
        segment_max = max(segment_close_data)
        i_temp = close_data.index(segment_max)
        # 默认设置为已确认
        confirm_flag = 0
        pre_close = close_extreme_point[-1]
        # 检测该结点是否为该分段上的最大值
        while close_data[i_temp] != pre_close:
            i_temp -= 1
            if close_data[i_temp] > segment_max:
            # 该结点不是该分段上的最大值，设置为未确认
                confirm_flag = 1
                break
        index = segment_close_data.index(segment_max)
        date_extreme_point.append(segment_date_data[index])
        close_extreme_point.append(segment_close_data[index])
        segment_date_data.clear()
        segment_close_data.clear()
        # 当前价小于前一个低点，则判断上涨行情结束，加入快速突破的低点
        if close_data[i+1] < close_extreme_point[-2]:
            date_extreme_point.append(date_data[i+1])
            close_extreme_point.append(close_data[i+1])
            print("当前为快速突破的低点，已确认，波浪数量：%d" % (len(date_extreme_point)-1))
        elif confirm_flag == 0:
            print("当前为高点，已确认，波浪数量：%d" % (len(date_extreme_point)-1))
        else:
            print("当前为高点，未确认，波浪数量：%d" % (len(date_extreme_point)-1))

    return date_extreme_point, close_extreme_point

def combine_and_plot_segment(date1, price1, date2, price2):
    """合并画图，依次画出日线波浪和30分钟波浪。"""
    plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
    # plt.scatter(date1, price1, color='g')
    plt.plot(date1, price1, 'r-', linewidth=1.8, label="日线波浪")
    plt.plot(date2, price2, 'c-', linewidth=1.2, label="30分钟波浪")
    plt.legend()
    plt.title("上证指数", color='k', size=20)
    plt.xlabel("日   期", size=10)
    plt.ylabel("收盘价", size=10)
    plt.grid(True)
    plt.show()

def calculate_profit_rate(date_extreme_point, close_extreme_point):
    """计算每个分段的涨跌率，返回分段的涨跌幅度列表。"""
    profit_rate=[] # 涨跌幅度
    for k in range(0, len(date_extreme_point)):
        if k == 0:
            profit_temp = 0 # 第一段为0
            profit_rate.append(profit_temp)
        else:
            profit_temp = (close_extreme_point[k] - close_extreme_point[k-1])/close_extreme_point[k-1]
            profit_rate.append(profit_temp)
    return profit_rate

if __name__ == '__main__':
    # 连接Wind_Api，取出日期数据和分钟数据
    w.start()
    if w.isconnected():
        One_Day_Data = w.wsd("000001.SH", "close,MACD", "ED-3Y", "", "MACD_L=26;MACD_S=12;MACD_N=9;MACD_IO=2")
        Thirty_Minute_Data = w.wsi("000001.SH", "close,MACD", datetime.today()-timedelta(1100), "",
                                   "MACD_L=26;MACD_S=12;MACD_N=9;MACD_IO=2;BarSize=30")
    # 执行日期收盘价分段函数并导出数据
    writer = pd.ExcelWriter('MACD_daily_output.xlsx')
    One_Day_date, One_Day_price = divide_to_segment_data(One_Day_Data.Times, One_Day_Data.Data[0], One_Day_Data.Data[1])
    One_Day_rate = calculate_profit_rate(One_Day_date, One_Day_price)
    One_Day_Temp = {'date':One_Day_date, 'close_price':One_Day_price, 'pct_chg':One_Day_rate}
    One_Day_Frame = pd.DataFrame(One_Day_Temp)
    One_Day_Frame.to_excel(writer, sheet_name='日期分段', index=False, header=True)
    # 执行30分钟价格分段函数并导出数据
    Thirty_Minute_date, Thirty_Minute_price = divide_to_segment_data(Thirty_Minute_Data.Times, Thirty_Minute_Data.Data[0], Thirty_Minute_Data.Data[1])
    Thirty_Minute_rate = calculate_profit_rate(Thirty_Minute_date, Thirty_Minute_price)
    Thirty_Minute_Temp = {'date':Thirty_Minute_date, 'close_price':Thirty_Minute_price, 'pct_chg':Thirty_Minute_rate}
    Thirty_Minute_Frame = pd.DataFrame(Thirty_Minute_Temp)
    Thirty_Minute_Frame.to_excel(writer, sheet_name='30分钟分段', index=False, header=True)
    writer.save()
    # 画图
    combine_and_plot_segment(One_Day_date, One_Day_price, Thirty_Minute_date, Thirty_Minute_price)
