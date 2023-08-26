import numpy as np
import pandas as pd
from Portfolio5 import Portfolio

class BuyAndHoldPortfolio(Portfolio):
    
    def __init__(self,stock,returns,eta):
            super().__init__(stock,returns,eta,"Buy and Hold Portfolio")
            self.stocks = stock
            self.returns = returns
            self.num_stocks = len(self.stocks.columns)
            self.weights = self.calculate_weights()
            self.p =  self.transaction_cost_budget / len(self.stocks)

    def calculate_weights(self):
            return np.array([1 / self.num_stocks] * self.num_stocks)
        
    def rebalance_portfolio(self,time,mode = "Single Transaction",visualize = True):
        
        self.portfolio = self.weights * (self.budget) / self.stocks.iloc[time]  
        self.portfolio = np.floor(self.portfolio)
        
        self.remaining_budget = self.budget - np.sum(self.portfolio * self.stocks.iloc[time])
        
        self.budget = np.sum(self.portfolio * self.stocks.iloc[time+1]) + self.remaining_budget 
        
        #updating the weights 
        self.weights = self.portfolio * self.stocks.iloc[time+1] / (self.budget - self.remaining_budget)
        
        
    def run(self,mode="percentage"):
        
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

            #Check if the new weights don't exceed the cost budget and update the portfolio
            self.rebalance_portfolio(time=t, mode = mode,visualize = False)