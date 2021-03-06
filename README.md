# Assignment2
## 1.Abstract
Strategy effective testing: "Buy high sell low"

In this project, we're going to test the performance of a specific strategy which is commonly appeared in financial exchange market. That is, **when the price of an underlying goes up beyond a certain percentage, retail investor is positive about the future trend and thus buy the underlying. Oppositely, he would sell it to control the risk exposure.**

The goal of this project, to be more clearly, is to demonstrate that **we should hold the fund asset for a long period rather than frequently adjusting our position.** We will show the result by a long-term strategy backtest and visualize strategy netvalue variation. In this way, the conclusion would be clear for common retail investors.


## 2.Basic setting
index: 主动股基 930890.CSI

backtest period: 2016/01/02 to 2021/04/19

threshold: 30%

total transaction fee: 0.7%

initial status: short position

## 3.code explaination
We create our strategy class and define two simply function besides the init one. In init function, we need to use several private variables to record the newest transaction low price, high price, last trading date, etc. 

In signal function, by inputing the trade date, we're able to judge whether it satisfy the trading condition. The function will return the correct postion base on the comparision of current price and last high/low price, and of course our current position. Ploting the netvalue is just looping the date and update our return & netvalue.

## 4.Result analysis

![netvalue curve1](https://github.com/algo21-Sam/Assignment2/blob/main/net_value.png)

To be honest, the curve doesn't show up to be quite supportive. Thus, we decide to change the backtest period to 2008/01/02 to 2021/04/19.

![netvalue curve2](https://github.com/algo21-Sam/Assignment2/blob/main/net_value_2.png)

Though we can see that finally we get a better netvalue by holding the asset for a long period, it doesnt' convince me that the strategy is that bad enough. It's obvious that from 2008-2015 when the market endure severe dropdown, the strategy can perform much better than simply holding it all time. 
