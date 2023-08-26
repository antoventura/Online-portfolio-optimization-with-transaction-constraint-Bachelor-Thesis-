import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd

def sharpe_ratio(returns,rfr = 0.01,time_period = 5):
    '''
    param:returns : vector of daily portfolio returns.
    param:rfr : value of the risk free rate. Default is 0.01
    param:time_period : length of the time of the portfolio for adjusting the risk free rate. 
    
    Sharpe Ratio = (average return - risk free rate) / volatility
    
    Returns:
        float: Daily Sharpe Ratio.
    
    '''
    rf_rate_adjusted = (1 + rfr) ** time_period - 1
    rf = rf_rate_adjusted / 252   
    
    average_return = np.mean(returns)
    volatility = np.std(returns, ddof=1)  # Use ddof=1 for sample standard deviation
    
    sr = (average_return - rf) / volatility
    
    return sr 


def information_ratio(portfolio_returns, benchmark_returns):
    """
    param:portfolio_returns : Series of daily portfolio returns.
    param:benchmark_returns : Series of benchmark daily returns. 

    Returns:
        float: Information Ratio.
    """
    
    if type(portfolio_returns) == list:
        portfolio_returns = np.array(portfolio_returns)
    if type(benchmark_returns) == list:
        benchmark_returns = np.array(benchmark_returns)
        
    if type(portfolio_returns) != type(np.array(0)) or type(benchmark_returns) != type(np.array(0)) :
        raise Exception("Both Portfolio and Benchmark Return must be either a list or a numpy array")
    
    active_returns = portfolio_returns - benchmark_returns
    tracking_error = active_returns.std()
    if tracking_error != 0:
        information_ratio = active_returns.mean() / tracking_error
    else:
        return 0
    
    return information_ratio

def annualized_return(returns, freq=252):
    """
    param:returns : Series of daily portfolio returns.
    param:freq : Number of trading days in a year.

    Returns:
        float: Annualized return.
    """
    if type(returns) == list:
        returns = np.array(returns)
        
    if type(returns) != type(np.array(0)):
        raise Exception("Returns must be either a list or a numpy array")
        
    num_periods = len(returns)
    total_return = (returns + 1).prod() - 1
    annualized_return = (1 + total_return) ** (freq / num_periods) - 1
    
    return annualized_return

def max_drawdown_period(returns,cum_wealth,plot=False):
    """
    param:returns : Series of daily portfolio returns.
    param:cum_wealth : List of portfolio wealth at each time t
    param:plot : [True,False]. If True plots the max and min peak of the drawdown period 

    Returns:
        float: % value of Max Drawdown period in real or nominal terms of drop in value.
        
    Partially from:
    https://stackoverflow.com/questions/22607324/start-end-and-duration-of-maximum-drawdown-in-python
    
    """
    if type(returns) == list:
        returns = np.array(returns)
        
    if type(returns) != type(np.array(0)):
        raise Exception("Returns must be either a list or a numpy array")
        
    xs = returns.cumsum()
    i = np.argmax(np.maximum.accumulate(xs) - xs) # end of the period
    j = np.argmax(xs[:i]) # start of period
    
  
    drawdown = (cum_wealth[j] - cum_wealth[i]) / cum_wealth[j]  * 100
    
    if plot:
        plt.figure(figsize=(13, 5))
        plt.plot(cum_wealth)
        plt.plot([i, j], [cum_wealth[i], cum_wealth[j]], 'o', color='Red', markersize=10)
        
    
    
  
    return drawdown

def winning_percentage(returns):
    """
    
    param:returns : Series of daily portfolio returns.

    Returns:
        float: Winning percentage.
    """
    
    if type(returns) == list:
        returns = np.array(returns)
        
    if type(returns) != type(np.array(0)):
        raise Exception("Returns must be either a list or a numpy array")
    
    num_winning_trades = (returns > 0).sum()
    total_trades = len(returns)
    winning_percentage = num_winning_trades / total_trades
    
    return winning_percentage




def sortino_ratio(returns, rfr=0.01):
    """
   
    param:returns : List or array of portfolio returns.
    param:risk_free_rate : Risk-free rate of return. Default is 0.01.

    Returns:
        float: The Sortino Ratio.
    """
    rf_rate_adjusted = (1 + rfr) ** 5 - 1
    rf = rf_rate_adjusted / 252   
    
    returns = np.array(returns)
    downside_returns = np.minimum(returns - rf, 0)  # Calculate downside returns
    downside_std = np.std(downside_returns, ddof=1)  # Standard deviation of downside returns

    if downside_std != 0:
        sortino_ratio = (np.mean(returns - rf) / downside_std)
    else:
        sortino_ratio = np.inf

    return sortino_ratio


def ulcer(r, rf_rate=0.01, freq=None):
    """Compute Ulcer ratio."""
    
    if type(r) == list:
        r = np.array(r)
        
    if type(r) != type(np.array(0)):
        raise Exception("Returns must be either a list or a numpy array")
        
        
    rf = rf_rate / 252

    # subtract risk-free rate
    r -= rf

    # annualized excess return
    mu = r.mean() * 252

    # ulcer index
    x = (1 + r).cumprod()

    if isinstance(x, pd.Series):
        drawdown = 1 - x / x.cummax()
    else:
        drawdown = 1 - x / np.maximum.accumulate(x)

    return mu / np.sqrt((drawdown**2).mean())

