import numpy as np
import pandas as pd
from Portfolio5 import Portfolio

class ValueWeightedPortfolio(Portfolio):
    
    def __init__(self,stock,returns,eta,market_cap):
            super().__init__(stock,returns,eta,"Value Weighted Portfolio")
            self.stocks = stock
            self.returns = returns
            self.num_stocks = len(self.stocks.columns) 
            self.p =  self.transaction_cost_budget / len(self.stocks)
            self.market_cap = market_cap
            weights= self.calculate_weights(t=0)
            
            initial_stocks = weights * self.budget / self.stocks.iloc[0]
            self.initial_stocks = np.floor(initial_stocks)
            self.remaining_budget = self.budget - np.sum(self.initial_stocks * self.stocks.iloc[0])
            self.weights = self.initial_stocks * self.stocks.iloc[0] / (self.budget - self.remaining_budget)
            
    def calculate_weights(self,t):
        return  self.market_cap.iloc[t]/ np.sum(self.market_cap.iloc[t])
    
    
 
        
    def run(self,mode = "percentage"):
        
        for t in range(1,len(self.stocks)-1):
            
            #Compute daily returns
            if len(self.cumulative_wealth)> 0:
                daily_r = (-self.cumulative_wealth[-1] + self.budget) / self.cumulative_wealth[-1]
                self.daily_returns.append(daily_r)
            else: 
                daily_r = (-10**5 + self.budget) / 10**5
                self.daily_returns.append(daily_r)
                
            
            self.cumulative_wealth.append(self.budget)
            
            self.cumulative_cost.append(self.initial_transaction_cost_budget - self.transaction_cost_budget)
            
            #find new weights using hedge
            new_weights = self.calculate_weights(t = t)

            #Check if the new weights don't exceed the cost budget and update the portfolio
            self.rebalance_portfolio(t=t, new_weights=new_weights, mode = mode,visualize = False)