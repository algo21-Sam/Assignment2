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
