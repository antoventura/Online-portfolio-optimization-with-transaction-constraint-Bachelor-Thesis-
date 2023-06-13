import numpy as np
import pandas as pd
from Portfolio5 import Portfolio

class ValueWeightedPortfolio(Portfolio):
    
    def __init__(self,stock,returns,eta):
            super().__init__(stock,returns,eta,"Value Weighted Portfolio")
            self.stocks = stock
            self.returns = returns
            self.num_stocks = len(self.stocks.columns) 
            
    def calculate_weights(self,t):
        total_value = np.sum(self.weights * self.stocks.iloc[t])
        return self.weights * self.stocks.iloc[t] / total_value
    
    
    def rebalance_portfolio(self,time,mode = "Single Transaction",visualize = True):
        
        self.weights = self.calculate_weights(time)
        self.portfolio = self.weights * (self.budget) / self.stocks.iloc[time]    #rimettere il budget intero ogni volta ?
        self.portfolio = np.floor(self.portfolio)


        #computing how much budget we have by removing the decimals  
        self.new_remaining_budget = self.budget - np.sum(self.portfolio * self.stocks.iloc[time])
        #self.weights = self.portfolio * self.stocks.loc[t][1:] / (self.budget - self.remaining_budget)
        
        #computing transaction costs
        self.tr = self.transaction_costs(initial_stocks = self.initial_stocks, new_stocks = self.portfolio,mode = mode, time = time, perc = 0.2,visualize = visualize)
        
        #setting the portofolio of t-1
        self.initial_stocks = self.portfolio.copy()

        #updating new remaining budget
        self.remaining_budget = self.new_remaining_budget

        #updating the budget 
        self.budget = np.sum(self.portfolio * self.stocks.iloc[time+1]) + self.remaining_budget - self.tr

        #updating the weights 
        self.weights = self.portfolio * self.stocks.iloc[time+1] / (self.budget - self.remaining_budget)
        
        
    def run(self):
        
        for t in range(1,len(self.stocks)-1):
            
            self.cumulative_wealth.append(self.budget)
            #find new weights using hedge

            #Check if the new weights don't exceed the cost budget and update the portfolio
            self.rebalance_portfolio(time=t, mode = "percentage",visualize = False)

