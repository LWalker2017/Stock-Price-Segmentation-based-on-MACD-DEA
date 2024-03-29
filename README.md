# Stock-Price-Segmentation-based-on-MACD-DEA
## A Quantitative Timing Strategy

In light of Elliott wave principle and Fractal theory, I carried out preprocessing of over 10GB financial data and divided stock price action into two portions: trends (stock price going up) and corrections (stock price going down). Applied MACD/DEA index, this strategy could not only be used to select stocks for the portfolio but also become a decision variable to decide what the optimal time to buy and sell stocks.

In order to implement this strategy efficiently, I design an algorithm to look for the local minimum price and local maximum price of the time series respectively. Plus, my algorithm would confirm the formation of the waves, with the precision over 85%. Using a simple daily-level momentum strategy on the SSE Composite Index, it has achieved an annualized return of 13.59% over the past 10 years, with the annualized volatility of 20.13%, the sharpe ratio of 0.68 and the maximum drawdown less than 40%. After joining the trading strategy with the level misalignment (daily-level and 30-minute-level), the annualized revenue rose to 18.95%, with the annualized volatility of 19.59%, the sharpe ratio of 0.97 and the maximum drawdown was reduced to 30%.

上证指数: SSE Composite Index

![Image_text](https://github.com/LWalker2017/Stock-Price-Segmentation-based-on-MACD-DEA/blob/master/image/1day-30min-combine.png)

![Image_text](https://github.com/LWalker2017/Stock-Price-Segmentation-based-on-MACD-DEA/blob/master/image/20160701-20190701-1day.png)

![Image_text](https://github.com/LWalker2017/Stock-Price-Segmentation-based-on-MACD-DEA/blob/master/image/20160701-20190701-30min.png)

<div align=center><img src="https://github.com/LWalker2017/Stock-Price-Segmentation-based-on-MACD-DEA/blob/master/image/momentum-return.png"/></div>
