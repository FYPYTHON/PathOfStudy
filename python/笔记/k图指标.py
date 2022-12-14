# coding=utf-8
### 威廉指标(W&R)
W_R = (Hn-C)/(Hn-Ln) * 100
"""
# n  : 周期,  n=6, 12, 26
# Hn : 周期内最大值
# C  : 周期内最后一天的值
# Ln : 周期内最小值
W_R < 20 : 超卖， 买入线
W_R > 80 : 超买， 卖出线
W_R > 20 --> 50 : 买进
W_R < 80 --> 50 : 卖出
"""
### 能量潮指标(OBV)
"""
OBV =( (收盘价-最低价)-(最高价-收盘价) ) / (最高价-最低价) * V 

短期参考, 长期不宜
OBV下滑，股价上升: 考虑卖出
OBV上升, 股价下跌: 适当买入
OBV正转负: 卖出, 反之相反
OBV正负转换频率高: 择机二动
"""
### 相对强弱指标(RSI)
"""
RSI = N日内收盘涨幅的平均值 / (N日内收盘涨幅均值 + N日内收盘跌幅均值) * 100
RSI = 50: 分界点
RSI > 85 : 超买区
RSI < 15 : 超卖区

"""
### 乖离率指标(BIAS)
"""
BIAS= (当日股价 - 股价移动平均) / (股价移动平均) * 100
-15 < BIAS < 15
0 < BIAS < 15 : 适当卖出
-15 < BIAS < 0: 适当买入
"""
### 涨跌比率(ADR)
"""
ADR = n日内上涨数的移动合计 / n日内下跌数的移动合计
ADR下跌,股指下跌,继续下跌
ADR上涨,股指上涨,继续上涨
买点 0.5 < ADR < 1.5 卖点

"""

