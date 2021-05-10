# coding:utf-8 
"""
author:Sam
date：2021/4/19
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# 追涨杀跌类策略
class Strategy():
    def __init__(self,index, threshold, tradecost):
        """
        :param index: 指数收盘价以及涨跌幅
        :param threshold: 设定追涨杀跌的阈值
        :param tradecost: 总交易成本
        :param _low: 最近一次卖出后出现的最低点
        :param _high: 最近一次买入后出现的最高点
        """
        self.index = index
        self.threshold = threshold
        self.tradecost = tradecost
        self._low = index.iloc[0]['close_price']
        self._high = index.iloc[0]['close_price']    # 先假定第一个数据同时为最高点和最低点
        self._netvalue = 1                           # 最初净值设定：1
        self._status = 0                             # 最初状态：不持有指数
        self._last_trade_date = self.index.index[0].strftime("%Y-%m-%d")
                                                     # 上一次交易日期（变动状态）
        self._netvalue_dict = {}                     # 净值数据字典 用于绘制净值曲线
        self._daily_return = 0                       # 策略当天收益率

    def signal(self, date):   # 设定每日交易信号：上涨幅度超过阈值，买入指数；下跌幅度超过阈值，卖出指数
        """
        :param date: 交易日
        :return: 是否交易/持有状态
        """
        initial_status = self._status  # 初始状态
        status = self._status          # 待确认状态

        if self._status == 0 and ((self.index.loc[date]['close_price'] - self._low)/self._low > self.threshold) :
            status = 1
        if self._status == 1 and ((self.index.loc[date]['close_price'] - self._high) / self._high < -self.threshold):
            status = 0


        # 判断当前日期是否为最高点或最低点，并作出调整
        if self.index.loc[date]['close_price'] <= self.index.loc[self._last_trade_date:date]['close_price'].min():
            self._low = self.index.loc[date]['close_price']

        if self.index.loc[date]['close_price'] >= self.index.loc[self._last_trade_date:date]['close_price'].max():
            self._high = self.index.loc[date]['close_price']


        # 交易产生，最后一次交易日期
        if initial_status != status:
            self._last_trade_date = date

        return status


    def plot_netvalue(self):    # 计算、绘制净值曲线
        count = 0  # 计数器
        return_list = [0]
        self._netvalue_dict[self.index.index[0].strftime("%Y-%m-%d")] = 1
        for date in self.index.iloc[1:].index:
            pre_date = self.index.index[count]
            date = date.strftime("%Y-%m-%d")
            pre_date = pre_date.strftime("%Y-%m-%d")
            self._status = self.signal(pre_date)  # 用前一天交易状态进行判断
            if self._last_trade_date == pre_date:
                self._daily_return = self._status * (self.index.loc[date]['pct_change'] / 100 - self.tradecost)
                self._netvalue = self._netvalue * (1 + (self._daily_return))
            else:
                self._daily_return = self._status * (self.index.loc[date]['pct_change']/100)
                self._netvalue = self._netvalue * (1 +(self._daily_return))

            return_list.append(self._daily_return)
            self._netvalue_dict[date] = self._netvalue
            count = count + 1

        net_value_df = pd.DataFrame(data=self._netvalue_dict.values(),index=self._netvalue_dict.keys(),
                                    columns=['net_value'])
        net_value_df['daily_return'] = return_list

        print(net_value_df)
        net_value_df.to_csv("追涨杀跌策略净值曲线.csv")

        index_net_value_df = self.index[['net_value']]
        print(index_net_value_df)


        plt.plot(index_net_value_df.index, net_value_df['net_value'],label='strategy netvalue')
        plt.plot(index_net_value_df.index, index_net_value_df['net_value'],label = 'index netvalue')

        plt.legend()
        plt.title("netvalue curve")
        plt.xlabel("date")
        plt.ylabel("netvalue")
        plt.show()



if __name__ == '__main__':
    # 读取指数收盘价数据
    """
    回测：主动股基930890.CSI 2008/01/02 至 2021/04/19
    传入/修改三个变量：
        1. 指数时间序列（收盘价、涨跌幅）
        2. 追涨杀跌阈值
        3. 总交易成本
    """
    # 指数时间序列 （收盘价、涨跌幅）
    index = pd.read_excel('指数.xlsx')
    index.index = pd.to_datetime(index['date'])
    index = index.drop(['date'],axis=1)
    index = index.loc[:]
    print(index)

    index_netvalue_list = [1]

    for count in range(1,len(index.index)):
        index_netvalue_list.append(index_netvalue_list[count-1] * (1+index.iloc[count-1]['pct_change']/100))

    index['net_value'] = index_netvalue_list

    print(index)



    # 追涨杀跌阈值、总交易成本
    threshold = 0.3
    cost = 0.007

    strategy =Strategy(index, threshold, cost)
    strategy.plot_netvalue()




